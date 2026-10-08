#define main mqm_full_tail_hidden_main
#include "2026-10-08T1920Z_mqm_full_stochastic_tail_v01.cpp"
#undef main

struct RatE {
    long long n=0,d=1;
    RatE(){}
    RatE(long long a):n(a),d(1){}
    RatE(long long a,long long b):n(a),d(b){norm();}
    void norm(){if(d<0){d=-d;n=-n;} long long g=std::gcd(n<0?-n:n,d); if(g){n/=g;d/=g;}}
};
RatE operator+(RatE a,RatE b){return RatE(a.n*b.d+b.n*a.d,a.d*b.d);}
RatE operator-(RatE a,RatE b){return RatE(a.n*b.d-b.n*a.d,a.d*b.d);}
RatE operator*(RatE a,RatE b){return RatE(a.n*b.n,a.d*b.d);}
RatE operator*(RatE a,long long b){return RatE(a.n*b,a.d);}
RatE operator*(long long b,RatE a){return a*b;}
string re(const RatE&r){return r.d==1?to_string(r.n):to_string(r.n)+"/"+to_string(r.d);}

struct RoundResE { P data; uint8_t center=0, flags=0, edges=0; };

RoundResE sim_roundE(P data,const Loc*loc,int real){
    auto idle=[&](int bd){
        if(loc&&loc->kind==IDLE&&loc->boundary==bd)
            data=pxor(data,singlep(loc->q,rc3(real)));
    };
    idle(0);
    uint8_t fr=0,fl=0,er=0;

    for(int ci=0;ci<4;ci++){
        P e=data;
        if(loc&&loc->kind==C_SYN_PREP&&loc->ci==ci){
            char c=rc3(real); if(c=='X'||c=='Y') e=pxor(e,singlep(8,'X'));
        }
        if(loc&&loc->kind==C_FLAG_PREP&&loc->ci==ci){
            char c=rc3(real); if(c=='Z'||c=='Y') e=pxor(e,singlep(9,'Z'));
        }
        for(int oi=0;oi<(int)COPS[ci].size();oi++){
            e=applyop(e,COPS[ci][oi]);
            if(loc&&loc->ci==ci&&loc->op==oi){
                if(loc->kind==C_1Q)
                    e=pxor(e,singlep(COPS[ci][oi].a,rc3(real)));
                else if(loc->kind==C_2Q){
                    auto [a,b]=rc15(real);
                    e=pxor(e,pairp(COPS[ci][oi].a,COPS[ci][oi].b,a,b));
                }
            }
        }
        int sb=(e.x>>8)&1, fb=(e.z>>9)&1;
        if(loc&&loc->kind==C_SYN_MEAS&&loc->ci==ci) sb^=1;
        if(loc&&loc->kind==C_FLAG_MEAS&&loc->ci==ci) fb^=1;
        if(sb) fr|=1u<<ci;
        if(fb) fl|=1u<<ci;
        data=extract8(e);
        idle(ci+1);
    }

    for(int ei=0;ei<6;ei++){
        int ci=4+ei;
        P e=data;
        if(loc&&loc->kind==E_SYN_PREP&&loc->ci==ci){
            char c=rc3(real); if(c=='X'||c=='Y') e=pxor(e,singlep(8,'X'));
        }
        array<Op,2> ops={
            Op{2,EDGES[ei].first-1,8},
            Op{2,EDGES[ei].second-1,8}
        };
        for(int oi=0;oi<2;oi++){
            e=applyop(e,ops[oi]);
            if(loc&&loc->kind==E_2Q&&loc->ci==ci&&loc->op==oi){
                auto [a,b]=rc15(real);
                e=pxor(e,pairp(ops[oi].a,ops[oi].b,a,b));
            }
        }
        int eb=(e.x>>8)&1;
        if(loc&&loc->kind==E_MEAS&&loc->ci==ci) eb^=1;
        if(eb) er|=1u<<ei;
        data=extract8(e);
        idle(5+ei);
    }
    return {data,fr,fl,er};
}

struct SigE {
    P data;
    uint64_t centers=0,flags=0,edges=0;
    uint8_t loss=0;
};
struct LSE { Loc loc; vector<SigE> s; };

vector<LSE> build_sigsE(){
    int gid=0; vector<Loc> locs;
    for(int r=0;r<3;r++){
        auto x=build_round(r,gid);
        locs.insert(locs.end(),x.begin(),x.end());
    }
    vector<LSE> out; out.reserve(locs.size());
    for(auto &L:locs){
        LSE a; a.loc=L; a.s.resize(L.rcount);
        for(int rr=0;rr<L.rcount;rr++){
            SigE sg;
            if(L.var==VL){
                sg.loss=(L.kind==DATA_LOSS)?2:1;
                a.s[rr]=sg; continue;
            }
            P data{}; uint64_t c=0,f=0,e=0;
            for(int r=0;r<3;r++){
                auto z=sim_roundE(data,r==L.round?&L:nullptr,rr);
                data=z.data;
                c|=uint64_t(z.center)<<(4*r);
                f|=uint64_t(z.flags)<<(4*r);
                e|=uint64_t(z.edges)<<(6*r);
            }
            sg.data=data; sg.centers=c; sg.flags=f; sg.edges=e;
            a.s[rr]=sg;
        }
        out.push_back(move(a));
    }
    return out;
}

struct CombE {
    P data;
    uint64_t centers=0,flags=0,edges=0;
    uint8_t loss=0;
};
void add_eventE(CombE&c,const LSE&ls,int real){
    const auto&s=ls.s[real];
    c.loss=max(c.loss,s.loss);
    c.data=pxor(c.data,s.data);
    c.centers^=s.centers;
    c.flags^=s.flags;
    c.edges^=s.edges;
}

uint8_t centerE(const CombE&c,int r){return (c.centers>>(4*r))&15u;}
uint8_t flagsE(const CombE&c,int r){return (c.flags>>(4*r))&15u;}
uint8_t edgeE(const CombE&c,int r){return (c.edges>>(6*r))&63u;}

bool edge_valid(uint8_t e){
    auto b=[&](int i){return (e>>i)&1;};
    return ((b(0)^b(1)^b(3))==0) &&
           ((b(0)^b(2)^b(4))==0) &&
           ((b(1)^b(2)^b(5))==0);
}
uint16_t receiptE(const CombE&c,int r){
    return uint16_t(centerE(c,r)) | (uint16_t(edgeE(c,r))<<4);
}
bool pre_reject_2E(const CombE&c){
    if(c.loss) return true;
    return flagsE(c,0)||flagsE(c,1);
}
bool fast_2E(const CombE&c){
    if(pre_reject_2E(c)) return false;
    return edge_valid(edgeE(c,0)) &&
           edge_valid(edgeE(c,1)) &&
           receiptE(c,0)==receiptE(c,1);
}
bool triggers_R3_2E(const CombE&c){
    return !pre_reject_2E(c) && !fast_2E(c);
}

Score classify_2E(const CombE&c){
    Score z;
    if(c.loss==2){z.Q=1;return z;}
    if(c.loss==1){z.H=1;return z;}
    if(flagsE(c,0)||flagsE(c,1)){z.H=1;return z;}

    uint8_t sel=0;
    if(fast_2E(c)){
        sel=centerE(c,0);
    } else {
        if(flagsE(c,2)){z.H=1;return z;}
        bool v3=edge_valid(edgeE(c,2));
        if(!v3){z.H=1;return z;}
        bool v1=edge_valid(edgeE(c,0));
        bool v2=edge_valid(edgeE(c,1));
        uint16_t r3=receiptE(c,2);
        bool m1=v1 && r3==receiptE(c,0);
        bool m2=v2 && r3==receiptE(c,1);
        if(m1==m2){z.H=1;return z;}
        sel=m1?centerE(c,0):centerE(c,1);
    }

    P data=pxor(c.data,DEC[b_to_s(sel)]);
    z.Y=1;
    z.L=LCLASS[pack(data)]!=0;
    z.R1=DRESS[pack(data)]==1;
    z.CLEAN=!z.L&&DRESS[pack(data)]==0;
    z.GOOD=!z.L;
    return z;
}

const int NME=7;
const array<string,NME> MNE={"Y","HOLD","QUARANTINE","L_AND_ACCEPT","ACCEPT_DW1","Y_CLEAN","Y_GOOD"};
array<int,NME> mve(const Score&s){return {s.Y,s.H,s.Q,s.L,s.R1,s.CLEAN,s.GOOD};}

struct RawE {
    long long f0=0,sp15=0,sq=0,sl=0;
    long long tsp15=0,tsq=0,tsl=0;
    long long pp225=0,pq15=0,pl15=0,qq=0,ql=0,ll=0;
    long long op_pp225=0,op_pq15=0,op_pl15=0,op_qq=0,op_ql=0,op_ll=0;
};
struct PolyE { RatE c0,cp,cq,cl,cpp,cpq,cpl,cqq,cql,cll; };

void add_singleE(array<RawE,NME>&A,const Loc&L,const Score&s,bool trig){
    auto m=mve(s);
    for(int k=0;k<NME;k++) if(m[k]){
        if(L.var==VP){A[k].sp15+=15/L.rcount;if(trig)A[k].tsp15+=15/L.rcount;}
        else if(L.var==VQ){A[k].sq++;if(trig)A[k].tsq++;}
        else {A[k].sl++;if(trig)A[k].tsl++;}
    }
}
void add_pair_fieldE(RawE&r,Var a,int rca,Var b,int rcb,bool optional){
    long long *pp=&r.pp225,*pq=&r.pq15,*pl=&r.pl15,*qq=&r.qq,*ql=&r.ql,*ll=&r.ll;
    if(optional){pp=&r.op_pp225;pq=&r.op_pq15;pl=&r.op_pl15;qq=&r.op_qq;ql=&r.op_ql;ll=&r.op_ll;}
    if(a==VP&&b==VP)*pp+=225/(rca*rcb);
    else if((a==VP&&b==VQ)||(a==VQ&&b==VP))*pq+=15/(a==VP?rca:rcb);
    else if((a==VP&&b==VL)||(a==VL&&b==VP))*pl+=15/(a==VP?rca:rcb);
    else if(a==VQ&&b==VQ)(*qq)++;
    else if((a==VQ&&b==VL)||(a==VL&&b==VQ))(*ql)++;
    else if(a==VL&&b==VL)(*ll)++;
}
void add_pairE(array<RawE,NME>&A,const Loc&L1,const Loc&L2,const Score&s,bool optional){
    auto m=mve(s);
    for(int k=0;k<NME;k++)if(m[k])
        add_pair_fieldE(A[k],L1.var,L1.rcount,L2.var,L2.rcount,optional);
}

PolyE coeffE(const RawE&r,int Ap,int Aq,int Al,int Op,int Oq,int Ol){
    RatE f(r.f0),Sp(r.sp15,15),Sq(r.sq),Sl(r.sl),Tp(r.tsp15,15),Tq(r.tsq),Tl(r.tsl);
    RatE Ppp(r.pp225,225),Ppq(r.pq15,15),Ppl(r.pl15,15),Pqq(r.qq),Pql(r.ql),Pll(r.ll);
    RatE Opp(r.op_pp225,225),Opq(r.op_pq15,15),Opl(r.op_pl15,15),Oqq(r.op_qq),Oql(r.op_ql),Oll(r.op_ll);
    PolyE p;
    p.c0=f; p.cp=Sp-Ap*f; p.cq=Sq-Aq*f; p.cl=Sl-Al*f;
    p.cpp=Ppp-(Ap-1)*Sp+RatE(1LL*Ap*(Ap-1)/2)*f-Op*Tp+Opp;
    p.cpq=Ppq-Aq*Sp-Ap*Sq+RatE(1LL*Ap*Aq)*f-Oq*Tp-Op*Tq+Opq;
    p.cpl=Ppl-Al*Sp-Ap*Sl+RatE(1LL*Ap*Al)*f-Ol*Tp-Op*Tl+Opl;
    p.cqq=Pqq-(Aq-1)*Sq+RatE(1LL*Aq*(Aq-1)/2)*f-Oq*Tq+Oqq;
    p.cql=Pql-Al*Sq-Aq*Sl+RatE(1LL*Aq*Al)*f-Ol*Tq-Oq*Tl+Oql;
    p.cll=Pll-(Al-1)*Sl+RatE(1LL*Al*(Al-1)/2)*f-Ol*Tl+Oll;
    return p;
}
PolyE subE(PolyE a,const PolyE&b){
    a.c0=a.c0-b.c0;a.cp=a.cp-b.cp;a.cq=a.cq-b.cq;a.cl=a.cl-b.cl;
    a.cpp=a.cpp-b.cpp;a.cpq=a.cpq-b.cpq;a.cpl=a.cpl-b.cpl;
    a.cqq=a.cqq-b.cqq;a.cql=a.cql-b.cql;a.cll=a.cll-b.cll;
    return a;
}
PolyE ratioE(const PolyE&num,const PolyE&den){
    assert(den.c0.n==1&&den.c0.d==1&&num.c0.n==0);
    PolyE r;
    r.cp=num.cp;r.cq=num.cq;r.cl=num.cl;
    r.cpp=num.cpp-den.cp*num.cp;
    r.cpq=num.cpq-(den.cp*num.cq+den.cq*num.cp);
    r.cpl=num.cpl-(den.cp*num.cl+den.cl*num.cp);
    r.cqq=num.cqq-den.cq*num.cq;
    r.cql=num.cql-(den.cq*num.cl+den.cl*num.cq);
    r.cll=num.cll-den.cl*num.cl;
    return r;
}
string pje(const PolyE&p){
    stringstream o;
    o<<"{\"1\":\""<<re(p.c0)<<"\",\"p\":\""<<re(p.cp)<<"\",\"q\":\""<<re(p.cq)
     <<"\",\"l\":\""<<re(p.cl)<<"\",\"p2\":\""<<re(p.cpp)<<"\",\"pq\":\""<<re(p.cpq)
     <<"\",\"pl\":\""<<re(p.cpl)<<"\",\"q2\":\""<<re(p.cqq)<<"\",\"ql\":\""<<re(p.cql)
     <<"\",\"l2\":\""<<re(p.cll)<<"\"}";
    return o.str();
}

int main(){
    init_code();
    auto all=build_sigsE();
    vector<int> mand,opt;
    for(int i=0;i<(int)all.size();i++){
        if(all[i].loc.round<2) mand.push_back(i);
        else opt.push_back(i);
    }
    int Ap=0,Aq=0,Al=0,Op=0,Oq=0,Ol=0;
    for(int i:mand){if(all[i].loc.var==VP)Ap++;else if(all[i].loc.var==VQ)Aq++;else Al++;}
    for(int i:opt){if(all[i].loc.var==VP)Op++;else if(all[i].loc.var==VQ)Oq++;else Ol++;}
    if(Ap!=358||Aq!=28||Al!=204||Op!=179||Oq!=14||Ol!=102){cerr<<"loc mismatch\n";return 3;}

    array<RawE,NME> agg{};
    CombE zero;
    auto mz=mve(classify_2E(zero));
    for(int k=0;k<NME;k++)agg[k].f0=mz[k];

    long long singles=0,mm=0,mo=0,triggers=0;
    for(int ii:mand){
        auto&A=all[ii];
        for(int ra=0;ra<A.loc.rcount;ra++){
            CombE c; add_eventE(c,A,ra);
            bool tr=triggers_R3_2E(c);
            if(tr)triggers++;
            auto s=classify_2E(c);
            add_singleE(agg,A.loc,s,tr);
            singles++;
        }
    }
    for(size_t ai=0;ai<mand.size();ai++){
        auto&A=all[mand[ai]];
        for(size_t bi=ai+1;bi<mand.size();bi++){
            auto&B=all[mand[bi]];
            for(int ra=0;ra<A.loc.rcount;ra++)for(int rb=0;rb<B.loc.rcount;rb++){
                CombE c;add_eventE(c,A,ra);add_eventE(c,B,rb);
                add_pairE(agg,A.loc,B.loc,classify_2E(c),false);mm++;
            }
        }
    }
    for(int ii:mand){
        auto&A=all[ii];
        for(int ra=0;ra<A.loc.rcount;ra++){
            CombE base;add_eventE(base,A,ra);
            if(!triggers_R3_2E(base))continue;
            for(int jj:opt){
                auto&B=all[jj];
                for(int rb=0;rb<B.loc.rcount;rb++){
                    CombE c=base;add_eventE(c,B,rb);
                    add_pairE(agg,A.loc,B.loc,classify_2E(c),true);mo++;
                }
            }
        }
    }

    array<PolyE,NME> poly;
    for(int k=0;k<NME;k++)poly[k]=coeffE(agg[k],Ap,Aq,Al,Op,Oq,Ol);
    PolyE good=subE(poly[0],poly[3]);
    PolyE eps=ratioE(poly[3],poly[0]);

    auto addp=[](PolyE a,const PolyE&b){
        a.c0=a.c0+b.c0;a.cp=a.cp+b.cp;a.cq=a.cq+b.cq;a.cl=a.cl+b.cl;
        a.cpp=a.cpp+b.cpp;a.cpq=a.cpq+b.cpq;a.cpl=a.cpl+b.cpl;
        a.cqq=a.cqq+b.cqq;a.cql=a.cql+b.cql;a.cll=a.cll+b.cll;return a;
    };
    PolyE part=addp(addp(poly[0],poly[1]),poly[2]);
    if(!(part.c0.n==1&&part.c0.d==1&&part.cp.n==0&&part.cq.n==0&&part.cl.n==0&&
         part.cpp.n==0&&part.cpq.n==0&&part.cpl.n==0&&part.cqq.n==0&&
         part.cql.n==0&&part.cll.n==0)){cerr<<"partition fail\n";return 4;}

    cout<<"{\n"
        <<"  \"version\":\"0.2\",\n"
        <<"  \"status\":\"POSTEXPOSURE_EXACT_DEGREE2_ADAPTIVE_2PLUSE\",\n"
        <<"  \"locations\":{\"mandatory\":{\"p\":"<<Ap<<",\"q\":"<<Aq<<",\"l\":"<<Al
        <<"},\"conditional_R3\":{\"p\":"<<Op<<",\"q\":"<<Oq<<",\"l\":"<<Ol<<"}},\n"
        <<"  \"workload\":{\"single_realizations\":"<<singles<<",\"mandatory_pair_realizations\":"
        <<mm<<",\"trigger_plus_R3_realizations\":"<<mo<<",\"triggering_single_realizations\":"
        <<triggers<<"},\n"
        <<"  \"polynomials_degree2\":{\n";
    for(int k=0;k<NME;k++){
        if(k)cout<<",\n";
        cout<<"    \""<<MNE[k]<<"\":"<<pje(poly[k]);
    }
    cout<<",\n    \"Y_GOOD\":"<<pje(good)
        <<",\n    \"EPSILON_L_GIVEN_A\":"<<pje(eps)
        <<"\n  },\n"
        <<"  \"raw_trigger_single\":{\n";
    for(int k=0;k<NME;k++){
        if(k)cout<<",\n";
        cout<<"    \""<<MNE[k]<<"\":{\"p_num15\":"<<agg[k].tsp15
            <<",\"q\":"<<agg[k].tsq<<",\"l\":"<<agg[k].tsl<<"}";
    }
    cout<<"\n  },\n"
        <<"  \"receipt\":{\"center_bits\":4,\"edge_bits\":6,\"cycle_rank_checks\":3},\n"
        <<"  \"physical_promotion\":0\n"
        <<"}\n";
}
