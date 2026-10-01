"""Download explicitly selected public files with access checks and a byte audit.

No crawling, login, certificate bypass or automatic publication. Missing robots
(404) means no rules; access denial or unreadable policy stops the download.
"""
import argparse
import hashlib
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, urlsplit
from urllib.robotparser import RobotFileParser

import requests

ROOT = Path(__file__).resolve().parent
USER_AGENT = 'Kaali/1.0 (public statistical research)'


def allowed(session, url):
    parts = urlsplit(url)
    if parts.scheme != 'https' or not parts.hostname or parts.username:
        raise ValueError('Only public HTTPS URLs are supported')
    origin = f'{parts.scheme}://{parts.netloc}'
    response = session.get(origin + '/robots.txt', timeout=25)
    if response.status_code == 404:
        return {'url': response.url, 'status': 404, 'rule': 'no published robots file'}
    response.raise_for_status()
    if response.status_code != 200 or '<html' in response.text.lower():
        raise ValueError('Robots policy could not be read')
    parser = RobotFileParser()
    parser.parse(response.text.splitlines())
    if not parser.can_fetch(USER_AGENT, url):
        raise ValueError('Robots policy disallows automated download')
    time.sleep(max(2, parser.crawl_delay(USER_AGENT) or parser.crawl_delay('*') or 0))
    return {'url': response.url, 'status': 200, 'sha256': hashlib.sha256(response.content).hexdigest()}


def validate_payload(content, suffix):
    if not content:
        raise ValueError('Empty download')
    if suffix == '.pdf' and not content.startswith(b'%PDF-'):
        raise ValueError('Expected PDF; server returned a different payload')
    if suffix in {'.xlsx', '.zip'} and not content.startswith(b'PK'):
        raise ValueError('Expected ZIP/XLSX file signature')
    if suffix in {'.csv', '.json', '.geojson'} and content.lstrip().lower().startswith((b'<!doctype html', b'<html')):
        raise ValueError('Expected data file; server returned HTML')


def download(spec):
    destination = (ROOT/'raw'/spec['path']).resolve()
    if not destination.is_relative_to((ROOT/'raw').resolve()):
        raise ValueError('Destination must stay inside raw/')
    audit = {**spec, 'attemptedAt': datetime.now(timezone.utc).isoformat(), 'status': 'pending'}
    directory=ROOT/'raw'/'acquisition-audits'
    name=hashlib.sha256(spec['url'].encode()).hexdigest()[:16]
    audit_path=directory/f'{name}.json'
    if destination.exists():
        if audit_path.exists():
            previous=json.loads(audit_path.read_text(encoding='utf-8'))
            if (previous.get('status') == 'downloaded' and previous.get('path') == spec['path']
                    and previous.get('sha256') == hashlib.sha256(destination.read_bytes()).hexdigest()):
                return previous | {'reuse': 'existing bytes verified; no new retrieval'}
        raise ValueError(f'Refusing to overwrite existing raw file: {destination.name}')
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    try:
        url = spec['url']
        policies = []
        for _ in range(5):
            policies.append(allowed(session, url))
            time.sleep(2)
            response = session.get(url, timeout=(15, 60), allow_redirects=False, stream=True)
            if response.is_redirect:
                url = urljoin(url, response.headers['Location'])
                response.close()
                continue
            response.raise_for_status()
            if response.status_code != 200:
                raise ValueError(f'Unexpected HTTP status {response.status_code}')
            chunks=[]
            size=0
            for chunk in response.iter_content(1024*1024):
                size += len(chunk)
                if size > 150*1024*1024:
                    raise ValueError('Download exceeds 150 MB limit')
                chunks.append(chunk)
            content=b''.join(chunks)
            validate_payload(content, destination.suffix.lower())
            destination.parent.mkdir(parents=True, exist_ok=True)
            with destination.open('xb') as output:
                output.write(content)
            audit.update(status='downloaded', retrievedAt=datetime.now(timezone.utc).isoformat(), finalUrl=url,
                         bytes=len(content), sha256=hashlib.sha256(content).hexdigest(),
                         contentType=response.headers.get('Content-Type'), lastModified=response.headers.get('Last-Modified'), robots=policies)
            break
        else:
            raise ValueError('Too many redirects')
    except (requests.RequestException, ValueError) as error:
        audit.update(status='unavailable', reason=f'{type(error).__name__}: {error}')
    finally:
        session.close()
    directory.mkdir(parents=True, exist_ok=True)
    audit_path.write_text(json.dumps(audit,indent=2,ensure_ascii=False),encoding='utf-8')
    return audit


if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('manifest', type=Path)
    args=parser.parse_args()
    for source in json.loads(args.manifest.read_text(encoding='utf-8')):
        result=download(source)
        print(json.dumps(result,ensure_ascii=True),flush=True)
