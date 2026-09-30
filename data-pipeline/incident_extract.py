"""Extract one manually reviewed news event; never retain article prose or people."""
import argparse
import hashlib
import json
from datetime import date, datetime, timezone
from pathlib import Path
from collect import canonical_url, fetch_permitted


def extract(html, review):
    import trafilatura
    required={'id','url','publisher','headline','publishedAt','reviewedAt','regionId','cityId',
              'privacyReviewed','event','access','evidenceTokens'}
    if set(review)!=required or review['privacyReviewed'] is not True:
        raise ValueError('Exact reviewed fields required; personal fields forbidden')
    canonical_url(review['url'])
    if not 1<=len(review['headline'])<=180:raise ValueError('Invalid editorial headline')
    event=review['event']
    if set(event)!={'id','locality','date','dateBasis','timeBand','category','status'}:
        raise ValueError('Unexpected event fields')
    if event['status']!='reported-allegation':raise ValueError('News does not establish conviction')
    if event['category'] not in ['molestation','rape','harassment','sexual-assault']:
        raise ValueError('Unreviewed category')
    if event['timeBand'] is not None and (type(event['timeBand']) is not int or event['timeBand'] not in range(6)):
        raise ValueError('Invalid time band')
    published=date.fromisoformat(review['publishedAt']);date.fromisoformat(review['reviewedAt'])
    if event['date'] is not None and date.fromisoformat(event['date'])>published:
        raise ValueError('Event after publication')
    if event['dateBasis'] not in ['explicit','day-month-with-publication-year','unknown']:
        raise ValueError('Unreviewed date basis')
    if (event['date'] is None)!=(event['dateBasis']=='unknown'):
        raise ValueError('Date basis mismatch')
    body=trafilatura.extract(html,include_comments=False)
    if not body:raise ValueError('No article text')
    text=' '.join(body.casefold().split())
    if not review['evidenceTokens'] or any(token.casefold() not in text for token in review['evidenceTokens']):
        raise ValueError('Reviewed evidence changed; re-review required')
    # Tokens detect drift only. Locality/date/time association needs human review.
    return {k:review[k] for k in ['id','url','publisher','headline','publishedAt','reviewedAt',
                                 'regionId','cityId','privacyReviewed','event']}|{
        'kind':'incident-report','origin':'news','eligibleForTraining':False,
        'neighbourhoodId':None,'observationCoverage':'unknown',
        'sha256':hashlib.sha256(html.encode()).hexdigest(),
        'retrievedAt':datetime.now(timezone.utc).isoformat(),
        'licence':'Publisher copyright; linked factual extraction only. No article republication.'}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--review',type=Path,required=True)
    args=parser.parse_args();review=json.loads(args.review.read_text(encoding='utf-8'))
    response=fetch_permitted(review['access']|{'id':review['id'],'url':review['url']},
                             'KaaliResearch/1.0 (single-article factual extraction)')
    record=extract(response.text,review)
    path=Path(__file__).parent/'raw/news'/(hashlib.sha256(review['url'].encode()).hexdigest()[:16]+'.event.json')
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
    print(f'Reviewed event facts saved: {path.name}; no body, identities or coordinates retained.')


if __name__=='__main__':main()
