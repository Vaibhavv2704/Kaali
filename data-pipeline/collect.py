"""Permission-gated collectors. No crawling or private incident publication by default."""
import argparse
import hashlib
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse, urlunparse
from urllib.robotparser import RobotFileParser
import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent

def canonical_url(url):
    parsed = urlparse(url)
    if parsed.scheme != 'https' or not parsed.hostname:
        raise ValueError('Only HTTPS source URLs are permitted')
    return urlunparse(parsed._replace(fragment=''))

def fetch_permitted(source, user_agent):
    if not source.get('approved') or not source.get('license') or not source.get('termsReviewedAt'):
        raise ValueError(f"{source['id']}: licence/terms approval required; no request sent")
    url = canonical_url(source['url'])
    origin = f"https://{urlparse(url).netloc}"
    session = requests.Session()
    session.headers['User-Agent'] = user_agent
    robots = session.get(origin + '/robots.txt', timeout=20, allow_redirects=False)
    if robots.status_code != 200:
        raise ValueError('robots.txt unavailable: manual access review required')
    parser = RobotFileParser()
    parser.parse(robots.text.splitlines())
    if not parser.can_fetch(user_agent, url):
        raise ValueError('robots.txt disallows collection')
    time.sleep(max(2, parser.crawl_delay(user_agent) or parser.crawl_delay('*') or 0))
    response = session.get(url, timeout=30, allow_redirects=False)
    response.raise_for_status()
    if response.status_code != 200:
        raise ValueError('Redirect or unexpected response requires new permission review')
    return response

def news_candidate(html, url, reviewed_headline):
    # Raw article text is inspected only in memory; publication needs manual review.
    # Requiring an approved headline prevents accidental victim identity publication.
    if not reviewed_headline or len(reviewed_headline) > 180:
        raise ValueError('Privacy-reviewed headline required, max 180 characters')
    BeautifulSoup(html, 'html.parser').decompose()
    url = canonical_url(url)
    return {'id': hashlib.sha256(url.encode()).hexdigest()[:16], 'url': url, 'headline': reviewed_headline}

def extract_candidates(html, nlp):
    """Optional spaCy GPE/LOC/date candidates. Return for private human review only."""
    import trafilatura
    text = trafilatura.extract(html) or ''
    doc = nlp(text)
    return [{'label': e.label_, 'value': e.text} for e in doc.ents if e.label_ in {'GPE', 'LOC', 'DATE', 'TIME'}]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--config', type=Path, default=ROOT/'config/sources.json')
    ap.add_argument('--source', required=True)
    args = ap.parse_args()
    config = json.loads(args.config.read_text())
    source = next(s for s in config['sources'] if s['id'] == args.source)
    response = fetch_permitted(source, config['userAgent'])
    output = ROOT/'private'
    output.mkdir(exist_ok=True)
    # Source payloads remain ignored private staging; never copy articles to public/data.
    (output/f"{source['id']}.audit.json").write_text(json.dumps({'source':source['url'],'retrievedAt':datetime.now(timezone.utc).isoformat(),'status':response.status_code,'sha256':hashlib.sha256(response.content).hexdigest()},indent=2))
    print('Access checked; audit saved. Payload not persisted; supply reviewed adapters for dataset import.')

if __name__ == '__main__':
    main()
