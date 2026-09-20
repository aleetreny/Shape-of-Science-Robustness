"""Exact set/rank operations, checked against the frozen reference implementation."""
import ctypes,subprocess
import numpy as np
from .common import ROOT,OUT,file_sha,write_json
from sos_analysis.geometry import normalize_rows
_LIBRARY=None

def library():
 global _LIBRARY
 if _LIBRARY is None:
  src=ROOT/'sos_closure/kernels.c';folder=OUT/'technical';folder.mkdir(parents=True,exist_ok=True)
  dest=folder/('kernels_'+file_sha(src)[:16]+'.dylib')
  if not dest.exists():subprocess.run(['/usr/bin/clang','-O3','-std=c11','-dynamiclib',str(src),'-o',str(dest)],check=True)
  _LIBRARY=ctypes.CDLL(str(dest));ip=np.ctypeslib.ndpointer(dtype=np.int32,flags='C_CONTIGUOUS');dp=np.ctypeslib.ndpointer(dtype=np.float64,flags='C_CONTIGUOUS')
  _LIBRARY.filter_rankings.argtypes=[ip,ip,ip,*([ctypes.c_int]*4),ip];_LIBRARY.filter_rankings.restype=ctypes.c_int
  _LIBRARY.overlap_sums.argtypes=[ip,*([ctypes.c_int]*3),ip,ip,ctypes.c_int,ip,ctypes.c_int,ctypes.c_int,dp];_LIBRARY.overlap_sums.restype=ctypes.c_int
 return _LIBRARY

def full_ranks(x,ids):
 assert np.all(np.diff(ids)>0)
 x=normalize_rows(x);sim=np.round(x@x.T,12);np.fill_diagonal(sim,-np.inf)
 return np.ascontiguousarray(np.argsort(-sim,axis=1,kind='stable'),dtype=np.int32)

def restrict(ranks,selections,ids,k=50):
 ranks=np.ascontiguousarray(ranks,dtype=np.int32);sel=np.ascontiguousarray(selections,dtype=np.int32);ids=np.ascontiguousarray(ids,dtype=np.int32)
 assert ranks.shape==(len(ids),len(ids)) and sel.ndim==2 and sel.shape[1]>k
 assert np.all((sel>=0)&(sel<len(ids))) and all(len(np.unique(s))==len(s) for s in sel)
 out=np.empty((*sel.shape,k),dtype=np.int32)
 result=library().filter_rankings(ranks,sel,ids,len(ids),len(sel),sel.shape[1],k,out);assert result==0,result
 return out

def overlaps(neighbors,pairs,ks=(10,25,50)):
 nn=np.ascontiguousarray(neighbors,dtype=np.int32);pairs=np.array(pairs,dtype=np.int32);left=np.ascontiguousarray(pairs[:,0]);right=np.ascontiguousarray(pairs[:,1]);ks=np.ascontiguousarray(ks,dtype=np.int32)
 assert nn.ndim==3 and max(ks)<=nn.shape[2] and nn.shape[1]>0
 out=np.empty((len(pairs),len(ks)),float)
 result=library().overlap_sums(nn,len(nn),nn.shape[1],nn.shape[2],left,right,len(pairs),ks,len(ks),500000,out);assert result==0,result
 return out
