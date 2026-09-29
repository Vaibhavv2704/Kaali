"""Read a reviewed public article in memory; retain structured facts, never its body.

This is a bounded single-article collector, not a crawler. Human review supplies
category/year associations. Presence checks detect changed pages, not truth.
"""
import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

from collect import fetch_permitted, canonical_url

ROOT = Path(__file__).resolve().parent


def validate_review(review):
    required = {'id', 'url', 'publisher', 'headline', 'publishedAt', 'reviewedAt',
                'regionId', 'cityId', 'privacyReviewed', 'facts', 'access'}
    if set(review) != required or review['privacyReviewed'] is not True:
        raise ValueError('Exact reviewed fields and privacy review required')
    canonical_url(review['url'])
    if not 1 <= len(review['headline']) <= 180:
        raise ValueError('Use a short privacy-reviewed editorial headline')
    for key in ('publishedAt', 'reviewedAt'):
        datetime.strptime(review[key], '%Y-%m-%d')
    seen = set()
    for fact in review['facts']:
        if set(fact) != {'category', 'year', 'count'}:
            raise ValueError('Narratives and personal data are not accepted')
        if fact['category'] not in ('rape', 'molestation', 'eve-teasing'):
            raise ValueError('Unreviewed category; extend the mapping explicitly')
        if type(fact['count']) is not int or fact['count'] < 0:
            raise ValueError('Count must be a nonnegative integer')
        if type(fact['year']) is not int or not 1900 <= fact['year'] < int(review['publishedAt'][:4]):
            raise ValueError('Annual review supports completed calendar years only')
        key = (fact['category'], fact['year'])
        if key in seen:
            raise ValueError('Duplicate category/year')
        seen.add(key)
    if not seen:
        raise ValueError('No reviewed facts supplied')


def extract_reviewed(html, review):
    import trafilatura
    from bs4 import BeautifulSoup
    validate_review(review)
    selector = review['access'].get('articleSelector')
    if selector:
        soup = BeautifulSoup(html, 'html.parser')
        containers = soup.select(selector)
        if len(containers) != 1:
            raise ValueError('Reviewed article container changed')
        for element in containers[0].select('script, style, nav, aside'):
            element.decompose()
        body = containers[0].get_text(' ', strip=True)
    else:
        body = trafilatura.extract(html, include_comments=False, include_tables=True)
    if not body:
        raise ValueError('No article text extracted; do not use navigation or snippets')
    # Never log, persist or export article text or automatically detected names.
    normalized = re.sub(r'(?<=\d),(?=\d)', '', body.casefold())
    for fact in review['facts']:
        for token in (str(fact['count']), str(fact['year']), fact['category']):
            if not re.search(r'(?<!\w)' + re.escape(token) + r'(?!\w)', normalized):
                raise ValueError(f'Reviewed evidence token {token!r} missing; re-review required')
    return {key: review[key] for key in ('id', 'url', 'publisher', 'headline',
            'publishedAt', 'reviewedAt', 'regionId', 'cityId', 'privacyReviewed')} | {
        'kind': 'aggregate-report', 'eligibleForTraining': False,
        'facts': review['facts'], 'origin': 'news',
        'neighbourhoodId': None, 'timeBand': None,
        'sha256': hashlib.sha256(html.encode('utf-8')).hexdigest(),
        'retrievedAt': datetime.now(timezone.utc).isoformat(),
        'licence': 'Publisher copyright; linked factual extraction only. No article republication.',
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--review', type=Path, required=True)
    args = parser.parse_args()
    review = json.loads(args.review.read_text(encoding='utf-8'))
    validate_review(review)
    source = review['access'] | {'id': review['id'], 'url': review['url']}
    response = fetch_permitted(source, 'KaaliResearch/1.0 (single-article factual extraction)')
    result = extract_reviewed(response.text, review)
    output = ROOT / 'raw/news'
    output.mkdir(parents=True, exist_ok=True)
    # Filename is derived rather than accepting a config-supplied path.
    target = output / (hashlib.sha256(review['url'].encode()).hexdigest()[:16] + '.facts.json')
    target.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(f'Extracted {len(result["facts"])} reviewed aggregate facts to {target.name}. No article body retained.')


if __name__ == '__main__':
    main()
