#!/usr/bin/env python3
from fractions import Fraction as F
import json, sys, hashlib

src=sys.argv[1] if len(sys.argv)>1 else '/tmp/mqm_symbolic_results_final.json'
r=json.load(open(src))
terms=['1','p','q','l','p2','pq','pl','q2','ql','l2']

def P(d):
    return {k:F(d[k]) for k in terms}

def coeff(raw,Np,Nq,Nl):
    f0=F(raw['f0']);Sp=F(raw['sp_num15'],15);Sq=F(raw['sq']);Sl=F(raw['sl'])
    Spp=F(raw['pp_num225'],225);Spq=F(raw['pq_num15'],15);Spl=F(raw['pl_num15'],15)
    Sqq=F(raw['qq']);Sql=F(raw['ql']);Sll=F(raw['ll'])
    return {
      '1':f0,
      'p':Sp-Np*f0,'q':Sq-Nq*f0,'l':Sl-Nl*f0,
      'p2':Spp-(Np-1)*Sp+F(Np*(Np-1),2)*f0,
      'pq':Spq-Nq*Sp-Np*Sq+Np*Nq*f0,
      'pl':Spl-Nl*Sp-Np*Sl+Np*Nl*f0,
      'q2':Sqq-(Nq-1)*Sq+F(Nq*(Nq-1),2)*f0,
      'ql':Sql-Nl*Sq-Nq*Sl+Nq*Nl*f0,
      'l2':Sll-(Nl-1)*Sl+F(Nl*(Nl-1),2)*f0,
    }

def sub(a,b):return {k:a[k]-b[k] for k in terms}
def add(a,b):return {k:a[k]+b[k] for k in terms}
def ratio(num,den):
    assert den['1']==1 and num['1']==0
    return {'1':F(0),'p':num['p'],'q':num['q'],'l':num['l'],
      'p2':num['p2']-den['p']*num['p'],
      'pq':num['pq']-den['p']*num['q']-den['q']*num['p'],
      'pl':num['pl']-den['p']*num['l']-den['l']*num['p'],
      'q2':num['q2']-den['q']*num['q'],
      'ql':num['ql']-den['q']*num['l']-den['l']*num['q'],
      'l2':num['l2']-den['l']*num['l']}
def recip_times(den,C):
    assert den['1']==1
    return {'1':F(C),'p':-C*den['p'],'q':-C*den['q'],'l':-C*den['l'],
      'p2':C*(den['p']**2-den['p2']),
      'pq':C*(2*den['p']*den['q']-den['pq']),
      'pl':C*(2*den['p']*den['l']-den['pl']),
      'q2':C*(den['q']**2-den['q2']),
      'ql':C*(2*den['q']*den['l']-den['ql']),
      'l2':C*(den['l']**2-den['l2'])}
def sfrac(x):return str(x.numerator) if x.denominator==1 else f'{x.numerator}/{x.denominator}'
def ser(p):return {k:sfrac(p[k]) for k in terms}

resource={'1+0':(39,14),'2+1':(117,42),'3+1':(156,56)}
report={'version':'0.1','status':'PASS_EXACT_INDEPENDENT_AGGREGATION','source_sha256':hashlib.sha256(open(src,'rb').read()).hexdigest(),'protocols':{}}
for name,d in r['protocols'].items():
    N=d['locations']; polys={}
    for metric,raw in d['raw_aggregates'].items():
        polys[metric]=coeff(raw,N['p'],N['q'],N['l'])
        expected=P(d['polynomials_degree2'][metric])
        assert polys[metric]==expected,(name,metric,polys[metric],expected)
    good=sub(polys['Y'],polys['L_AND_ACCEPT']); eps=ratio(polys['L_AND_ACCEPT'],polys['Y']);r1=ratio(polys['ACCEPT_DW1'],polys['Y'])
    g,m=resource[name];cg=recip_times(good,g);cm=recip_times(good,m)
    for key,val in [('Y_GOOD',good),('EPSILON_L_GIVEN_A',eps),('R1_GIVEN_A',r1),('TWO_QUBIT_GATES_PER_GOOD',cg),('MEASUREMENTS_PER_GOOD',cm)]:
        assert val==P(d['polynomials_degree2'][key]),(name,key)
    partition=add(add(polys['Y'],polys['HOLD']),polys['QUARANTINE'])
    assert partition=={'1':F(1),**{k:F(0) for k in terms[1:]}},(name,'partition')
    report['protocols'][name]={
      'location_counts_match': N==({'1+0':{'p':179,'q':14,'l':102},'2+1':{'p':537,'q':42,'l':306},'3+1':{'p':716,'q':56,'l':408}}[name]),
      'partition_pass':True,
      'metrics_recomputed':{k:ser(v) for k,v in polys.items()},
      'derived':{'Y_GOOD':ser(good),'EPSILON_L_GIVEN_A':ser(eps),'R1_GIVEN_A':ser(r1),'TWO_QUBIT_GATES_PER_GOOD':ser(cg),'MEASUREMENTS_PER_GOOD':ser(cm)}
    }
print(json.dumps(report,indent=2,sort_keys=True))