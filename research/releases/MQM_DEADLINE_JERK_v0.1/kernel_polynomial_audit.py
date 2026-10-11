from fractions import Fraction as F
from math import factorial
import json
from pathlib import Path
rows=[]
# Monomials t^a s^b u^c: triangular integral=t^(a+b+c+2)/[(c+1)(b+c+2)].
for a in range(4):
 for b in range(4):
  for c in range(4):
   degree=a+b+c+2
   left=F(degree*(degree-1)*(degree-2),(c+1)*(b+c+2))
   diag=F(3*a+2*b+c)
   boundary=F(3*a*(a-1),c+1)+F(3*a*b,c+1)+F(b*(b-1),c+1)
   bulk=F(a*(a-1)*(a-2),(c+1)*(b+c+2))
   assert left==diag+boundary+bulk
   rows.append({'powers':[a,b,c],'third_coefficient':str(-left)})
P=Path(__file__).resolve().parent
(P/'results/KERNEL_POLYNOMIAL_AUDIT.json').write_text(json.dumps({'status':'EXACT polynomial Leibniz controls; not continuum derivative transfer','monomials':len(rows),'rows':rows,'external_review':'OPEN'},indent=2)+'\n')
print(len(rows),'exact polynomial controls')
