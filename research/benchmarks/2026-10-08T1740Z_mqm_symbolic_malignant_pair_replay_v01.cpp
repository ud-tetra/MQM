#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <numeric>
#include <sstream>
#include <string>
#include <tuple>
#include <unordered_set>
#include <vector>
using namespace std;

struct Rat {
    long long n=0,d=1;
    Rat(){}
    Rat(long long a):n(a),d(1){}
    Rat(long long a,long long b):n(a),d(b){ norm(); }
    void norm(){ if(d<0){d=-d;n=-n;} long long g=std::gcd(n<0?-n:n,d); if(g){n/=g;d/=g;} }
};
Rat operator+(Rat a,Rat b){ return Rat(a.n*b.d+b.n*a.d,a.d*b.d); }
Rat operator-(Rat a,Rat b){ return Rat(a.n*b.d-b.n*a.d,a.d*b.d); }
Rat operator*(Rat a,Rat b){ return Rat(a.n*b.n,a.d*b.d); }
Rat operator*(Rat a,long long b){ return Rat(a.n*b,a.d); }
Rat operator*(long long b,Rat a){ return a*b; }
string rs(const Rat&r){ if(r.d==1)return to_string(r.n); return to_string(r.n)+"/"+to_string(r.d); }

uint32_t pv(const string&s){
    uint32_t x=0,z=0; int n=s.size();
    for(int i=0;i<n;i++){ char c=s[i]; if(c=='X'||c=='Y')x|=(1u<<i); if(c=='Z'||c=='Y')z|=(1u<<i); }
    return x | (z<<n);
}
pair<uint32_t,uint32_t> splitp(uint32_t v,int n){ uint32_t m=(1u<<n)-1; return {uint32_t(v&m),uint32_t((v>>n)&m)}; }
int wt(uint32_t v,int n){ auto [x,z]=splitp(v,n); return __builtin_popcount((unsigned)(x|z)); }
int symp(uint32_t a,uint32_t b,int n){ auto [ax,az]=splitp(a,n); auto [bx,bz]=splitp(b,n); return (__builtin_popcount((unsigned)(ax&bz))+__builtin_popcount((unsigned)(az&bx)))&1; }
uint32_t H(uint32_t v,int q,int n){ auto [x,z]=splitp(v,n); int xb=(x>>q)&1,zb=(z>>q)&1; if(xb!=zb){x^=1u<<q;z^=1u<<q;} return x|(z<<n); }
uint32_t Sg(uint32_t v,int q,int n){ auto [x,z]=splitp(v,n); if((x>>q)&1)z^=1u<<q; return x|(z<<n); }
uint32_t CNOT(uint32_t v,int c,int t,int n){ auto [x,z]=splitp(v,n); if((x>>c)&1)x^=1u<<t; if((z>>t)&1)z^=1u<<c; return x|(z<<n); }
uint32_t singlep(int q,char p,int n){ uint32_t x=0,z=0; if(p=='X'||p=='Y')x|=1u<<q; if(p=='Z'||p=='Y')z|=1u<<q; return x|(z<<n); }
uint32_t pairp(int a,int b,char pa,char pb,int n){ return singlep(a,pa,n)^singlep(b,pb,n); }
uint32_t embed8(uint32_t v8,int n){ auto [x,z]=splitp(v8,8); return x|(z<<n); }
uint32_t extract8(uint32_t v,int n){ auto [x,z]=splitp(v,n); return (x&0xffu)|((z&0xffu)<<8); }

struct Op { int type; int a,b; }; // 0 H,1 S,2 CNOT
const array<string,4> CHECKS={"IIIXXZZI","IIIZZYYI","IIIYIYZZ","XXXXYYIX"};
const array<vector<int>,4> ORDERS={vector<int>{4,5,6,7},vector<int>{4,5,6,7},vector<int>{4,6,7,8},vector<int>{4,5,6,1,2,3,8}};
const array<pair<int,int>,6> EDGES={pair<int,int>{1,2},{1,3},{1,8},{2,3},{2,8},{3,8}};
vector<Op> center_ops(int ci){
    vector<Op> o; string c=CHECKS[ci];
    for(int q=0;q<8;q++){ if(c[q]=='X')o.push_back({0,q,0}); else if(c[q]=='Y'){o.push_back({1,q,0});o.push_back({0,q,0});} }
    int k=0; for(int d:ORDERS[ci]){ o.push_back({2,d-1,8}); k++; if(k==1||k==3)o.push_back({2,9,8}); }
    for(int q=7;q>=0;q--){ if(c[q]=='X')o.push_back({0,q,0}); else if(c[q]=='Y'){o.push_back({0,q,0});o.push_back({1,q,0});} }
    return o;
}
array<vector<Op>,4> COPS={center_ops(0),center_ops(1),center_ops(2),center_ops(3)};
uint32_t applyop(uint32_t e,const Op&o,int n){ if(o.type==0)return H(e,o.a,n); if(o.type==1)return Sg(e,o.a,n); return CNOT(e,o.a,o.b,n); }

// Frozen source algebra.
array<uint32_t,4> OLDST={pv("IIIXXZZI"),pv("IIIYIYZZ"),pv("IIIXZIXZ"),pv("XXXXYYIX")};
array<uint32_t,4> CANDST={pv("IIIXXZZI"),pv("IIIZZYYI"),pv("IIIYIYZZ"),pv("XXXXYYIX")};
array<string,16> DECSTR={
    "IIIIIIII", // 0000
    "IIIIIYII", // 1000
    "IIIXIIII", // 0100
    "IIIIIIXI", // 1100
    "IIIIIIZI", // 0010
    "IIIIYIII", // 1010
    "IIIIIIIX", // 0110
    "IIIIIIYI", // 1110
    "IIIIIIIZ", // 0001
    "IIIIZIII", // 1001
    "IIIIIZII", // 0101
    "IIIIIXII", // 1101
    "IIIIXIII", // 0011
    "IIIYIIII", // 1011
    "IIIIIIIY", // 0111
    "IIIZIIII"  // 1111
};
array<uint32_t,16> DECODER;
vector<uint32_t> GAUGE;
unordered_set<uint32_t> GSET;
uint32_t LX=pv("IIIYZIZI"),LZ=pv("IIIXIZIZ");
array<uint8_t,65536> OSYN,CSYN,DRESS,LCLASS;
int b_to_s(int b){ int b1=b&1,b2=(b>>1)&1,b3=(b>>2)&1,b4=(b>>3)&1; int s1=b1,s2=b3,s3=b2^b3,s4=b4; return s1|(s2<<1)|(s3<<2)|(s4<<3); }
void init_code(){
    for(int i=0;i<16;i++) DECODER[i]=pv(DECSTR[i]);
    vector<string> gs={"IIIXXZZI","IIIYIYZZ","IIIXZIXZ","XXXXYYIX","XIIIIIII","ZIIIIIIZ","IXIIIIII","IZIIIIIZ","IIXIIIII","IIZIIIIZ"};
    GAUGE={0};
    for(auto&s:gs){ uint32_t g=pv(s); size_t z=GAUGE.size(); for(size_t i=0;i<z;i++)GAUGE.push_back(GAUGE[i]^g); }
    sort(GAUGE.begin(),GAUGE.end()); GAUGE.erase(unique(GAUGE.begin(),GAUGE.end()),GAUGE.end());
    for(auto g:GAUGE)GSET.insert(g);
    for(int v=0;v<65536;v++){
        int os=0,cs=0; for(int i=0;i<4;i++){os|=symp(v,OLDST[i],8)<<i;cs|=symp(v,CANDST[i],8)<<i;} OSYN[v]=os;CSYN[v]=cs;
        int d=9; for(auto g:GAUGE)d=min(d,wt(v^g,8)); DRESS[v]=d;
        uint32_t r=v^DECODER[os]; uint8_t lc=255; array<pair<uint8_t,uint32_t>,4> ls={pair<uint8_t,uint32_t>{0,0},{1,LX},{2,LZ},{3,uint32_t(LX^LZ)}};
        for(auto [nm,l]:ls)if(GSET.count(r^l)){lc=nm;break;} if(lc==255){cerr<<"bad logical class\n";exit(2);} LCLASS[v]=lc;
    }
    for(int b=0;b<16;b++){ // candidate-to-old syndrome exact map check on all Paulis below
        (void)b;
    }
    for(int v=0;v<65536;v++) if(b_to_s(CSYN[v])!=OSYN[v]){cerr<<"syndrome map fail\n";exit(2);} 
}

// Location kinds.
enum Var{VP,VQ,VL};
enum Kind{C_SYN_PREP,C_FLAG_PREP,C_1Q,C_2Q,E_SYN_PREP,E_2Q,IDLE,C_SYN_MEAS,C_FLAG_MEAS,E_MEAS,DATA_LOSS,C_SYN_LOSS,C_FLAG_LOSS,E_SYN_LOSS};
struct Loc{ int id,round; Var var; Kind kind; int ci=-1,op=-1,q=-1,boundary=-1; int rcount=1; bool p2=false; string label; };

vector<Loc> build_round_locs(int round,int &gid){
    vector<Loc> L;
    auto add=[&](Var v,Kind k,int ci,int op,int q,int bd,int rc,bool p2,string lab){L.push_back({gid++,round,v,k,ci,op,q,bd,rc,p2,lab});};
    // boundary 0 idle + data loss
    for(int q=0;q<8;q++){add(VP,IDLE,-1,-1,q,0,3,false,"idle_pre_B1_q"+to_string(q+1));add(VL,DATA_LOSS,-1,-1,q,0,1,false,"loss_pre_B1_q"+to_string(q+1));}
    for(int ci=0;ci<4;ci++){
        add(VP,C_SYN_PREP,ci,-1,-1,-1,3,false,"B"+to_string(ci+1)+"_syn_prep");
        add(VP,C_FLAG_PREP,ci,-1,-1,-1,3,false,"B"+to_string(ci+1)+"_flag_prep");
        auto &ops=COPS[ci];
        for(int oi=0;oi<(int)ops.size();oi++){
            if(ops[oi].type==2)add(VP,C_2Q,ci,oi,-1,-1,15,true,"B"+to_string(ci+1)+"_2q_"+to_string(oi));
            else add(VP,C_1Q,ci,oi,-1,-1,3,false,"B"+to_string(ci+1)+"_1q_"+to_string(oi));
        }
        add(VL,C_SYN_LOSS,ci,-1,-1,-1,1,false,"B"+to_string(ci+1)+"_syn_loss");
        add(VL,C_FLAG_LOSS,ci,-1,-1,-1,1,false,"B"+to_string(ci+1)+"_flag_loss");
        add(VQ,C_SYN_MEAS,ci,-1,-1,-1,1,false,"B"+to_string(ci+1)+"_syn_q");
        add(VQ,C_FLAG_MEAS,ci,-1,-1,-1,1,false,"B"+to_string(ci+1)+"_flag_q");
        int bd=ci+1; for(int q=0;q<8;q++){add(VP,IDLE,-1,-1,q,bd,3,false,"idle_b"+to_string(bd)+"_q"+to_string(q+1));add(VL,DATA_LOSS,-1,-1,q,bd,1,false,"loss_b"+to_string(bd)+"_q"+to_string(q+1));}
    }
    for(int ei=0;ei<6;ei++){
        int ci=4+ei;
        add(VP,E_SYN_PREP,ci,-1,-1,-1,3,false,"E"+to_string(ei)+"_syn_prep");
        for(int oi=0;oi<2;oi++)add(VP,E_2Q,ci,oi,-1,-1,15,true,"E"+to_string(ei)+"_2q_"+to_string(oi));
        add(VL,E_SYN_LOSS,ci,-1,-1,-1,1,false,"E"+to_string(ei)+"_syn_loss");
        add(VQ,E_MEAS,ci,-1,-1,-1,1,false,"E"+to_string(ei)+"_q");
        int bd=5+ei; for(int q=0;q<8;q++){add(VP,IDLE,-1,-1,q,bd,3,false,"idle_b"+to_string(bd)+"_q"+to_string(q+1));add(VL,DATA_LOSS,-1,-1,q,bd,1,false,"loss_b"+to_string(bd)+"_q"+to_string(q+1));}
    }
    return L;
}

char realchar(int r){ static const char P[3]={'X','Y','Z'}; return P[r]; }
pair<char,char> realpair(int r){ static vector<pair<char,char>> V=[](){vector<pair<char,char>>v;string p="IXYZ";for(char a:p)for(char b:p)if(!(a=='I'&&b=='I'))v.push_back({a,b});return v;}(); return V[r]; }

struct RoundRes{ uint32_t data; uint8_t frame=0,flags=0; };
RoundRes sim_round(uint32_t data,const Loc*loc,int real){
    auto apply_idle=[&](int bd){ if(loc&&loc->kind==IDLE&&loc->boundary==bd)data^=singlep(loc->q,realchar(real),8); };
    apply_idle(0);
    uint8_t frame=0,flags=0;
    for(int ci=0;ci<4;ci++){
        int n=10; uint32_t e=embed8(data,n);
        if(loc&&loc->kind==C_SYN_PREP&&loc->ci==ci){char p=realchar(real);if(p=='X'||p=='Y')e^=singlep(8,'X',n);}
        if(loc&&loc->kind==C_FLAG_PREP&&loc->ci==ci){char p=realchar(real);if(p=='Z'||p=='Y')e^=singlep(9,'Z',n);}
        auto &ops=COPS[ci];
        for(int oi=0;oi<(int)ops.size();oi++){
            e=applyop(e,ops[oi],n);
            if(loc&&loc->ci==ci&&loc->op==oi){
                if(loc->kind==C_1Q)e^=singlep(ops[oi].a,realchar(real),n);
                else if(loc->kind==C_2Q){auto [a,b]=realpair(real);e^=pairp(ops[oi].a,ops[oi].b,a,b,n);}
            }
        }
        auto [x,z]=splitp(e,n); int sb=(x>>8)&1,fb=(z>>9)&1;
        if(loc&&loc->kind==C_SYN_MEAS&&loc->ci==ci)sb^=1;
        if(loc&&loc->kind==C_FLAG_MEAS&&loc->ci==ci)fb^=1;
        if(sb)frame|=1u<<ci; if(fb)flags|=1u<<ci; data=extract8(e,n);
        apply_idle(ci+1);
    }
    for(int ei=0;ei<6;ei++){
        int ci=4+ei,n=9; uint32_t e=embed8(data,n);
        if(loc&&loc->kind==E_SYN_PREP&&loc->ci==ci){char p=realchar(real);if(p=='X'||p=='Y')e^=singlep(8,'X',n);}
        int a=EDGES[ei].first-1,b=EDGES[ei].second-1;
        array<Op,2> ops={Op{2,a,8},Op{2,b,8}};
        for(int oi=0;oi<2;oi++){
            e=applyop(e,ops[oi],n);
            if(loc&&loc->kind==E_2Q&&loc->ci==ci&&loc->op==oi){auto [pa,pb]=realpair(real);e^=pairp(ops[oi].a,ops[oi].b,pa,pb,n);}
        }
        // Edge measurement q has no downstream use; data only matters.
        data=extract8(e,n); apply_idle(5+ei);
    }
    return {data,frame,flags};
}

struct Sig{ uint32_t data=0; uint32_t frames=0,flags=0; int loss=0; }; // loss1 HOLD,2 QUAR
struct LocSigs{ Loc loc; vector<Sig> sigs; };

vector<LocSigs> build_sigs(int acq,int ver){
    int gid=0; vector<Loc> locs; vector<vector<Loc>> rounds;
    for(int r=0;r<acq+ver;r++){auto rr=build_round_locs(r,gid); rounds.push_back(rr); locs.insert(locs.end(),rr.begin(),rr.end());}
    // count verification.
    vector<LocSigs> out; out.reserve(locs.size());
    for(const Loc&L:locs){
        LocSigs ls;ls.loc=L;ls.sigs.resize(L.rcount);
        for(int real=0;real<L.rcount;real++){
            Sig sg;
            if(L.var==VL){ sg.loss=(L.kind==DATA_LOSS)?2:1; ls.sigs[real]=sg; continue; }
            if(L.round<acq){
                uint32_t data=0,fp=0,fl=0;
                for(int r=0;r<acq;r++){
                    const Loc*target=(r==L.round)?&L:nullptr;
                    RoundRes rr=sim_round(data,target,real); data=rr.data; fp|=uint32_t(rr.frame)<<(4*r); fl|=uint32_t(rr.flags)<<(4*r);
                }
                sg.data=data;sg.frames=fp;sg.flags=fl;
            } else {
                RoundRes rr=sim_round(0,&L,real);sg.data=rr.data;sg.frames=rr.frame;sg.flags=rr.flags;
            }
            ls.sigs[real]=sg;
        }
        out.push_back(move(ls));
    }
    // exact location count checks per round.
    return out;
}

uint8_t maj3(uint8_t a,uint8_t b,uint8_t c){ uint8_t r=0;for(int i=0;i<4;i++)if(((a>>i)&1)+((b>>i)&1)+((c>>i)&1)>=2)r|=1u<<i;return r; }
struct Score{ bool Y=false,HOLD=false,QUAR=false,L=false,R1=false,CLEAN=false; };
// Separate classification retaining acquisition and verification signatures.
struct Comb { Sig acq,ver; int loss=0; };
Comb combine_for_protocol(int acq,int ver,const LocSigs&A,int ra,const LocSigs*B=nullptr,int rb=0){
    Comb c; auto add=[&](const LocSigs&L,int r){const Sig&s=L.sigs[r];c.loss=max(c.loss,s.loss); if(L.loc.round<acq){c.acq.data^=s.data;c.acq.frames^=s.frames;c.acq.flags^=s.flags;} else {c.ver.data^=s.data;c.ver.frames^=s.frames;c.ver.flags^=s.flags;}}; add(A,ra);if(B)add(*B,rb);return c;
}
Score classify_comb(int acq,int ver,const Comb&c){
    Score z;if(c.loss==2){z.QUAR=true;return z;}if(c.loss==1){z.HOLD=true;return z;}
    if(c.acq.flags){z.HOLD=true;return z;}
    uint8_t sel=0;
    if(acq==1)sel=c.acq.frames&15;
    else if(acq==2){uint8_t f0=c.acq.frames&15,f1=(c.acq.frames>>4)&15;if(f0!=f1){z.HOLD=true;return z;}sel=f0;}
    else if(acq==3)sel=maj3(c.acq.frames&15,(c.acq.frames>>4)&15,(c.acq.frames>>8)&15);
    uint32_t data=c.acq.data^DECODER[b_to_s(sel)];
    if(ver){uint8_t obs=CSYN[data]^(c.ver.frames&15); if(c.ver.flags||obs){z.HOLD=true;return z;} data^=c.ver.data;}
    z.Y=true; z.L=(LCLASS[data]!=0); z.R1=(DRESS[data]==1); z.CLEAN=(!z.L&&DRESS[data]==0); return z;
}

const int NM=6; // Y,H,Q,L,R1,CLEAN
array<int,NM> metric(const Score&s){return {s.Y,s.HOLD,s.QUAR,s.L,s.R1,s.CLEAN};}
struct AggRaw { int f0=0; long long sp15=0,sq=0,sl=0,pp225=0,pq15=0,pl15=0,qq=0,ql=0,ll=0; };
struct AllAgg { array<AggRaw,NM> a; };
void add_single(AllAgg&agg,Var v,int rcount,const Score&s){auto m=metric(s);for(int k=0;k<NM;k++)if(m[k]){if(v==VP)agg.a[k].sp15+=15/rcount;else if(v==VQ)agg.a[k].sq++;else agg.a[k].sl++;}}
void add_pair(AllAgg&agg,const Loc&A,int ra,const Loc&B,int rb,const Score&s){auto m=metric(s);for(int k=0;k<NM;k++)if(m[k]){
    if(A.var==VP&&B.var==VP)agg.a[k].pp225+=225/(A.rcount*B.rcount);
    else if((A.var==VP&&B.var==VQ)||(A.var==VQ&&B.var==VP)){int rc=A.var==VP?A.rcount:B.rcount;agg.a[k].pq15+=15/rc;}
    else if((A.var==VP&&B.var==VL)||(A.var==VL&&B.var==VP)){int rc=A.var==VP?A.rcount:B.rcount;agg.a[k].pl15+=15/rc;}
    else if(A.var==VQ&&B.var==VQ)agg.a[k].qq++;
    else if((A.var==VQ&&B.var==VL)||(A.var==VL&&B.var==VQ))agg.a[k].ql++;
    else if(A.var==VL&&B.var==VL)agg.a[k].ll++;
}}
struct Poly { Rat c0,cp,cq,cl,cpp,cpq,cpl,cqq,cql,cll; };
Poly coeff(const AggRaw&r,int Np,int Nq,int Nl){
    Rat f0(r.f0),Sp(r.sp15,15),Sq(r.sq),Sl(r.sl),Spp(r.pp225,225),Spq(r.pq15,15),Spl(r.pl15,15),Sqq(r.qq),Sql(r.ql),Sll(r.ll);
    Poly p; p.c0=f0;p.cp=Sp-Np*f0;p.cq=Sq-Nq*f0;p.cl=Sl-Nl*f0;
    p.cpp=Spp-(Np-1)*Sp+Rat(1LL*Np*(Np-1)/2)*f0;
    p.cpq=Spq-Nq*Sp-Np*Sq+Rat(1LL*Np*Nq)*f0;
    p.cpl=Spl-Nl*Sp-Np*Sl+Rat(1LL*Np*Nl)*f0;
    p.cqq=Sqq-(Nq-1)*Sq+Rat(1LL*Nq*(Nq-1)/2)*f0;
    p.cql=Sql-Nl*Sq-Nq*Sl+Rat(1LL*Nq*Nl)*f0;
    p.cll=Sll-(Nl-1)*Sl+Rat(1LL*Nl*(Nl-1)/2)*f0;
    return p;
}
Poly subpoly(const Poly&a,const Poly&b){Poly p; p.c0=a.c0-b.c0;p.cp=a.cp-b.cp;p.cq=a.cq-b.cq;p.cl=a.cl-b.cl;p.cpp=a.cpp-b.cpp;p.cpq=a.cpq-b.cpq;p.cpl=a.cpl-b.cpl;p.cqq=a.cqq-b.cqq;p.cql=a.cql-b.cql;p.cll=a.cll-b.cll;return p;}
Poly ratio_series(const Poly&num,const Poly&den){
    assert(den.c0.n==1&&den.c0.d==1); assert(num.c0.n==0);
    Poly r; r.c0=Rat(0);r.cp=num.cp;r.cq=num.cq;r.cl=num.cl;
    r.cpp=num.cpp-den.cp*num.cp;
    r.cpq=num.cpq-(den.cp*num.cq+den.cq*num.cp);
    r.cpl=num.cpl-(den.cp*num.cl+den.cl*num.cp);
    r.cqq=num.cqq-den.cq*num.cq;
    r.cql=num.cql-(den.cq*num.cl+den.cl*num.cq);
    r.cll=num.cll-den.cl*num.cl;
    return r;
}
Poly reciprocal_times(const Poly&den,long long C){
    assert(den.c0.n==1&&den.c0.d==1); Poly r; r.c0=Rat(C);r.cp=Rat(-C)*den.cp;r.cq=Rat(-C)*den.cq;r.cl=Rat(-C)*den.cl;
    r.cpp=Rat(C)*(den.cp*den.cp-den.cpp);
    r.cpq=Rat(C)*(Rat(2)*den.cp*den.cq-den.cpq);
    r.cpl=Rat(C)*(Rat(2)*den.cp*den.cl-den.cpl);
    r.cqq=Rat(C)*(den.cq*den.cq-den.cqq);
    r.cql=Rat(C)*(Rat(2)*den.cq*den.cl-den.cql);
    r.cll=Rat(C)*(den.cl*den.cl-den.cll);return r;
}
string polyjson(const Poly&p){stringstream o;o<<"{\"1\":\""<<rs(p.c0)<<"\",\"p\":\""<<rs(p.cp)<<"\",\"q\":\""<<rs(p.cq)<<"\",\"l\":\""<<rs(p.cl)<<"\",\"p2\":\""<<rs(p.cpp)<<"\",\"pq\":\""<<rs(p.cpq)<<"\",\"pl\":\""<<rs(p.cpl)<<"\",\"q2\":\""<<rs(p.cqq)<<"\",\"ql\":\""<<rs(p.cql)<<"\",\"l2\":\""<<rs(p.cll)<<"\"}";return o.str();}
string rawjson(const AggRaw&r){stringstream o;o<<"{\"f0\":"<<r.f0<<",\"sp_num15\":"<<r.sp15<<",\"sq\":"<<r.sq<<",\"sl\":"<<r.sl<<",\"pp_num225\":"<<r.pp225<<",\"pq_num15\":"<<r.pq15<<",\"pl_num15\":"<<r.pl15<<",\"qq\":"<<r.qq<<",\"ql\":"<<r.ql<<",\"ll\":"<<r.ll<<"}";return o.str();}

struct Result { string name; int acq,ver,Np,Nq,Nl; long long realized=0; AllAgg agg; array<long long,NM> single_unweighted{}; array<Poly,NM> polys; Poly good,eps,r1ratio,cost2qgood,costmeasgood; };
Result runproto(string name,int acq,int ver,int gateCost,int measCost){
    cerr<<"build sigs "<<name<<"\n"; auto ls=build_sigs(acq,ver); int Np=0,Nq=0,Nl=0; for(auto&x:ls){if(x.loc.var==VP)Np++;else if(x.loc.var==VQ)Nq++;else Nl++;}
    if(Np!=179*(acq+ver)||Nq!=14*(acq+ver)||Nl!=102*(acq+ver)){cerr<<"location count mismatch "<<Np<<" "<<Nq<<" "<<Nl<<"\n";exit(3);} 
    Result R;R.name=name;R.acq=acq;R.ver=ver;R.Np=Np;R.Nq=Nq;R.Nl=Nl;
    // zero
    Comb zero; Score z=classify_comb(acq,ver,zero); auto zm=metric(z); for(int k=0;k<NM;k++)R.agg.a[k].f0=zm[k];
    // singles
    for(auto&A:ls)for(int ra=0;ra<A.loc.rcount;ra++){Comb c=combine_for_protocol(acq,ver,A,ra);Score s=classify_comb(acq,ver,c);add_single(R.agg,A.loc.var,A.loc.rcount,s);auto mm=metric(s);for(int k=0;k<NM;k++)R.single_unweighted[k]+=mm[k];R.realized++;}
    // pairs
    cerr<<"pairs "<<name<<" locs="<<ls.size()<<"\n";
    for(size_t i=0;i<ls.size();i++){
        auto&A=ls[i];
        for(size_t j=i+1;j<ls.size();j++){
            auto&B=ls[j];
            for(int ra=0;ra<A.loc.rcount;ra++)for(int rb=0;rb<B.loc.rcount;rb++){
                Comb c=combine_for_protocol(acq,ver,A,ra,&B,rb);Score s=classify_comb(acq,ver,c);add_pair(R.agg,A.loc,ra,B.loc,rb,s);R.realized++;
            }
        }
    }
    for(int k=0;k<NM;k++)R.polys[k]=coeff(R.agg.a[k],Np,Nq,Nl);
    R.good=subpoly(R.polys[0],R.polys[3]);R.eps=ratio_series(R.polys[3],R.polys[0]);R.r1ratio=ratio_series(R.polys[4],R.polys[0]);R.cost2qgood=reciprocal_times(R.good,gateCost);R.costmeasgood=reciprocal_times(R.good,measCost);
    // partition coefficient exact check Y+H+Q ==1
    Poly part=R.polys[0]; part= subpoly(part, Poly{}); // no-op
    auto addp=[](Poly a,const Poly&b){a.c0=a.c0+b.c0;a.cp=a.cp+b.cp;a.cq=a.cq+b.cq;a.cl=a.cl+b.cl;a.cpp=a.cpp+b.cpp;a.cpq=a.cpq+b.cpq;a.cpl=a.cpl+b.cpl;a.cqq=a.cqq+b.cqq;a.cql=a.cql+b.cql;a.cll=a.cll+b.cll;return a;};
    part=addp(part,R.polys[1]);part=addp(part,R.polys[2]);
    if(!(part.c0.n==1&&part.c0.d==1&&part.cp.n==0&&part.cq.n==0&&part.cl.n==0&&part.cpp.n==0&&part.cpq.n==0&&part.cpl.n==0&&part.cqq.n==0&&part.cql.n==0&&part.cll.n==0)){cerr<<"partition fail "<<name<<"\n";exit(4);} 
    return R;
}

int main(int argc,char**argv){
    init_code();
    vector<tuple<string,int,int,int,int>> P={{"1+0",1,0,39,14},{"2+1",2,1,117,42},{"3+1",3,1,156,56}};
    vector<Result> results;
    for(auto &[n,a,v,g,m]:P)results.push_back(runproto(n,a,v,g,m));
    const array<string,NM> names={"Y","HOLD","QUARANTINE","L_AND_ACCEPT","ACCEPT_DW1","Y_CLEAN"};
    cout<<"{\n  \"version\":\"0.1\",\n  \"status\":\"EXACT_SYMBOLIC_PAIR_ENUMERATION\",\n  \"source_branch_sha\":\"0d5d41b1410d097b9f33604c35085e63d109e86e\",\n  \"protocols\":{\n";
    for(size_t ri=0;ri<results.size();ri++){
        auto&R=results[ri]; if(ri)cout<<",\n"; cout<<"    \""<<R.name<<"\":{\n";
        cout<<"      \"locations\":{\"p\":"<<R.Np<<",\"q\":"<<R.Nq<<",\"l\":"<<R.Nl<<"},\n";
        cout<<"      \"expanded_single_plus_pair_realizations\":"<<R.realized<<",\n";
        cout<<"      \"single_unweighted\":{";for(int k=0;k<NM;k++){if(k)cout<<",";cout<<"\""<<names[k]<<"\":"<<R.single_unweighted[k];}cout<<"},\n";
        cout<<"      \"raw_aggregates\":{\n"; for(int k=0;k<NM;k++){if(k)cout<<",\n";cout<<"        \""<<names[k]<<"\":"<<rawjson(R.agg.a[k]);} cout<<"\n      },\n";
        cout<<"      \"polynomials_degree2\":{\n"; for(int k=0;k<NM;k++){if(k)cout<<",\n";cout<<"        \""<<names[k]<<"\":"<<polyjson(R.polys[k]);} cout<<",\n        \"Y_GOOD\":"<<polyjson(R.good)<<",\n        \"EPSILON_L_GIVEN_A\":"<<polyjson(R.eps)<<",\n        \"R1_GIVEN_A\":"<<polyjson(R.r1ratio)<<",\n        \"TWO_QUBIT_GATES_PER_GOOD\":"<<polyjson(R.cost2qgood)<<",\n        \"MEASUREMENTS_PER_GOOD\":"<<polyjson(R.costmeasgood)<<"\n      }\n";
        cout<<"    }";
    }
    cout<<"\n  },\n  \"notes\":{\"l_symbol\":\"p_loss\",\"hold_quarantine_success\":false,\"physical_promotion\":0}\n}\n";
}