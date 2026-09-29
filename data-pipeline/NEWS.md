# News extraction

The user explicitly reinstated news/article-text extraction on 2026-09-30 after the narrower Phase 1 source list. Public access, robots rules, publisher restrictions and victim privacy still apply. No permission document is requested from the user for public-source factual research. SafeCity, Safetipin and private police/RTI datasets remain deferred.

## Reproduce the first Delhi extraction

```powershell
.venv/Scripts/python.exe data-pipeline/news_extract.py --review data-pipeline/config/news-delhi-review.json
.venv/Scripts/python.exe -m unittest discover -s data-pipeline/tests
```

The first command checks robots, waits at least two seconds (or a longer crawl delay), fetches one reviewed public article, extracts its article container in memory, and checks that the reviewed category/count/year tokens remain present. Redirects, inaccessible robots and changed evidence stop extraction. No alternate endpoint or paywall bypass is attempted.

Output: `data-pipeline/raw/news/4da9308a5bd296b3.facts.json`. This ignored staging file contains nine facts, a content hash, retrieval time and provenance; no body, victim details, addresses, images or quotations. The reviewed facts have also been copied to `public/data/news.json` and are displayed on `/evidence` as news-reported figures.

The hash covers the decoded HTML encoded as UTF-8, not immutable publisher bytes. Navigation changes may change it. Numeric-token checks are drift detection, **not automated evidence of the relationships between numbers**. The category/year/count relationships in this first adapter were individually reviewed against the article. New articles require their own review and an appropriate adapter; do not reuse these nine figures or the selector blindly.

## Incident extraction next

Extract locality, event date, event time and category only when the article explicitly associates them with the incident. Keep publication date separate from event date. Reporting station, dateline, victim residence and arrest location are not incident locations. Keep missing or ambiguous values null. Do not store person entities or residential addresses. Deduplicate corroborating reports by reviewed event identity before aggregation; similar locality/date/category alone is only a review hint.

News observation frequency measures media coverage as well as reporting; it is not an unbiased crime census. The current article contains annual city aggregates only. It supplies no neighbourhood targets, exposure, observed negative cases or time bands, so no risk score or training label is generated. Source category wording is preserved without claiming IPC/BNS equivalence. Never add this report to overlapping NCRB totals or other reports of the same police release.

## Access failure

Do not substitute invented figures if the command fails. Existing published facts retain their original retrieval date. A failure requires another publicly permitted source or an explicitly reviewed manual factual record, never silent use of a search snippet as a downloaded article.
