"""Export a file://-browsable copy of dist without changing research artifacts."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit
import re, posixpath, hashlib, json, zipfile, tempfile, shutil
R=Path(__file__).resolve().parents[1]
D=R/'dist'
NAME='MQM_OFFLINE_WEBSITE_v1.zip'
DEST=R/'offline-build';DEST.mkdir(exist_ok=True)
class Audit(HTMLParser):
 def __init__(self,base,root):super().__init__();self.base=base;self.root=root;self.links=0
 def handle_starttag(self,tag,attrs):
  for key,value in attrs:
   if key not in ('href','src') or not value:continue
   u=urlsplit(value)
   if u.scheme or u.netloc or not u.path:continue
   assert not u.path.startswith('/'),value
   target=(self.base.parent/u.path).resolve()
   assert target.is_relative_to(self.root.resolve()) and target.is_file(),(self.base,value)
   self.links+=1
with tempfile.TemporaryDirectory() as tmp:
 out=Path(tmp)/'MQM_OFFLINE_WEBSITE';out.mkdir()
 for f in D.rglob('*'):
  if f.is_file() and f.name!=NAME:
   dest=out/f.relative_to(D);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(f,dest)
 for f in out.rglob('*.html'):
  def rewrite(m):
   original=m.group(2);u=urlsplit(original)
   if not original.startswith('/') or original.startswith('//'):return m.group(0)
   p=u.path.lstrip('/');target=out/p
   if target.is_dir():p=(p.rstrip('/')+'/' if p else '')+'index.html'
   relative=posixpath.relpath(p, f.parent.relative_to(out).as_posix())
   if u.query:relative+='?'+u.query
   if u.fragment:relative+='#'+u.fragment
   return m.group(1)+relative+m.group(3)
  source=re.sub(r'<a\b[^>]*href=[\"\']/MQM_OFFLINE_WEBSITE_v1\.zip[\"\'][^>]*>.*?</a>', '', f.read_text())
  f.write_text(re.sub(r'((?:href|src)=[\"\'])(/[^\"\']*)([\"\'])',rewrite,source))
 (out/'README.txt').write_text('MQM offline website\nOpen index.html in a browser. All local page, manuscript, replay-package and stylesheet links work without a network connection. External references require internet access. Research artifact bytes are unchanged. Physical promotion remains 0.\n')
 links=0
 for f in out.rglob('*.html'):
  a=Audit(f,out);a.feed(f.read_text());links+=a.links
 data=json.loads((R/'research/session_catalogue.json').read_text())
 for release in data['releases']:
  for path,expected in [(release['zip_url'],release['zip_sha256'])]+[(p['url'],p['sha256']) for p in release['pdfs']]:
   assert hashlib.sha256((out/path.lstrip('/')).read_bytes()).hexdigest()==expected
 hashes={str(f.relative_to(out)):hashlib.sha256(f.read_bytes()).hexdigest() for f in out.rglob('*') if f.is_file()}
 (out/'OFFLINE_MANIFEST.json').write_text(json.dumps(dict(files=hashes,local_links_checked=links,releases=len(data['releases']),physical_promotion=0),indent=2)+'\n')
 with zipfile.ZipFile(DEST/NAME,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for f in sorted(out.rglob('*')):
   if f.is_file():info=zipfile.ZipInfo(str(f.relative_to(out.parent)),date_time=(1980,1,1,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16;z.writestr(info,f.read_bytes())
 print(json.dumps(dict(offline_zip=NAME,files=len(hashes),local_links_checked=links,releases=len(data['releases']),sha256=hashlib.sha256((DEST/NAME).read_bytes()).hexdigest())))
