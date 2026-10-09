#define main mqm_lc_hidden_main
#include "../architecture/2026-10-09T1432Z_mqm_local_clifford_automorphism_v01a.cpp"
#undef main
#include <numeric>
using namespace std; using VI=vector<int>; using cd=complex<double>;
const int NQ=8,DIM=256;

struct Sim{vector<cd> U; long long GR=0,RZ=0,CZ=0; double tpar=0,tser=0; bool actual=false; Sim(bool a):U(DIM*DIM),actual(a){for(int i=0;i<DIM;i++)U[i*DIM+i]=1;}};
void oneq(Sim&s,int q,cd a,cd b,cd c,cd d){int bit=1<<q;for(int base=0;base<DIM;base++)if(!(base&bit)){int r0=base,r1=base|bit;for(int col=0;col<DIM;col++){cd x=s.U[r0*DIM+col],y=s.U[r1*DIM+col];s.U[r0*DIM+col]=a*x+b*y;s.U[r1*DIM+col]=c*x+d*y;}}}
void rz_site(Sim&s,int q,double th){s.RZ++;s.tser+=abs(th)/M_PI*0.25;double x=s.actual?1.012*th:th;oneq(s,q,exp(cd(0,-x/2)),0,0,exp(cd(0,x/2)));}
void rz_layer(Sim&s,const vector<int>&qs,double th){if(qs.empty())return;s.tpar+=abs(th)/M_PI*0.25;for(int q:qs)rz_site(s,q,th);}
void gr_y(Sim&s,double th){s.GR++;double tt=abs(th)/M_PI*4.1;s.tpar+=tt;s.tser+=tt;double x=s.actual?th+0.0345:th,C=cos(x/2),S=sin(x/2);for(int q=0;q<NQ;q++)oneq(s,q,C,-S,S,C);}
void Hsel(Sim&s,const vector<int>&T0){vector<int>T=T0;sort(T.begin(),T.end());vector<int>S;for(int q=0;q<NQ;q++)if(!binary_search(T.begin(),T.end(),q))S.push_back(q);rz_layer(s,T,M_PI);gr_y(s,M_PI/4);rz_layer(s,S,M_PI);gr_y(s,M_PI/4);rz_layer(s,S,-M_PI);}
void Slay(Sim&s,const vector<int>&T){rz_layer(s,T,M_PI/2);}
void cz(Sim&s,int q1,int q2){s.CZ++;s.tpar+=0.416;s.tser+=0.416;int b1=1<<q1,b2=1<<q2;for(int r=0;r<DIM;r++)if((r&b1)&&(r&b2))for(int c=0;c<DIM;c++)s.U[r*DIM+c]*=-1.;}
void cnot(Sim&s,int c,int t){Hsel(s,{t});cz(s,c,t);Hsel(s,{t});}
void swp(Sim&s,int a,int b){cnot(s,a,b);cnot(s,b,a);cnot(s,a,b);}
void permute_ideal(Sim&s,const array<uint8_t,8>&p){vector<cd> V(s.U.size());for(int r=0;r<DIM;r++){int d=0;for(int q=0;q<8;q++)if(r>>q&1)d|=1<<p[q];for(int c=0;c<DIM;c++)V[d*DIM+c]=s.U[r*DIM+c];}s.U.swap(V);}
double favg(const vector<cd>&A,const vector<cd>&B){cd tr=0;for(size_t i=0;i<A.size();i++)tr+=conj(A[i])*B[i];return (norm(tr)+DIM)/(double(DIM)*(DIM+1));}
double iderr(const vector<cd>&A){cd tr=0;for(int i=0;i<DIM;i++)tr+=A[i*DIM+i];return 1.-(norm(tr)+DIM)/(double(DIM)*(DIM+1));}

struct Plan{vector<pair<char,vector<int>>> layers; long long gr=0,rz=0;};
Plan plan_words(const array<string,8>&w){
  array<int,8> radix{},mul{};int states=1;for(int i=0;i<8;i++){radix[i]=w[i].size()+1;mul[i]=states;states*=radix[i];}
  struct V{int gr=1e9,rz=1e9,l=1e9,prev=-1;char op=0;};
  vector<V> dp(states);dp[0]={0,0,0,-1,0};
  auto dec=[&](int s){array<int,8>p{};for(int i=0;i<8;i++)p[i]=(s/mul[i])%radix[i];return p;};
  auto enc=[&](array<int,8>p){int s=0;for(int i=0;i<8;i++)s+=p[i]*mul[i];return s;};
  for(int st=0;st<states;st++)if(dp[st].gr<1e9){
    auto pos=dec(st);
    for(char op:string("HS")){
      vector<int>T;auto np=pos;
      for(int q=0;q<8;q++)if(pos[q]<(int)w[q].size()&&w[q][pos[q]]==op){T.push_back(q);np[q]++;}
      if(T.empty())continue;int ns=enc(np),ag=op=='H'?2:0,ar=op=='H'?(16-(int)T.size()):(int)T.size();
      auto cand=tuple(dp[st].gr+ag,dp[st].rz+ar,dp[st].l+1);
      auto cur=tuple(dp[ns].gr,dp[ns].rz,dp[ns].l);
      if(cand<cur)dp[ns]={get<0>(cand),get<1>(cand),get<2>(cand),st,op};
    }
  }
  int fin=states-1;Plan P;P.gr=dp[fin].gr;P.rz=dp[fin].rz;
  vector<pair<char,vector<int>>> rev;int st=fin;
  while(st){char op=dp[st].op;int pr=dp[st].prev;auto a=dec(pr),b=dec(st);vector<int>T;for(int q=0;q<8;q++)if(b[q]>a[q])T.push_back(q);rev.push_back({op,T});st=pr;}
  reverse(rev.begin(),rev.end());P.layers=rev;return P;
}
void apply_plan(Sim&s,const Plan&P){for(auto &L:P.layers){if(L.first=='H')Hsel(s,L.second);else Slay(s,L.second);}}
vector<pair<int,int>> swap_decomp(const array<uint8_t,8>&p){vector<int>vis(8);vector<pair<int,int>>sw;for(int i=0;i<8;i++)if(!vis[i]){vector<int>c;int j=i;while(!vis[j]){vis[j]=1;c.push_back(j);j=p[j];}for(int k=(int)c.size()-1;k>=1;k--)sw.push_back({c[0],c[k]});}return sw;}

int main(){
 vector<string> gs={"IIIXXZZI","IIIYIYZZ","IIIXZIXZ","XXXXYYIX","XIIIIIII","ZIIIIIIZ","IXIIIIII","IZIIIIIZ","IIXIIIII","IIZIIIIZ"};
 vector<P> gen;for(auto&s:gs)gen.push_back(pv(s));auto Gv=spanv(gen);unordered_set<int>G;for(P x:Gv)G.insert(x);
 vector<int> sc(256);for(P x:Gv)sc[supp(x)]++;
 vector<array<uint8_t,8>> perms;array<uint8_t,8> p={0,1,2,3,4,5,6,7};
 do{bool ok=1;for(int m=0;m<256&&ok;m++)if(sc[m]){int y=0;for(int i=0;i<8;i++)if(m>>i&1)y|=1<<p[i];if(sc[y]!=sc[m])ok=0;}if(ok)perms.push_back(p);}while(next_permutation(p.begin(),p.end()));
 vector<T>A;const int N=1679616;for(auto &pp:perms)for(int code=0;code<N;code++){int q=code;T t;t.p=pp;for(int i=0;i<8;i++){t.m[i]=q%6;q/=6;}bool ok=1;for(P g:gen)if(!G.count(applyT(g,t))){ok=0;break;}if(ok)A.push_back(t);}
 auto lmcomp=[&](int aa,int bb){int bx=LMS[bb].x1,bz=LMS[bb].z1;int ax=lmap(bx,LMS[aa]),az=lmap(bz,LMS[aa]);for(int k=0;k<6;k++)if(LMS[k].x1==ax&&LMS[k].z1==az)return k;return -1;};
 vector<int> ld(6,-1);vector<string> lw(6);queue<int>q;ld[0]=0;lw[0]="";q.push(0);int H=2,S=5;while(!q.empty()){int u=q.front();q.pop();for(auto [g,ch]:vector<pair<int,char>>{{H,'H'},{S,'S'}}){int v=lmcomp(g,u);if(ld[v]<0){ld[v]=ld[u]+1;lw[v]=lw[u]+ch;q.push(v);}}}
 map<string,pair<int,int>> targets={{"v128",{128,4}},{"b",{579,6}}};
 cout<<setprecision(17)<<"{\n  \"version\":\"0.1\",\n  \"status\":\"V128_NATIVE_COMPILE_AND_STRESS\",\n  \"targets\":{";
 bool first=true;
 for(auto [nm,ip]:targets){
   if(!first)cout<<",";first=false;int id=ip.first,per=ip.second;T t=A[id];array<string,8>w{};for(int i=0;i<8;i++)w[i]=lw[t.m[i]];Plan P=plan_words(w);auto sw=swap_decomp(t.p);
   int moved=0;for(int i=0;i<8;i++)moved+=t.p[i]!=i;
   cout<<"\n    \""<<nm<<"\":{\"id\":"<<id<<",\"signed_period\":"<<per<<",\"perm_one_based\":[";
   for(int i=0;i<8;i++){if(i)cout<<",";cout<<int(t.p[i])+1;}cout<<"],\"local_words\":[";
   for(int i=0;i<8;i++){if(i)cout<<",";cout<<"\""<<(w[i].empty()?"I":w[i])<<"\"";}cout<<"],\"batched_layers\":[";
   for(int i=0;i<(int)P.layers.size();i++){if(i)cout<<",";cout<<"{\"op\":\""<<P.layers[i].first<<"\",\"targets\":[";
     for(int j=0;j<(int)P.layers[i].second.size();j++){if(j)cout<<",";cout<<P.layers[i].second[j]+1;}cout<<"]}";}cout<<"],\"moved_roles\":"<<moved<<",\"min_swaps\":"<<sw.size();
   for(string mode:{"gate_SWAP","transport"}){
     Sim ideal(false),actual(true);
     for(int k=0;k<per;k++){apply_plan(ideal,P);apply_plan(actual,P);if(mode=="gate_SWAP"){for(auto [a,b0]:sw){swp(ideal,a,b0);swp(actual,a,b0);}}else{permute_ideal(ideal,t.p);permute_ideal(actual,t.p);}}
     double F=favg(ideal.U,actual.U);
     cout<<",\""<<mode<<"\":{\"GR\":"<<actual.GR<<",\"Rz\":"<<actual.RZ<<",\"CZ\":"<<actual.CZ<<",\"parallel_us\":"<<actual.tpar<<",\"serialRz_us\":"<<actual.tser<<",\"ideal_identity_infidelity\":"<<iderr(ideal.U)<<",\"cross_profile_Favg\":"<<F<<",\"cross_profile_infidelity\":"<<1-F<<",\"CZ_survival\":"<<pow(0.9962,actual.CZ)<<",\"Rz_leakage_envelope\":"<<pow(1-0.00066,actual.RZ)<<",\"GR_product\":"<<pow(0.99980,actual.GR)<<"}";
   }
   cout<<"}";
 }
 cout<<"\n  },\n  \"transport_scope\":\"ideal instantaneous permutation; MOVE timing/error/loss remain OPEN\",\n  \"physical_promotion\":0\n}\n";
}
