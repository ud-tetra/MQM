"""Release gates: local routes, package replay, branch consistency and claim hygiene."""
from pathlib import Path
from collections import Counter
import json,hashlib,zipfile,tempfile,subprocess,sys,re
from lxml import html
ROOT=Path(__file__).resolve().parents[1];D=ROOT/'dist'
pages=list(D.rglob('*.html'));assert len(pages)==6
ids={};trees={}
for p in pages:
 t=html.fromstring(p.read_bytes());trees[p]=t
 values=t.xpath('//@id');assert all(n==1 for n in Counter(values).values()),p
 assert len(t.xpath('//h1'))==1
 assert t.get('lang')=='en'
 assert len(t.xpath('//details'))==len(t.xpath('//details/summary'))
 assert all(x.xpath('./caption') for x in t.xpath('//table'))
 assert t.xpath('//meta[@name="description"]/@content')
 ids[p]=set(values)
for p,t in trees.items():
 for url in t.xpath('//@href')+t.xpath('//@src'):
  if url.startswith(('https://','data:')):continue
  route,_,fragment=url.partition('#')
  target=(D/route.lstrip('/')) if route else p
  if target.is_dir():target=target/'index.html'
  assert target.is_file(),(p,url)
  if fragment:assert fragment in ids[target],(p,url)
 for x in t.xpath('//@aria-labelledby'):
  assert all(v in ids[p] for v in x.split())
 text=t.text_content()
 assert not re.search(r'Lattix|TetraDEC|Evaluate quantum\s*architecture|Keep the geometry',text,re.I)
 assert not re.search(r'10[⁻−-]⁴|10\s*−4|1e-4|p\*\s*[~≈=]',text)
 if p.parent.name!='origin':assert 'Unified Dynamics' not in text
assert len(list(D.glob('*.zip')))==1
archive=D/'MQM_RESEARCH_RELEASE_0.5.zip'
assert (D/'MQM_RESEARCH_RELEASE_0.5.sha256').read_text().split()[0]==hashlib.sha256(archive.read_bytes()).hexdigest()
with tempfile.TemporaryDirectory() as tmp:
 with zipfile.ZipFile(archive) as z:
  assert z.testzip() is None
  for name in z.namelist():
   assert not name.startswith('/') and '..' not in Path(name).parts
   assert '__pycache__' not in name and '.openai' not in name
   assert not re.search(r'sealed|credentials|\.env',name,re.I)
  z.extractall(tmp)
 root=Path(tmp)/'MQM_0.5'
 result=subprocess.run([sys.executable,'-B','support/verify_release.py'],cwd=root,check=True,capture_output=True,text=True)
 replay=json.loads(result.stdout)
 branches=json.loads((root/'branches.json').read_text());schema=json.loads((root/'schema/branch.schema.json').read_text())
 assert len(branches)==3
 for b in branches:
  assert set(b)==set(schema['required'])
  assert len(b['logicals']['X'])==len(b['logicals']['Z'])==b['n_data']
  for p in b['generators']['center']+b['generators']['gauge']:
   assert len(p)==b['n_data'] and set(p)<=set('IXYZ')
  assert b['n_gauge']>=0 and b['n_data']>b['n_gauge']
  for syndrome,pauli in b['decoder']['lookup'].items():
   assert len(syndrome)==len(b['generators']['center']) and set(syndrome)<=set('01')
   assert len(pauli)==b['n_data'] and set(pauli)<=set('IXYZ')
 assert branches[2]['n_ancilla'] is None
 import stim
 circuits=list((root/'circuits').rglob('*.stim'));assert len(circuits)==21
 for p in circuits:stim.Circuit(p.read_text())
info=subprocess.run(['pdfinfo',str(ROOT/'release/docs/ENTANGLER_LEMMA.pdf')],check=True,capture_output=True,text=True).stdout
assert re.search(r'Pages:\s+1\b',info)
report={'release':'0.5','date':'2026-09-18','static_pages':len(pages),'routes_assets_fragments':'PASS','semantic_structure':'PASS','public_memory_numbers':'REMOVED','industrial_names':'ABSENT','origin_isolated':'PASS','public_release_zips':1,'clean_extraction':replay,'branch_record_consistency':'PASS','stim_circuits_parsed':21,'track_a_inventory':'20 logical draft circuits; ideal expectations checked during creation; experimental acceptance not frozen','lemma_pdf':'one A4 page; rendered and visually inspected','independent_replication':False,'hardware_executed':False,'physical_promotion':0,'browser_visual_qa':'NOT_RUN: plain static project has no compatible supervised preview','custom_hostname':'prepared; DNS and TLS activation pending'}
(ROOT/'docs/MQM_RESEARCH_ACCEPTANCE_v0.5.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
