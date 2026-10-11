import os
os.environ['OPENBLAS_NUM_THREADS']='1';os.environ['OMP_NUM_THREADS']='1'
from pathlib import Path
import json,time
import numpy as np
P=Path(__file__).resolve().parent;ns={'__file__':str(P/'inputs/response_model.py')};exec((P/'inputs/response_model.py').read_text(),ns)
M=192;H,H1,n=ns['models'](M);delta=H1.diagonal()[4:];V=np.zeros((H.shape[0],M));V[3+np.arange(M),np.arange(M)]=1.;W=V;norms=[]
for r in range(1,5):
 W=H@W-W*delta;ss=np.sum(W*W,axis=0);norms.append(ss.tolist())
seed=np.zeros((M+4,1));seed[1]=2.;seed[3]=H1[2,3];R=seed;I=np.zeros_like(seed)
for step in range(128):
 ar=R.copy();ai=I.copy();tr=R.copy();ti=I.copy()
 for k in range(1,49):nr=(H1@ti)/(8*k);ni=-(H1@tr)/(8*k);ar+=nr;ai+=ni;tr,ti=nr,ni
 R,I=ar,ai
out={'status':'SIMULATED returned binary64 data; require exact rational enclosure','M':192,'hot_power_squared_norms':norms,'occupation':n.tolist(),'cold_third_live_real':R[:4,0].tolist(),'cold_third_live_imag':I[:4,0].tolist(),'cold_seed_lambda':float(seed[3,0]),'hot_global_launch_triangle_diagnostic':float(np.dot(n,np.sqrt(norms[3])+4*np.sqrt(norms[2])*np.sqrt(norms[0])+3*np.array(norms[1]))),'cold_third_seed':'2p1+lambda*p3'}
(P/'results/LAUNCH_MOMENTS_OUTPUT.json').write_text(json.dumps(out,indent=2)+'\n');print({k:v for k,v in out.items() if k in ['M','hot_global_launch_triangle_diagnostic','cold_seed_lambda']})
