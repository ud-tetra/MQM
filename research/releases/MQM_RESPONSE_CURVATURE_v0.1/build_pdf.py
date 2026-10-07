from pathlib import Path
import subprocess,json
import fitz
P=Path(__file__).resolve().parent; M=P/'manuscript';stem='MQM_RESPONSE_CURVATURE_IEEE_A4_v0.1'
for k in range(2):
 r=subprocess.run(['pdflatex','-interaction=nonstopmode','-halt-on-error',stem+'.tex'],cwd=M,capture_output=True,text=True)
 (P/'results'/f'PDF_BUILD_{k}.txt').write_text(r.stdout+r.stderr)
 assert r.returncode==0
log=(M/(stem+'.log')).read_text();assert 'Overfull' not in log and 'undefined references' not in log
D=fitz.open(M/(stem+'.pdf'));assert all(abs(p.rect.width-595.276)<1 and abs(p.rect.height-841.89)<1 for p in D)
subprocess.run(['pdftoppm','-scale-to','1400','-png',str(M/(stem+'.pdf')),str(P/'results/PAGE')],check=True)
(P/'results/PDF_QA.json').write_text(json.dumps({'pages':len(D),'IEEEtran_A4':True,'overfull_boxes':False,'renderer':'Poppler pdftoppm'},indent=2)+'\n')
print('PDF pages',len(D))
