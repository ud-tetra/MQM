import os
os.environ['OPENBLAS_NUM_THREADS']='1'
from pathlib import Path
import json
import numpy as np
from scipy.sparse import csr_matrix
P=Path(__file__).resolve().parent
ns={'__file__':str(P/'inputs/response_model.py')};exec((P/'inputs/response_model.py').read_text(),ns)
_,Hd,_=ns['models'](192);H=csr_matrix(Hd);assert max(np.diff(H.indptr))<=196
V=np.zeros((196,3));V[0,0]=1;V[1,1]=1;V[0,2]=V[2,2]=1
R=V.copy();I=np.zeros_like(R)
for step in range(128):
 ar=R.copy();ai=I.copy();tr=R.copy();ti=I.copy()
 for k in range(1,49):
  nr=(H@ti)/(8*k);ni=-(H@tr)/(8*k)
  ar+=nr;ai+=ni;tr,ti=nr,ni
 R,I=ar,ai
out={'status':'BINARY64 exact returned data; requires arithmetic and transfer ledger','steps':128,'degree':48,'real':R[:4].tolist(),'imag':I[:4].tolist(),'row_nonzeros':int(max(np.diff(H.indptr))),'squared_native_norms':np.sum(R[:4]**2+I[:4]**2,axis=0).tolist()}
(P/'results/LAUNCH_OUTPUT.json').write_text(json.dumps(out,indent=2)+'\n');np.savez(P/'results/LAUNCH_VECTORS.npz',vectors=R+1j*I)
print(out)
