#define main mqm_full_tail_hidden_main
#include "mqm_full_stochastic_tail_v01.cpp"
#undef main

struct RatX { long long n=0,d=1; RatX(){} RatX(long long a):n(a),d(1){} RatX(long long a,long long b):n(a),d(b){norm();} void norm(){if(d<0){d=-d;n=-n;} long long g=std::gcd(n<0?-n:n,d); if(g){n/=g;d/=g;}}};
RatX operator+(RatX a,RatX b){return RatX(a.n*b.d+b.n*a.d,a.d*b.d);} RatX operator-(RatX a,RatX b){return RatX(a.n*b.d-b.n*a.d,a.d*b.d);} RatX operator*(RatX a,RatX b){return RatX(a.n*b.n,a.d*b.d);} RatX operator*(RatX a,long long b){return RatX(a.n*b,a.d);} RatX operator*(long long b,RatX a){return a*b;} string rx(const RatX&r){return r.d==1?to_string(r.n):to_string(r.n)+"/"+to_string(r.d);} 

const int NM2=7; const array<string,NM2> MN2={"Y","HOLD","QUARANTINE","L_AND_ACCEPT","ACCEPT_DW1","Y_CLEAN","Y_GOOD"};
struct RawA { long long f0=0,sp15=0,sq=0,sl=0,tsp15=0,tsq=0,tsl=0,pp225=0,pq15=0,pl15=0,qq=0,ql=0,ll=0,op_pp225=0,op_pq15=0,op_pl15=0,op_qq=0,op_ql=0,op_ll=0;};
struct PolyA { RatX c0,cp,cq,cl,cpp,cpq,cpl,cqq,cql,cll;};

bool pre_reject12(const Comb&c){ if(c.loss) return true; return (c.acq.flags & 0xffu)!=0; }
bool triggers_R3(const Comb&c){ if(pre_reject12(c)) return false; uint8_t b1=c.acq.frames&15,b2=(c.acq.frames>>4)&15; return b1!=b2; }
Score classify_2C(const Comb&c){
    Score z; if(c.loss==2){z.Q=1;return z;} if(c.loss==1){z.H=1;return z;}
    uint8_t f1=c.acq.frames&15, f2=(c.acq.frames>>4)&15; uint8_t g12=c.acq.flags&0xff;
    if(g12){z.H=1;return z;}
    uint8_t sel=0;
    if(f1==f2) sel=f1;
    else {
        uint8_t f3=(c.acq.frames>>8)&15, g3=(c.acq.flags>>8)&15;
        if(g3){z.H=1;return z;}
        bool m1=f3==f1, m2=f3==f2;
        if(m1==m2){z.H=1;return z;} // neither or pathological both when f1!=f2
        sel=m1?f1:f2;
    }
    P data=pxor(c.acq.data,DEC[b_to_s(sel)]);
    z.Y=1; z.L=LCLASS[pack(data)]!=0; z.R1=DRESS[pack(data)]==1; z.CLEAN=!z.L&&DRESS[pack(data)]==0; z.GOOD=!z.L; return z;
}
array<int,NM2> mva(const Score&s){return {s.Y,s.H,s.Q,s.L,s.R1,s.CLEAN,s.GOOD};}

void add_singleA(array<RawA,NM2>&A,const Loc&L,const Score&s,bool trig){auto m=mva(s);for(int k=0;k<NM2;k++)if(m[k]){if(L.var==VP){A[k].sp15+=15/L.rcount;if(trig)A[k].tsp15+=15/L.rcount;} else if(L.var==VQ){A[k].sq++;if(trig)A[k].tsq++;} else {A[k].sl++;if(trig)A[k].tsl++;}}}
void add_pair_field(RawA&r,Var a,int rca,Var b,int rcb,bool optional){
    long long *pp=&r.pp225,*pq=&r.pq15,*pl=&r.pl15,*qq=&r.qq,*ql=&r.ql,*ll=&r.ll;
    if(optional){pp=&r.op_pp225;pq=&r.op_pq15;pl=&r.op_pl15;qq=&r.op_qq;ql=&r.op_ql;ll=&r.op_ll;}
    if(a==VP&&b==VP)*pp+=225/(rca*rcb);
    else if((a==VP&&b==VQ)||(a==VQ&&b==VP))*pq+=15/(a==VP?rca:rcb);
    else if((a==VP&&b==VL)||(a==VL&&b==VP))*pl+=15/(a==VP?rca:rcb);
    else if(a==VQ&&b==VQ)(*qq)++;
    else if((a==VQ&&b==VL)||(a==VL&&b==VQ))(*ql)++;
    else if(a==VL&&b==VL)(*ll)++;
}
void add_pairA(array<RawA,NM2>&A,const Loc&L1,const Loc&L2,const Score&s,bool optional){auto m=mva(s);for(int k=0;k<NM2;k++)if(m[k])add_pair_field(A[k],L1.var,L1.rcount,L2.var,L2.rcount,optional);}

PolyA coeffA(const RawA&r,int Ap,int Aq,int Al,int Op,int Oq,int Ol){
    RatX f(r.f0),Sp(r.sp15,15),Sq(r.sq),Sl(r.sl),Tp(r.tsp15,15),Tq(r.tsq),Tl(r.tsl);
    RatX Ppp(r.pp225,225),Ppq(r.pq15,15),Ppl(r.pl15,15),Pqq(r.qq),Pql(r.ql),Pll(r.ll);
    RatX Opp(r.op_pp225,225),Opq(r.op_pq15,15),Opl(r.op_pl15,15),Oqq(r.op_qq),Oql(r.op_ql),Oll(r.op_ll);
    PolyA p; p.c0=f;p.cp=Sp-Ap*f;p.cq=Sq-Aq*f;p.cl=Sl-Al*f;
    p.cpp=Ppp-(Ap-1)*Sp+RatX(1LL*Ap*(Ap-1)/2)*f-Op*Tp+Opp;
    p.cpq=Ppq-Aq*Sp-Ap*Sq+RatX(1LL*Ap*Aq)*f-Oq*Tp-Op*Tq+Opq;
    p.cpl=Ppl-Al*Sp-Ap*Sl+RatX(1LL*Ap*Al)*f-Ol*Tp-Op*Tl+Opl;
    p.cqq=Pqq-(Aq-1)*Sq+RatX(1LL*Aq*(Aq-1)/2)*f-Oq*Tq+Oqq;
    p.cql=Pql-Al*Sq-Aq*Sl+RatX(1LL*Aq*Al)*f-Ol*Tq-Oq*Tl+Oql;
    p.cll=Pll-(Al-1)*Sl+RatX(1LL*Al*(Al-1)/2)*f-Ol*Tl+Oll;
    return p;
}
PolyA subA(PolyA a,const PolyA&b){a.c0=a.c0-b.c0;a.cp=a.cp-b.cp;a.cq=a.cq-b.cq;a.cl=a.cl-b.cl;a.cpp=a.cpp-b.cpp;a.cpq=a.cpq-b.cpq;a.cpl=a.cpl-b.cpl;a.cqq=a.cqq-b.cqq;a.cql=a.cql-b.cql;a.cll=a.cll-b.cll;return a;}
PolyA ratioA(const PolyA&num,const PolyA&den){assert(den.c0.n==1&&den.c0.d==1&&num.c0.n==0);PolyA r;r.cp=num.cp;r.cq=num.cq;r.cl=num.cl;r.cpp=num.cpp-den.cp*num.cp;r.cpq=num.cpq-(den.cp*num.cq+den.cq*num.cp);r.cpl=num.cpl-(den.cp*num.cl+den.cl*num.cp);r.cqq=num.cqq-den.cq*num.cq;r.cql=num.cql-(den.cq*num.cl+den.cl*num.cq);r.cll=num.cll-den.cl*num.cl;return r;}
string pj(const PolyA&p){stringstream o;o<<"{\"1\":\""<<rx(p.c0)<<"\",\"p\":\""<<rx(p.cp)<<"\",\"q\":\""<<rx(p.cq)<<"\",\"l\":\""<<rx(p.cl)<<"\",\"p2\":\""<<rx(p.cpp)<<"\",\"pq\":\""<<rx(p.cpq)<<"\",\"pl\":\""<<rx(p.cpl)<<"\",\"q2\":\""<<rx(p.cqq)<<"\",\"ql\":\""<<rx(p.cql)<<"\",\"l2\":\""<<rx(p.cll)<<"\"}";return o.str();}

int main(){
    init_code(); auto all=build_sigs(3,0); vector<int> mand,opt; for(int i=0;i<(int)all.size();i++){if(all[i].loc.round<2)mand.push_back(i); else opt.push_back(i);} int Ap=0,Aq=0,Al=0,Op=0,Oq=0,Ol=0; for(int i:mand){if(all[i].loc.var==VP)Ap++;else if(all[i].loc.var==VQ)Aq++;else Al++;}for(int i:opt){if(all[i].loc.var==VP)Op++;else if(all[i].loc.var==VQ)Oq++;else Ol++;}
    if(Ap!=358||Aq!=28||Al!=204||Op!=179||Oq!=14||Ol!=102){cerr<<"loc mismatch\n";return 3;}
    array<RawA,NM2> agg{}; Comb zero; auto mz=mva(classify_2C(zero));for(int k=0;k<NM2;k++)agg[k].f0=mz[k];
    long long single_real=0,pair_mm_real=0,pair_mo_real=0,trigger_real=0;
    // mandatory singles
    for(int ii:mand){auto&A=all[ii];for(int ra=0;ra<A.loc.rcount;ra++){Comb c;add_event(c,A,ra,3);bool tr=triggers_R3(c);if(tr)trigger_real++;Score s=classify_2C(c);add_singleA(agg,A.loc,s,tr);single_real++;}}
    // mandatory-mandatory pairs
    for(size_t ai=0;ai<mand.size();ai++){auto&A=all[mand[ai]];for(size_t bi=ai+1;bi<mand.size();bi++){auto&B=all[mand[bi]];for(int ra=0;ra<A.loc.rcount;ra++)for(int rb=0;rb<B.loc.rcount;rb++){Comb c;add_event(c,A,ra,3);add_event(c,B,rb,3);Score s=classify_2C(c);add_pairA(agg,A.loc,B.loc,s,false);pair_mm_real++;}}}
    // triggering mandatory single + optional R3 event
    for(int ii:mand){auto&A=all[ii];for(int ra=0;ra<A.loc.rcount;ra++){Comb base;add_event(base,A,ra,3);if(!triggers_R3(base))continue;for(int jj:opt){auto&B=all[jj];for(int rb=0;rb<B.loc.rcount;rb++){Comb c=base;add_event(c,B,rb,3);Score s=classify_2C(c);add_pairA(agg,A.loc,B.loc,s,true);pair_mo_real++;}}}}
    array<PolyA,NM2> poly;for(int k=0;k<NM2;k++)poly[k]=coeffA(agg[k],Ap,Aq,Al,Op,Oq,Ol);PolyA good=subA(poly[0],poly[3]);PolyA eps=ratioA(poly[3],poly[0]);
    // exact partition check
    auto addp=[](PolyA a,const PolyA&b){a.c0=a.c0+b.c0;a.cp=a.cp+b.cp;a.cq=a.cq+b.cq;a.cl=a.cl+b.cl;a.cpp=a.cpp+b.cpp;a.cpq=a.cpq+b.cpq;a.cpl=a.cpl+b.cpl;a.cqq=a.cqq+b.cqq;a.cql=a.cql+b.cql;a.cll=a.cll+b.cll;return a;};PolyA part=addp(addp(poly[0],poly[1]),poly[2]);if(!(part.c0.n==1&&part.cp.n==0&&part.cq.n==0&&part.cl.n==0&&part.cpp.n==0&&part.cpq.n==0&&part.cpl.n==0&&part.cqq.n==0&&part.cql.n==0&&part.cll.n==0)){cerr<<"partition fail\n";return 4;}
    ofstream out("/mnt/data/mqm_full/MQM_2PLUSC_EXACT_RESULTS_v0.1.json");out<<"{\n  \"version\":\"0.1\",\n  \"status\":\"POSTEXPOSURE_EXACT_DEGREE2_ADAPTIVE_2PLUSC\",\n  \"locations\":{\"mandatory\":{\"p\":"<<Ap<<",\"q\":"<<Aq<<",\"l\":"<<Al<<"},\"conditional_R3\":{\"p\":"<<Op<<",\"q\":"<<Oq<<",\"l\":"<<Ol<<"}},\n  \"workload\":{\"single_realizations\":"<<single_real<<",\"mandatory_pair_realizations\":"<<pair_mm_real<<",\"trigger_plus_R3_realizations\":"<<pair_mo_real<<",\"triggering_single_realizations\":"<<trigger_real<<"},\n  \"polynomials_degree2\":{\n";for(int k=0;k<NM2;k++){if(k)out<<",\n";out<<"    \""<<MN2[k]<<"\":"<<pj(poly[k]);}out<<",\n    \"Y_GOOD\":"<<pj(good)<<",\n    \"EPSILON_L_GIVEN_A\":"<<pj(eps)<<"\n  },\n  \"raw_trigger_single\":{\n";for(int k=0;k<NM2;k++){if(k)out<<",\n";out<<"    \""<<MN2[k]<<"\":{\"p_num15\":"<<agg[k].tsp15<<",\"q\":"<<agg[k].tsq<<",\"l\":"<<agg[k].tsl<<"}";}out<<"\n  },\n  \"physical_promotion\":0\n}\n";out.close();cerr<<"done 2+C exact\n";
}