from pathlib import Path
from html.parser import HTMLParser
import hashlib,json
R=Path(__file__).resolve().parents[1];D=R/'dist';data=json.loads((R/'research/session_catalogue.json').read_text())
for r in data['releases']:
 assert hashlib.sha256((D/r['zip_url'].lstrip('/')).read_bytes()).hexdigest()==r['zip_sha256']
 for p in r['pdfs']:assert hashlib.sha256((D/p['url'].lstrip('/')).read_bytes()).hexdigest()==p['sha256']
class Links(HTMLParser):
 def handle_starttag(self,tag,attrs):
  for k,v in attrs:
   if k in ['href','src'] and v and v.startswith('/'):
    path=D/v.split('#')[0].lstrip('/')
    assert path.is_file() or (path/'index.html').is_file(),v
for f in D.glob('*/index.html'):Links().feed(f.read_text())
Links().feed((D/'index.html').read_text())
assert hashlib.sha256((D/'MQM_RESEARCH_RELEASE_0.5.zip').read_bytes()).hexdigest()=='12479c3490d11faa768f246b5d296630fa656365ada362a243f0ad0e8bb5976b'
assert '127/2²³' in (D/'tracker/index.html').read_text()
assert '773/2²⁶' in (D/'tracker/index.html').read_text()
assert '2⁻²²⁹' in (D/'tracker/index.html').read_text()
assert 'Physical promotion 0' in (D/'research/index.html').read_text()
report={'release_packages':len(data['releases']),'manuscripts':sum(len(r['pdfs']) for r in data['releases']),'hashes_verified':True,'local_links_verified':True,'code_release_0_5_unchanged':True,'thermal_target':'PASS_CONDITIONAL finite window; external review and permanent retention OPEN','physical_promotion':0}
(R/'docs/MQM_SESSION_SITE_QA_2026_10_07.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
