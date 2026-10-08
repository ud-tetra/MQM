#define main mqm_full_tail_hidden_main
#include "2026-10-08T1920Z_mqm_full_stochastic_tail_v01.cpp"
#undef main

struct RatV {
    long long n=0,d=1;
    RatV(){}
    RatV(long long a):n(a),d(1){}
    RatV(long long a,long long b):n(a),d(b){norm();}
    void norm(){if(d<0){d=-d;n=-n;} long long g=std::gcd(n<0?-n:n,d); if(g){n/=g;d/=g;}}
};
RatV operator+(RatV a,RatV b){return RatV(a.n*b.d+b.n*a.d,a.d*b.d);}
RatV operator-(RatV a,RatV b){return RatV(a.n*b.d-b.n*a.d,a.d*b.d);}
RatV operator*(RatV a,RatV b){return RatV(a.n*b.n,a.d*b.d);}
RatV operator*(RatV a,long long b){return RatV(a.n*b,a.d);}
RatV operator*(long long b,RatV a){return a*b;}
string rv(const RatV&r){return r.d==1?to_string(r.n):to_string(r.n)+"/"+to_string(r.d);}

const int NMV=7;
const array<string,NMV> MNV={"Y","HOLD","QUARANTINE","L_AND_ACCEPT","ACCEPT_DW1","Y_CLEAN","Y_GOOD"};

bool trigger_verify(const Comb&c){
    if(c.loss) return false;
    if(c.acq.flags) return false;
    uint8_t b1=c.acq.frames&15, b2=(c.acq.frames>>4)&15;
    return b1==b2 && b1!=0;
}

Score classify_2PV(const Comb&c){
    Score z;
    if(c.loss==2){z.Q=1;return z;}
    if(c.loss==1){z.H=1;return z;}
    if(c.acq.flags){z.H=1;return z;}
    uint8_t b1=c.acq.frames&15,b2=(c.acq.frames>>4)&15;
    if(b1!=b2){z.H=1;return z;}
    uint8_t sel=b1;
    P data=pxor(c.acq.data,DEC[b_to_s(sel)]);
    if(sel!=0){
        if(c.ver.flags){z.H=1;return z;}
        uint8_t obs=CSYN[pack(data)]^(c.ver.frames&15);
        if(obs){z.H=1;return z;}
        data=pxor(data,c.ver.data);
    }
    z.Y=1; z.L=LCLASS[pack(data)]!=0; z.R1=DRESS[pack(data)]==1;
    z.CLEAN=!z.L&&DRESS[pack(data)]==0; z.GOOD=!z.L;
    return z;
}
array<int,NMV> mvv(const Score&s){return {s.Y,s.H,s.Q,s.L,s.R1,s.CLEAN,s.GOOD};}

struct RawV {
    long long f0=0,sp15=0,sq=0,sl=0;
    long long tsp15=0,tsq=0,tsl=0;
    long long pp225=0,pq15=0,pl15=0,qq=0,ql=0,ll=0;
    long long op_pp225=0,op_pq15=0,op_pl15=0,op_qq=0,op_ql=0,op_ll=0;
};
struct PolyV { RatV c0,cp,cq,cl,cpp,cpq,cpl,cqq,cql,cll; };

void add_singleV(array<RawV,NMV>&A,const Loc&L,const Score&s,bool trig){
    auto m=mvv(s);
    for(int k=0;k<NMV;k++)if(m[k]){
        if(L.var==VP){A[k].sp15+=15/L.rcount;if(trig)A[k].tsp15+=15/L.rcount;}
        else if(L.var==VQ){A[k].sq++;if(trig)A[k].tsq++;}
        else {A[k].sl++;if(trig)A[k].tsl++;}
    }
}
void pairfieldV(RawV&r,Var a,int rca,Var b,int rcb,bool optional){
    long long *pp=&r.pp225,*pq=&r.pq15,*pl=&r.pl15,*qq=&r.qq,*ql=&r.ql,*ll=&r.ll;
    if(optional){pp=&r.op_pp225;pq=&r.op_pq15;pl=&r.op_pl15;qq=&r.op_qq;ql=&r.op_ql;ll=&r.op_ll;}
    if(a==VP&&b==VP)*pp+=225/(rca*rcb);
    else if((a==VP&&b==VQ)||(a==VQ&&b==VP))*pq+=15/(a==VP?rca:rcb);
    else if((a==VP&&b==VL)||(a==VL&&b==VP))*pl+=15/(a==VP?rca:rcb);
    else if(a==VQ&&b==VQ)(*qq)++;
    else if((a==VQ&&b==VL)||(a==VL&&b==VQ))(*ql)++;
    else if(a==VL&&b==VL)(*ll)++;
}
void add_pairV(array<RawV,NMV>&A,const Loc&L1,const Loc&L2,const Score&s,bool optional){
    auto m=mvv(s); for(int k=0;k<NMV;k++)if(m[k])pairfieldV(A[k],L1.var,L1.rcount,L2.var,L2.rcount,optional);
}
PolyV coeffV(const RawV&r,int Ap,int Aq,int Al,int Op,int Oq,int Ol){
    RatV f(r.f0),Sp(r.sp15,15),Sq(r.sq),Sl(r.sl),Tp(r.tsp15,15),Tq(r.tsq),Tl(r.tsl);
    RatV Ppp(r.pp225,225),Ppq(r.pq15,15),Ppl(r.pl15,15),Pqq(r.qq),Pql(r.ql),Pll(r.ll);
    RatV Opp(r.op_pp225,225),Opq(r.op_pq15,15),Opl(r.op_pl15,15),Oqq(r.op_qq),Oql(r.op_ql),Oll(r.op_ll);
    PolyV p;
    p.c0=f;p.cp=Sp-Ap*f;p.cq=Sq-Aq*f;p.cl=Sl-Al*f;
    p.cpp=Ppp-(Ap-1)*Sp+RatV(1LL*Ap*(Ap-1)/2)*f-Op*Tp+Opp;
    p.cpq=Ppq-Aq*Sp-Ap*Sq+RatV(1LL*Ap*Aq)*f-Oq*Tp-Op*Tq+Opq;
    p.cpl=Ppl-Al*Sp-Ap*Sl+RatV(1LL*Ap*Al)*f-Ol*Tp-Op*Tl+Opl;
    p.cqq=Pqq-(Aq-1)*Sq+RatV(1LL*Aq*(Aq-1)/2)*f-Oq*Tq+Oqq;
    p.cql=Pql-Al*Sq-Aq*Sl+RatV(1LL*Aq*Al)*f-Ol*Tq-Oq*Tl+Oql;
    p.cll=Pll-(Al-1)*Sl+RatV(1LL*Al*(Al-1)/2)*f-Ol*Tl+Oll;
    return p;
}
PolyV subV(PolyV a,const PolyV&b){
    a.c0=a.c0-b.c0;a.cp=a.cp-b.cp;a.cq=a.cq-b.cq;a.cl=a.cl-b.cl;
    a.cpp=a.cpp-b.cpp;a.cpq=a.cpq-b.cpq;a.cpl=a.cpl-b.cpl;a.cqq=a.cqq-b.cqq;
    a.cql=a.cql-b.cql;a.cll=a.cll-b.cll;return a;
}
PolyV ratioV(const PolyV&num,const PolyV&den){
    assert(den.c0.n==1&&den.c0.d==1&&num.c0.n==0);
    PolyV r;r.cp=num.cp;r.cq=num.cq;r.cl=num.cl;
    r.cpp=num.cpp-den.cp*num.cp;
    r.cpq=num.cpq-(den.cp*num.cq+den.cq*num.cp);
    r.cpl=num.cpl-(den.cp*num.cl+den.cl*num.cp);
    r.cqq=num.cqq-den.cq*num.cq;
    r.cql=num.cql-(den.cq*num.cl+den.cl*num.cq);
    r.cll=num.cll-den.cl*num.cl;
    return r;
}
string pjv(const PolyV&p){
    stringstream o;o<<"{\"1\":\""<<rv(p.c0)<<"\",\"p\":\""<<rv(p.cp)<<"\",\"q\":\""<<rv(p.cq)
    <<"\",\"l\":\""<<rv(p.cl)<<"\",\"p2\":\""<<rv(p.cpp)<<"\",\"pq\":\""<<rv(p.cpq)
    <<"\",\"pl\":\""<<rv(p.cpl)<<"\",\"q2\":\""<<rv(p.cqq)<<"\",\"ql\":\""<<rv(p.cql)
    <<"\",\"l2\":\""<<rv(p.cll)<<"\"}";return o.str();
}

int main(){
    init_code();
    auto all=build_sigs(2,1);
    vector<int> mand,opt;
    for(int i=0;i<(int)all.size();i++){ if(all[i].loc.round<2)mand.push_back(i); else opt.push_back(i); }
    int Ap=0,Aq=0,Al=0,Op=0,Oq=0,Ol=0;
    for(int i:mand){if(all[i].loc.var==VP)Ap++;else if(all[i].loc.var==VQ)Aq++;else Al++;}
    for(int i:opt){if(all[i].loc.var==VP)Op++;else if(all[i].loc.var==VQ)Oq++;else Ol++;}
    if(Ap!=358||Aq!=28||Al!=204||Op!=179||Oq!=14||Ol!=102){cerr<<"loc mismatch\n";return 3;}

    array<RawV,NMV> agg{};
    Comb zero;auto m0=mvv(classify_2PV(zero));for(int k=0;k<NMV;k++)agg[k].f0=m0[k];
    long long single=0,mm=0,mo=0,tr=0;

    for(int ii:mand){
        auto&A=all[ii];
        for(int ra=0;ra<A.loc.rcount;ra++){
            Comb c;add_event(c,A,ra,2);
            bool t=trigger_verify(c);if(t)tr++;
            add_singleV(agg,A.loc,classify_2PV(c),t);single++;
        }
    }
    for(size_t ai=0;ai<mand.size();ai++){
        auto&A=all[mand[ai]];
        for(size_t bi=ai+1;bi<mand.size();bi++){
            auto&B=all[mand[bi]];
            for(int ra=0;ra<A.loc.rcount;ra++)for(int rb=0;rb<B.loc.rcount;rb++){
                Comb c;add_event(c,A,ra,2);add_event(c,B,rb,2);
                add_pairV(agg,A.loc,B.loc,classify_2PV(c),false);mm++;
            }
        }
    }
    for(int ii:mand){
        auto&A=all[ii];
        for(int ra=0;ra<A.loc.rcount;ra++){
            Comb base;add_event(base,A,ra,2);
            if(!trigger_verify(base))continue;
            for(int jj:opt){
                auto&B=all[jj];
                for(int rb=0;rb<B.loc.rcount;rb++){
                    Comb c=base;add_event(c,B,rb,2);
                    add_pairV(agg,A.loc,B.loc,classify_2PV(c),true);mo++;
                }
            }
        }
    }

    array<PolyV,NMV> poly;for(int k=0;k<NMV;k++)poly[k]=coeffV(agg[k],Ap,Aq,Al,Op,Oq,Ol);
    PolyV good=subV(poly[0],poly[3]);PolyV eps=ratioV(poly[3],poly[0]);
    auto addp=[](PolyV a,const PolyV&b){a.c0=a.c0+b.c0;a.cp=a.cp+b.cp;a.cq=a.cq+b.cq;a.cl=a.cl+b.cl;a.cpp=a.cpp+b.cpp;a.cpq=a.cpq+b.cpq;a.cpl=a.cpl+b.cpl;a.cqq=a.cqq+b.cqq;a.cql=a.cql+b.cql;a.cll=a.cll+b.cll;return a;};
    PolyV part=addp(addp(poly[0],poly[1]),poly[2]);
    if(!(part.c0.n==1&&part.c0.d==1&&part.cp.n==0&&part.cq.n==0&&part.cl.n==0&&part.cpp.n==0&&part.cpq.n==0&&part.cpl.n==0&&part.cqq.n==0&&part.cql.n==0&&part.cll.n==0)){cerr<<"partition fail\n";return 4;}

    cout<<"{\n  \"version\":\"0.3\",\n  \"status\":\"POSTEXPOSURE_EXACT_DEGREE2_ADAPTIVE_2PLUSPV\",\n";
    cout<<"  \"locations\":{\"mandatory\":{\"p\":"<<Ap<<",\"q\":"<<Aq<<",\"l\":"<<Al<<"},\"conditional_verify\":{\"p\":"<<Op<<",\"q\":"<<Oq<<",\"l\":"<<Ol<<"}},\n";
    cout<<"  \"workload\":{\"single_realizations\":"<<single<<",\"mandatory_pair_realizations\":"<<mm<<",\"trigger_plus_verify_realizations\":"<<mo<<",\"triggering_single_realizations\":"<<tr<<"},\n";
    cout<<"  \"polynomials_degree2\":{\n";
    for(int k=0;k<NMV;k++){if(k)cout<<",\n";cout<<"    \""<<MNV[k]<<"\":"<<pjv(poly[k]);}
    cout<<",\n    \"Y_GOOD\":"<<pjv(good)<<",\n    \"EPSILON_L_GIVEN_A\":"<<pjv(eps)<<"\n  },\n";
    cout<<"  \"raw_trigger_single\":{\n";
    for(int k=0;k<NMV;k++){if(k)cout<<",\n";cout<<"    \""<<MNV[k]<<"\":{\"p_num15\":"<<agg[k].tsp15<<",\"q\":"<<agg[k].tsq<<",\"l\":"<<agg[k].tsl<<"}";}
    cout<<"\n  },\n  \"physical_promotion\":0\n}\n";
}
