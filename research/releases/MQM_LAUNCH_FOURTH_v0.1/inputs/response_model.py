import os
os.environ['OPENBLAS_NUM_THREADS']='1';os.environ['OMP_NUM_THREADS']='1'
from pathlib import Path
import json,math,time
import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import expm_multiply
P=Path(__file__).resolve().parent;protocol=json.loads((P/'PROTOCOL.json').read_text())
def models(M):
 x,w=leggauss(M);delta=16*x;c=np.sqrt(64*w/math.pi);n=1/np.expm1((5/16)*(64+delta))
 D=3+4*M+M*(M+1)//2;off=3+4*M
 r=[];s=[];v=[]
 def edge(a,b,z):
  a=np.atleast_1d(a);b=np.atleast_1d(b);z=np.broadcast_to(z,a.shape)
  r.extend([a,b]);s.extend([b,a]);v.extend([z,z])
 edge(np.array([0,1]),np.array([1,2]),1.)
 for a,z in [(0,1.),(1,1.),(2,math.sqrt(4*math.sqrt(2)))]:edge(3+a*M+np.arange(M),3+(a+1)*M+np.arange(M),z)
 for a in range(3):edge(np.full(M,a),3+a*M+np.arange(M),c)
 j,k=np.triu_indices(M);ids=off+np.arange(len(j))
 r.extend([3+np.arange(4*M),ids]);s.extend([3+np.arange(4*M),ids]);v.extend([np.tile(delta,4),delta[j]+delta[k]])
 for a in range(M):
  b=np.arange(M);lo=np.minimum(a,b);hi=np.maximum(a,b);pair=off+lo*(2*M-lo+1)//2+hi-lo
  edge(np.full(M,3+3*M+a),pair,c*np.sqrt(1+(a==b)))
 H=coo_matrix((np.concatenate(v),(np.concatenate(r),np.concatenate(s))),shape=(D,D)).tocsr();H.eliminate_zeros()
 H1=np.zeros((M+4,M+4));H1[0,1]=H1[1,0]=1;H1[1,2]=H1[2,1]=1;H1[2,3]=H1[3,2]=math.sqrt(4*math.sqrt(2));H1[3,4:]=c;H1[4:,3]=c;H1[4:,4:]=np.diag(delta)
 return H,H1,n

def retained(W,n,M):
 out=np.zeros((8,8),complex);root=np.sqrt(n)
 V=W[:3]*root;out[5:8,5:8]=V@V.conj().T
 V=(W[3:3+4*M]*root).reshape(4,M,M)
 out[:4,:4]=np.einsum('ajk,bjk->ab',V,V.conj())
 out[4,4]=np.sum(abs(W[3+4*M:])**2*n)
 return out
