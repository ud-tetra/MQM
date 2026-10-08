#include <algorithm>
#include <array>
#include <cassert>
#include <cmath>
#include <cstdint>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <map>
#include <numeric>
#include <random>
#include <sstream>
#include <string>
#include <tuple>
#include <unordered_set>
#include <vector>
using namespace std;

struct P { uint16_t x=0,z=0; };
P pxor(P a,P b){return {uint16_t(a.x^b.x),uint16_t(a.z^b.z)};}
bool peq(P a,P b){return a.x==b.x&&a.z==b.z;}
int pwt(P a){return __builtin_popcount((unsigned)(a.x|a.z));}
P pv(const string&s){P p;for(int i=0;i<(int)s.size();++i){char c=s[i];if(c=='X'||c=='Y')p.x|=1u<<i;if(c=='Z'||c=='Y')p.z|=1u<<i;}return p;}
int symp(P a,P b){return (__builtin_popcount((unsigned)(a.x&b.z))+__builtin_popcount((unsigned)(a.z&b.x)))&1;}
P H(P p,int q){bool x=(p.x>>q)&1,z=(p.z>>q)&1;if(x!=z){p.x^=1u<<q;p.z^=1u<<q;}return p;}
P Sg(P p,int q){if((p.x>>q)&1)p.z^=1u<<q;return p;}
P CNOT(P p,int c,int t){if((p.x>>c)&1)p.x^=1u<<t;if((p.z>>t)&1)p.z^=1u<<c;return p;}
P singlep(int q,char c){P p;if(c=='X'||c=='Y')p.x|=1u<<q;if(c=='Z'||c=='Y')p.z|=1u<<q;return p;}
P pairp(int a,int b,char A,char B){return pxor(singlep(a,A),singlep(b,B));}
P extract8(P p){return {uint16_t(p.x&0xffu),uint16_t(p.z&0xffu)};}

struct Op{int t,a,b;}; // 0H 1S 2CNOT
const array<string,4> CHECKS={"IIIXXZZI","IIIZZYYI","IIIYIYZZ","XXXXYYIX"};
const array<vector<int>,4> ORDERS={vector<int>{4,5,6,7},vector<int>{4,5,6,7},vector<int>{4,6,7,8},vector<int>{4,5,6,1,2,3,8}};
const array<pair<int,int>,6> EDGES={pair<int,int>{1,2},{1,3},{1,8},{2,3},{2,8},{3,8}};
vector<Op> center_ops(int ci){vector<Op>o;auto&s=CHECKS[ci];for(int q=0;q<8;q++){if(s[q]=='X')o.push_back({0,q,0});else if(s[q]=='Y'){o.push_back({1,q,0});o.push_back({0,q,0});}}int k=0;for(int d:ORDERS[ci]){o.push_back({2,d-1,8});if(++k==1||k==3)o.push_back({2,9,8});}for(int q=7;q>=0;q--){if(s[q]=='X')o.push_back({0,q,0});else if(s[q]=='Y'){o.push_back({0,q,0});o.push_back({1,q,0});}}return o;}
array<vector<Op>,4> COPS={center_ops(0),center_ops(1),center_ops(2),center_ops(3)};
P applyop(P p,const Op&o){if(o.t==0)return H(p,o.a);if(o.t==1)return Sg(p,o.a);return CNOT(p,o.a,o.b);}

array<P,4> OLDST={pv("IIIXXZZI"),pv("IIIYIYZZ"),pv("IIIXZIXZ"),pv("XXXXYYIX")};
array<P,4> CANDST={pv("IIIXXZZI"),pv("IIIZZYYI"),pv("IIIYIYZZ"),pv("XXXXYYIX")};
array<string,16> DECSTR={"IIIIIIII","IIIIIYII","IIIXIIII","IIIIIIXI","IIIIIIZI","IIIIYIII","IIIIIIIX","IIIIIIYI","IIIIIIIZ","IIIIZIII","IIIIIZII","IIIIIXII","IIIIXIII","IIIYIIII","IIIIIIIY","IIIZIIII"};
array<P,16> DEC;
vector<P> GAUGE;
array<uint8_t,65536> OSYN{},CSYN{},DRESS{},LCLASS{};
P LX=pv("IIIYZIZI"),LZ=pv("IIIXIZIZ");
int pack(P p){return p.x|(int(p.z)<<8);} 
bool in_gauge(P p){int v=pack(p);static unordered_set<int> gs; if(gs.empty())for(auto g:GAUGE)gs.insert(pack(g));return gs.count(v);}
int b_to_s(int b){int b1=b&1,b2=(b>>1)&1,b3=(b>>2)&1,b4=(b>>3)&1;return b1|(b3<<1)|((b2^b3)<<2)|(b4<<3);} 
void init_code(){for(int i=0;i<16;i++)DEC[i]=pv(DECSTR[i]);vector<string> gs={"IIIXXZZI","IIIYIYZZ","IIIXZIXZ","XXXXYYIX","XIIIIIII","ZIIIIIIZ","IXIIIIII","IZIIIIIZ","IIXIIIII","IIZIIIIZ"};GAUGE={{0,0}};for(auto&s:gs){P g=pv(s);size_t n=GAUGE.size();for(size_t i=0;i<n;i++)GAUGE.push_back(pxor(GAUGE[i],g));}sort(GAUGE.begin(),GAUGE.end(),[](P a,P b){return pack(a)<pack(b);});GAUGE.erase(unique(GAUGE.begin(),GAUGE.end(),peq),GAUGE.end());for(int v=0;v<65536;v++){P p{uint16_t(v&255),uint16_t(v>>8)};int os=0,cs=0;for(int i=0;i<4;i++){os|=symp(p,OLDST[i])<<i;cs|=symp(p,CANDST[i])<<i;}OSYN[v]=os;CSYN[v]=cs;int dw=9;for(auto g:GAUGE)dw=min(dw,pwt(pxor(p,g)));DRESS[v]=dw;P r=pxor(p,DEC[os]);uint8_t lc=255;array<pair<uint8_t,P>,4> ls={pair<uint8_t,P>{0,{0,0}},{1,LX},{2,LZ},{3,pxor(LX,LZ)}};for(auto [nm,l]:ls)if(in_gauge(pxor(r,l))){lc=nm;break;}if(lc==255){cerr<<"logical fail init\n";exit(2);}LCLASS[v]=lc;if(b_to_s(cs)!=os){cerr<<"syn map fail\n";exit(2);}}}

enum Var{VP,VQ,VL};
enum Kind{C_SYN_PREP,C_FLAG_PREP,C_1Q,C_2Q,E_SYN_PREP,E_2Q,IDLE,C_SYN_MEAS,C_FLAG_MEAS,E_MEAS,DATA_LOSS,C_SYN_LOSS,C_FLAG_LOSS,E_SYN_LOSS};
struct Loc{int id,round;Var var;Kind kind;int ci=-1,op=-1,q=-1,boundary=-1,rcount=1;};
vector<Loc> build_round(int r,int &gid){vector<Loc>L;auto add=[&](Var v,Kind k,int ci=-1,int op=-1,int q=-1,int bd=-1,int rc=1){L.push_back({gid++,r,v,k,ci,op,q,bd,rc});};for(int q=0;q<8;q++){add(VP,IDLE,-1,-1,q,0,3);add(VL,DATA_LOSS,-1,-1,q,0,1);}for(int ci=0;ci<4;ci++){add(VP,C_SYN_PREP,ci,-1,-1,-1,3);add(VP,C_FLAG_PREP,ci,-1,-1,-1,3);for(int oi=0;oi<(int)COPS[ci].size();oi++){if(COPS[ci][oi].t==2)add(VP,C_2Q,ci,oi,-1,-1,15);else add(VP,C_1Q,ci,oi,-1,-1,3);}add(VL,C_SYN_LOSS,ci);add(VL,C_FLAG_LOSS,ci);add(VQ,C_SYN_MEAS,ci);add(VQ,C_FLAG_MEAS,ci);for(int q=0;q<8;q++){add(VP,IDLE,-1,-1,q,ci+1,3);add(VL,DATA_LOSS,-1,-1,q,ci+1,1);}}for(int ei=0;ei<6;ei++){int ci=4+ei;add(VP,E_SYN_PREP,ci,-1,-1,-1,3);for(int oi=0;oi<2;oi++)add(VP,E_2Q,ci,oi,-1,-1,15);add(VL,E_SYN_LOSS,ci);add(VQ,E_MEAS,ci);for(int q=0;q<8;q++){add(VP,IDLE,-1,-1,q,5+ei,3);add(VL,DATA_LOSS,-1,-1,q,5+ei,1);}}return L;}
char rc3(int r){return "XYZ"[r];}
pair<char,char> rc15(int r){static vector<pair<char,char>>v=[](){vector<pair<char,char>>a;string s="IXYZ";for(char x:s)for(char z:s)if(!(x=='I'&&z=='I'))a.push_back({x,z});return a;}();return v[r];}
struct RoundRes{P data;uint8_t frame=0,flags=0;};
RoundRes sim_round(P data,const Loc*loc,int real){auto idle=[&](int bd){if(loc&&loc->kind==IDLE&&loc->boundary==bd)data=pxor(data,singlep(loc->q,rc3(real)));};idle(0);uint8_t fr=0,fl=0;for(int ci=0;ci<4;ci++){P e=data;if(loc&&loc->kind==C_SYN_PREP&&loc->ci==ci){char c=rc3(real);if(c=='X'||c=='Y')e=pxor(e,singlep(8,'X'));}if(loc&&loc->kind==C_FLAG_PREP&&loc->ci==ci){char c=rc3(real);if(c=='Z'||c=='Y')e=pxor(e,singlep(9,'Z'));}for(int oi=0;oi<(int)COPS[ci].size();oi++){e=applyop(e,COPS[ci][oi]);if(loc&&loc->ci==ci&&loc->op==oi){if(loc->kind==C_1Q)e=pxor(e,singlep(COPS[ci][oi].a,rc3(real)));else if(loc->kind==C_2Q){auto [a,b]=rc15(real);e=pxor(e,pairp(COPS[ci][oi].a,COPS[ci][oi].b,a,b));}}}int sb=(e.x>>8)&1,fb=(e.z>>9)&1;if(loc&&loc->kind==C_SYN_MEAS&&loc->ci==ci)sb^=1;if(loc&&loc->kind==C_FLAG_MEAS&&loc->ci==ci)fb^=1;if(sb)fr|=1u<<ci;if(fb)fl|=1u<<ci;data=extract8(e);idle(ci+1);}for(int ei=0;ei<6;ei++){int ci=4+ei;P e=data;if(loc&&loc->kind==E_SYN_PREP&&loc->ci==ci){char c=rc3(real);if(c=='X'||c=='Y')e=pxor(e,singlep(8,'X'));}array<Op,2>ops={Op{2,EDGES[ei].first-1,8},Op{2,EDGES[ei].second-1,8}};for(int oi=0;oi<2;oi++){e=applyop(e,ops[oi]);if(loc&&loc->kind==E_2Q&&loc->ci==ci&&loc->op==oi){auto [a,b]=rc15(real);e=pxor(e,pairp(ops[oi].a,ops[oi].b,a,b));}}data=extract8(e);idle(5+ei);}return {data,fr,fl};}

struct Sig{P data;uint64_t frames=0,flags=0;uint8_t loss=0;};
struct LS{Loc loc;vector<Sig>s;};
vector<LS> build_sigs(int acq,int ver){int gid=0;vector<Loc>locs;for(int r=0;r<acq+ver;r++){auto x=build_round(r,gid);locs.insert(locs.end(),x.begin(),x.end());}vector<LS>out;out.reserve(locs.size());for(auto &L:locs){LS a;a.loc=L;a.s.resize(L.rcount);for(int rr=0;rr<L.rcount;rr++){Sig sg;if(L.var==VL){sg.loss=(L.kind==DATA_LOSS)?2:1;a.s[rr]=sg;continue;}if(L.round<acq){P data{};uint64_t f=0,g=0;for(int r=0;r<acq;r++){RoundRes z=sim_round(data,r==L.round?&L:nullptr,rr);data=z.data;f|=uint64_t(z.frame)<<(4*r);g|=uint64_t(z.flags)<<(4*r);}sg.data=data;sg.frames=f;sg.flags=g;}else{auto z=sim_round({},&L,rr);sg.data=z.data;sg.frames=z.frame;sg.flags=z.flags;}a.s[rr]=sg;}out.push_back(move(a));}return out;}
uint8_t maj3(uint8_t a,uint8_t b,uint8_t c){uint8_t r=0;for(int i=0;i<4;i++)if(((a>>i)&1)+((b>>i)&1)+((c>>i)&1)>=2)r|=1u<<i;return r;}
struct Comb{Sig acq,ver;uint8_t loss=0;};
struct Score{bool Y=0,H=0,Q=0,L=0,R1=0,CLEAN=0,GOOD=0;};
Score classify(int acq,int ver,const Comb&c){Score z;if(c.loss==2){z.Q=1;return z;}if(c.loss==1){z.H=1;return z;}if(c.acq.flags){z.H=1;return z;}uint8_t sel=0;if(acq==1)sel=c.acq.frames&15;else if(acq==2){auto a=c.acq.frames&15,b=(c.acq.frames>>4)&15;if(a!=b){z.H=1;return z;}sel=a;}else sel=maj3(c.acq.frames&15,(c.acq.frames>>4)&15,(c.acq.frames>>8)&15);P data=pxor(c.acq.data,DEC[b_to_s(sel)]);if(ver){uint8_t obs=CSYN[pack(data)]^(c.ver.frames&15);if(c.ver.flags||obs){z.H=1;return z;}data=pxor(data,c.ver.data);}z.Y=1;z.L=LCLASS[pack(data)]!=0;z.R1=DRESS[pack(data)]==1;z.CLEAN=!z.L&&DRESS[pack(data)]==0;z.GOOD=!z.L;return z;}
array<int,7> mv(const Score&s){return {s.Y,s.H,s.Q,s.L,s.R1,s.CLEAN,s.GOOD};}
void add_event(Comb &c,const LS&ls,int real,int acq){const Sig&s=ls.s[real];c.loss=max(c.loss,s.loss);if(ls.loc.round<acq){c.acq.data=pxor(c.acq.data,s.data);c.acq.frames^=s.frames;c.acq.flags^=s.flags;}else{c.ver.data=pxor(c.ver.data,s.data);c.ver.frames^=s.frames;c.ver.flags^=s.flags;}}

struct Raw{double f0=0,sp=0,sq=0,sl=0,spp=0,spq=0,spl=0,sqq=0,sql=0,sll=0;};
struct Proto{string name;int acq,ver,Np,Nq,Nl;vector<LS>ls;vector<int>ip,iq,il;array<Raw,7>raw;};
Proto make_proto(string name,int a,int v){Proto P{name,a,v};P.ls=build_sigs(a,v);for(int i=0;i<(int)P.ls.size();i++){auto var=P.ls[i].loc.var;if(var==VP){P.ip.push_back(i);P.Np++;}else if(var==VQ){P.iq.push_back(i);P.Nq++;}else{P.il.push_back(i);P.Nl++;}}Comb c0;auto z0=classify(a,v,c0);auto m0=mv(z0);for(int k=0;k<7;k++)P.raw[k].f0=m0[k];cerr<<"enumerate low-order "<<name<<" locs="<<P.ls.size()<<"\n";for(int i=0;i<(int)P.ls.size();i++){auto&A=P.ls[i];for(int ra=0;ra<A.loc.rcount;ra++){Comb c;add_event(c,A,ra,a);auto m=mv(classify(a,v,c));double w=1.0/A.loc.rcount;for(int k=0;k<7;k++)if(m[k]){if(A.loc.var==VP)P.raw[k].sp+=w;else if(A.loc.var==VQ)P.raw[k].sq+=w;else P.raw[k].sl+=w;}}}for(int i=0;i<(int)P.ls.size();i++){auto&A=P.ls[i];for(int j=i+1;j<(int)P.ls.size();j++){auto&B=P.ls[j];for(int ra=0;ra<A.loc.rcount;ra++)for(int rb=0;rb<B.loc.rcount;rb++){Comb c;add_event(c,A,ra,a);add_event(c,B,rb,a);auto m=mv(classify(a,v,c));double w=1.0/(A.loc.rcount*B.loc.rcount);for(int k=0;k<7;k++)if(m[k]){auto va=A.loc.var,vb=B.loc.var;if(va==VP&&vb==VP)P.raw[k].spp+=w;else if((va==VP&&vb==VQ)||(va==VQ&&vb==VP))P.raw[k].spq+=w;else if((va==VP&&vb==VL)||(va==VL&&vb==VP))P.raw[k].spl+=w;else if(va==VQ&&vb==VQ)P.raw[k].sqq+=w;else if((va==VQ&&vb==VL)||(va==VL&&vb==VQ))P.raw[k].sql+=w;else P.raw[k].sll+=w;}}}}return P;}

double binom_logpmf(int n,int k,double x){if(k<0||k>n)return -INFINITY;if(x==0)return k==0?0:-INFINITY;if(x==1)return k==n?0:-INFINITY;return lgamma(n+1)-lgamma(k+1)-lgamma(n-k+1)+k*log(x)+(n-k)*log1p(-x);} 
vector<double> binom_pmf(int n,double x){vector<double>a(n+1);if(x==0){a[0]=1;return a;}double q=1-x;a[0]=pow(q,n);for(int k=0;k<n;k++)a[k+1]=a[k]*(n-k)/(k+1)*x/q;return a;}
vector<double> conv(const vector<double>&a,const vector<double>&b){vector<double>c(a.size()+b.size()-1);for(size_t i=0;i<a.size();i++)if(a[i])for(size_t j=0;j<b.size();j++)if(b[j])c[i+j]+=a[i]*b[j];return c;}
struct CountSampler{vector<double> ap,aq,al,total,tailcdf;double tail=0;int Np,Nq,Nl;CountSampler(int np,int nq,int nl,double p,double q,double l):Np(np),Nq(nq),Nl(nl){ap=binom_pmf(np,p);aq=binom_pmf(nq,q);al=binom_pmf(nl,l);total=conv(conv(ap,aq),al);for(int n=3;n<(int)total.size();n++)tail+=total[n];double c=0;tailcdf.resize(total.size());if(tail>0)for(int n=3;n<(int)total.size();n++){c+=total[n]/tail;tailcdf[n]=c;}}int sampleN(mt19937_64&r){uniform_real_distribution<double>U(0,1);double u=U(r);auto it=lower_bound(tailcdf.begin()+3,tailcdf.end(),u);return int(it-tailcdf.begin());}tuple<int,int,int> sampleComp(int N,mt19937_64&r){vector<double>w;vector<pair<int,int>>ij;double s=0;for(int kp=0;kp<=min(N,Np);kp++)for(int kq=0;kq<=min(N-kp,Nq);kq++){int kl=N-kp-kq;if(kl<0||kl>Nl)continue;double x=ap[kp]*aq[kq]*al[kl];if(x){s+=x;w.push_back(s);ij.push_back({kp,kq});}}uniform_real_distribution<double>U(0,s);double u=U(r);size_t t=lower_bound(w.begin(),w.end(),u)-w.begin();int kp=ij[t].first,kq=ij[t].second;return {kp,kq,N-kp-kq};}};
uint64_t splitmix64(uint64_t x){x+=0x9e3779b97f4a7c15ULL;x=(x^(x>>30))*0xbf58476d1ce4e5b9ULL;x=(x^(x>>27))*0x94d049bb133111ebULL;return x^(x>>31);} 
void sample_distinct(const vector<int>&pool,int k,mt19937_64&r,vector<int>&out){out.clear();if(k==0)return;uniform_int_distribution<int>D(0,(int)pool.size()-1);while((int)out.size()<k){int x=pool[D(r)];bool ok=1;for(int y:out)if(x==y){ok=0;break;}if(ok)out.push_back(x);}}

double lowprob(const Raw&r,int np,int nq,int nl,double p,double q,double l){double ap=1-p,aq=1-q,al=1-l;double base=pow(ap,np)*pow(aq,nq)*pow(al,nl);double z=r.f0*base;if(np)z+=r.sp*p*pow(ap,np-1)*pow(aq,nq)*pow(al,nl);if(nq)z+=r.sq*q*pow(ap,np)*pow(aq,nq-1)*pow(al,nl);if(nl)z+=r.sl*l*pow(ap,np)*pow(aq,nq)*pow(al,nl-1);if(np>=2)z+=r.spp*p*p*pow(ap,np-2)*pow(aq,nq)*pow(al,nl);if(np&&nq)z+=r.spq*p*q*pow(ap,np-1)*pow(aq,nq-1)*pow(al,nl);if(np&&nl)z+=r.spl*p*l*pow(ap,np-1)*pow(aq,nq)*pow(al,nl-1);if(nq>=2)z+=r.sqq*q*q*pow(ap,np)*pow(aq,nq-2)*pow(al,nl);if(nq&&nl)z+=r.sql*q*l*pow(ap,np)*pow(aq,nq-1)*pow(al,nl-1);if(nl>=2)z+=r.sll*l*l*pow(ap,np)*pow(aq,nq)*pow(al,nl-2);return z;}

string jnum(double x){ostringstream o;o<<setprecision(17)<<x;return o.str();}
int main(){init_code();vector<Proto>P;P.push_back(make_proto("1+0",1,0));P.push_back(make_proto("2+1",2,1));P.push_back(make_proto("3+1",3,1));vector<double> rates={0,ldexp(1.0,-21),ldexp(1.0,-19),ldexp(1.0,-17),ldexp(1.0,-15)};const int SHOTS=200000;const double alpha=1.0/3000000.0;double h=sqrt(log(2/alpha)/(2.0*SHOTS));uint64_t master=0x4D514D5F32303236ULL;array<string,7> mn={"Y","HOLD","QUARANTINE","L_AND_ACCEPT","ACCEPT_DW1","Y_CLEAN","Y_GOOD"};ofstream out("/mnt/data/mqm_full/MQM_FULL_STOCHASTIC_GRID_RESULTS_v0.1.json");out<<"{\n\"version\":\"0.1\",\"status\":\"HIGHER_ORDER_TAIL_MONTE_CARLO_WITH_EXACT_LE2\",\"tail_shots_per_nonzero_point\":"<<SHOTS<<",\"hoeffding_conditional_halfwidth\":"<<setprecision(17)<<h<<",\"protocols\":{";for(int pi=0;pi<3;pi++){auto&pr=P[pi];if(pi)out<<",";out<<"\n\""<<pr.name<<"\":[";bool first=1;for(int ip=0;ip<5;ip++)for(int iq=0;iq<5;iq++)for(int il=0;il<5;il++){double p=rates[ip],q=rates[iq],l=rates[il];CountSampler cs(pr.Np,pr.Nq,pr.Nl,p,q,l);array<double,7> low{},est{},lo{},hi{};for(int k=0;k<7;k++)low[k]=lowprob(pr.raw[k],pr.Np,pr.Nq,pr.Nl,p,q,l);array<long long,7> cnt{};if(cs.tail>0){uint64_t seed=splitmix64(master^uint64_t(pi+1)^((uint64_t)ip<<8)^((uint64_t)iq<<16)^((uint64_t)il<<24));mt19937_64 rng(seed);vector<int>a,b,c;uniform_int_distribution<int>u3(0,2),u15(0,14);for(int s=0;s<SHOTS;s++){int N=cs.sampleN(rng);auto[kp,kq,kl]=cs.sampleComp(N,rng);sample_distinct(pr.ip,kp,rng,a);sample_distinct(pr.iq,kq,rng,b);sample_distinct(pr.il,kl,rng,c);Comb comb;for(int idx:a){auto&ls=pr.ls[idx];int rr=ls.loc.rcount==15?u15(rng):u3(rng);add_event(comb,ls,rr,pr.acq);}for(int idx:b)add_event(comb,pr.ls[idx],0,pr.acq);for(int idx:c)add_event(comb,pr.ls[idx],0,pr.acq);auto m=mv(classify(pr.acq,pr.ver,comb));for(int k=0;k<7;k++)cnt[k]+=m[k];}}for(int k=0;k<7;k++){double frac=cs.tail?double(cnt[k])/SHOTS:0;est[k]=low[k]+cs.tail*frac;double d=cs.tail*h;lo[k]=max(0.0,est[k]-d);hi[k]=min(1.0,est[k]+d);}double eps=est[0]>0?est[3]/est[0]:0;double epslo=(lo[3])/(hi[0]>0?hi[0]:1);double epshi=(lo[0]>0)?hi[3]/lo[0]:1;double r1=est[0]>0?est[4]/est[0]:0;double good=est[6];if(!first)out<<",";first=0;out<<"{\"i\":["<<ip<<","<<iq<<","<<il<<"],\"rates\":["<<jnum(p)<<","<<jnum(q)<<","<<jnum(l)<<"],\"tail\":"<<jnum(cs.tail)<<",\"metrics\":{";for(int k=0;k<7;k++){if(k)out<<",";out<<"\""<<mn[k]<<"\":{\"v\":"<<jnum(est[k])<<",\"lo\":"<<jnum(lo[k])<<",\"hi\":"<<jnum(hi[k])<<"}";}out<<",\"EPSILON_L_GIVEN_A\":{\"v\":"<<jnum(eps)<<",\"lo\":"<<jnum(epslo)<<",\"hi\":"<<jnum(epshi)<<"},\"R1_GIVEN_A\":{\"v\":"<<jnum(r1)<<"},\"GATES_PER_GOOD\":{\"v\":"<<jnum((pi==0?39:pi==1?117:156)/good)<<"},\"MEAS_PER_GOOD\":{\"v\":"<<jnum((pi==0?14:pi==1?42:56)/good)<<"}},\"tail_counts\":{";for(int k=0;k<7;k++){if(k)out<<",";out<<"\""<<mn[k]<<"\":"<<cnt[k];}out<<"}}";}out<<"]";}out<<"\n},\"physical_promotion\":0}\n";out.close();cerr<<"done\n";}