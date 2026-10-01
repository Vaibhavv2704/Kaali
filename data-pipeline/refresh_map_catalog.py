"""Read MapTiler's documented public style metadata, not map tiles."""
import json,re,hashlib
from pathlib import Path
from public_download import download
ROOT=Path(__file__).resolve().parent
URL='https://raw.githubusercontent.com/maptiler/maptiler-client-js/refs/heads/main/src/mapstyle.ts'
def main():
 result=download({'url':URL,'path':'maptiler/mapstyle.ts','source':'MapTiler public client style metadata','licence':'MapTiler client repository licence; metadata only'})
 if result['status']!='downloaded':raise ValueError(result.get('reason','Catalogue unavailable'))
 path=ROOT/'raw/maptiler/mapstyle.ts';text=path.read_text();styles=[]
 for block in re.findall(r'\{\s*id: "[^"]+".*?\n\s*\}',text,re.S):
  block=re.sub(r'//[^\n]*','',block)
  if re.search(r'deprecated:\s*true',block):continue
  match=re.search(r'id: "([^"]+)"',block)
  if match: styles.append({'id':match[1],'label':match[1].replace('-',' ').title()})
 if not styles:raise ValueError('No documented catalogue entries')
 target=ROOT.parent/'src/data/map-catalog.json'
 target.write_text(json.dumps({'sourceUrl':URL,'reviewedAt':'2026-10-02','sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'styles':styles},indent=2)+'\n')
 print('Documented catalogue variants: '+str(len(styles)))
if __name__=='__main__':main()
