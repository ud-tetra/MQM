#define main mqm_lc_hidden_main
#include "2026-10-09T1432Z_mqm_local_clifford_automorphism_v01a.cpp"
#undef main
using VI=vector<int>;

int main(){
  vector<string> gauge_s={"IIIXXZZI","IIIYIYZZ","IIIXZIXZ","XXXXYYIX","XIIIIIII","ZIIIIIIZ","IXIIIIII","IZIIIIIZ","IIXIIIII","IIZIIIIZ"};
  vector<string> center_s={"IIIXXZZI","IIIYIYZZ","IIIXZIXZ","XXXXYYIX"};
  vector<P> gen;for(auto&s:gauge_s)gen.push_back(pv(s));auto Gv=spanv(gen);unordered_set<int>G;for(P x:Gv)G.insert(x);
  vector<P> C;for(auto&s:center_s)C.push_back(pv(s));
  // explicit syndrome helper
  auto syndrome=[&](P e){int s=0;int ex=e&255,ez=(e>>8)&255;for(int i=0;i<4;i++){int cx=C[i]&255,cz=(C[i]>>8)&255;int b=((__builtin_popcount(ex&cz)+__builtin_popcount(ez&cx))&1);s|=b<<i;}return s;};
  map<string,string> dl={
   {"1000","IIIIIYII"},{"1001","IIIIZIII"},{"1010","IIIIYIII"},{"1011","IIIYIIII"},
   {"1100","IIIIIIXI"},{"1101","IIIIIXII"},{"1110","IIIIIIYI"},{"1111","IIIZIIII"},
   {"0000","IIIIIIII"},{"0110","IIIIIIIX"},{"0111","IIIIIIIY"},{"0001","IIIIIIIZ"},
   {"0010","IIIIIIZI"},{"0100","IIIXIIII"},{"0101","IIIIIZII"},{"0011","IIIIXIII"}};
  array<P,16>D{};
  for(auto [k,v]:dl){int s=0;for(int i=0;i<4;i++)if(k[i]=='1')s|=1<<i;D[s]=pv(v);assert(syndrome(D[s])==s);}
  P LX=pv("IIIYZIZI"),LZ=pv("IIIXIZIZ");
  auto lclass=[&](P v){return logical_class(v,G,LX,LZ);};

  vector<int> sc(256);for(P x:Gv)sc[supp(x)]++;
  vector<array<uint8_t,8>> perms;array<uint8_t,8> p={0,1,2,3,4,5,6,7};
  do{bool ok=1;for(int m=0;m<256&&ok;m++)if(sc[m]){int y=0;for(int i=0;i<8;i++)if(m>>i&1)y|=1<<p[i];if(sc[y]!=sc[m])ok=0;}if(ok)perms.push_back(p);}while(next_permutation(p.begin(),p.end()));
  vector<T>A;const int N=1679616;
  for(auto &pp:perms)for(int code=0;code<N;code++){int q=code;T t;t.p=pp;for(int i=0;i<8;i++){t.m[i]=q%6;q/=6;}bool ok=1;for(P g:gen)if(!G.count(applyT(g,t))){ok=0;break;}if(ok)A.push_back(t);}
  unordered_map<string,int> idx;for(int i=0;i<(int)A.size();i++)idx[key(A[i])]=i;int eid=idx[key(ident())];
  auto mid=[&](int a,int b){return idx[key(compose(A[a],A[b]))];};
  vector<int> invv(A.size());
  for(int i=0;i<(int)A.size();i++){int x=eid;for(int k=1;k<=24;k++){x=mid(i,x);if(x==eid){int y=eid;for(int j=0;j<k-1;j++)y=mid(i,y);invv[i]=y;break;}}}
  auto sg=[&](VI gens,int cap=2000){unordered_set<int>S;queue<int>Q;S.insert(eid);Q.push(eid);while(!Q.empty()&&S.size()<=size_t(cap)){int u=Q.front();Q.pop();for(int g:gens){int v=mid(g,u);if(S.insert(v).second)Q.push(v);}}VI v(S.begin(),S.end());sort(v.begin(),v.end());return v;};
  auto spec=[&](const VI&H){map<int,int>c;for(int x:H)c[ord(A[x])]++;return c;};
  auto isS4=[&](const VI&H){return H.size()==24&&spec(H)==map<int,int>{{1,1},{2,9},{3,8},{4,6}};};
  auto lp=[&](int i){return make_pair(logical_class(applyT(LX,A[i]),G,LX,LZ),logical_class(applyT(LZ,A[i]),G,LX,LZ));};
  VI K;for(int i=0;i<(int)A.size();i++)if(lp(i)==make_pair(1,2))K.push_back(i);
  int h1a=-1,h1b=-1;VI H1;
  for(int a:K)if(ord(A[a])==2){for(int b:K)if(ord(A[b])==3){if(ord(compose(A[a],A[b]))==4){auto H=sg({a,b},24);if(isS4(H)){h1a=a;h1b=b;H1=H;break;}}}if(h1a>=0)break;}
  VI A41;for(int a:H1)if(ord(A[a])==2){for(int b:H1)if(ord(A[b])==3){if(ord(compose(A[a],A[b]))==3){auto H=sg({a,b},12);if(H.size()==12&&spec(H)==map<int,int>{{1,1},{2,3},{3,8}}){A41=H;break;}}}if(!A41.empty())break;}
  auto left_cosets=[&](const VI&H,const VI&L){vector<VI>cs;unordered_set<int>seen;for(int g:H)if(!seen.count(g)){VI c;for(int l:L){int y=mid(g,l);c.push_back(y);seen.insert(y);}sort(c.begin(),c.end());cs.push_back(c);}return cs;};
  int g3=-1;for(int x:A41)if(ord(A[x])==3){g3=x;break;}VI C3=sg({g3},3);auto ca=left_cosets(A41,C3);VI ar;for(auto&c:ca)ar.push_back(*min_element(c.begin(),c.end()));
  vector<pair<int,int>> ae;for(int i=0;i<4;i++)for(int j=i+1;j<4;j++)ae.push_back({i,j});

  T rt=ident();array<int,8> rp={1,2,0,4,3,6,5,7};for(int i=0;i<8;i++)rt.p[i]=rp[i];int rid=idx[key(rt)];
  VI dr;int x=eid;for(int i=0;i<6;i++){dr.push_back(x);x=mid(rid,x);}vector<pair<int,int>> de;for(int i=0;i<6;i++)de.push_back({i,(i+1)%6});

  auto trans=[&](int u,int v){return mid(v,invv[u]);};
  struct R{long long interfaces=0,cases=0,strict=0,gauge=0,logical=0;map<int,long long> lc;};
  auto audit=[&](VI reps,vector<pair<int,int>> edges){
    R z;
    for(auto [u,v]:edges)for(int dir=0;dir<2;dir++){
      int a=dir? v:u,b=dir?u:v,t=trans(reps[a],reps[b]);z.interfaces++;
      for(int s=0;s<16;s++){
        P td=applyT(D[s],A[t]);int sp=syndrome(td);P def=td^D[sp];z.cases++;
        if(def==0)z.strict++;
        if(G.count(def))z.gauge++;
        int c=lclass(def);z.lc[c]++;if(c!=0)z.logical++;
      }
    }
    return z;
  };
  R RA=audit(ar,ae),RD=audit(dr,de);
  auto jr=[&](R z){stringstream o;o<<"{\"directed_interfaces\":"<<z.interfaces<<",\"decoder_plaquettes\":"<<z.cases<<",\"strict_zero_defect\":"<<z.strict<<",\"gauge_defect\":"<<z.gauge<<",\"nontrivial_logical_defect\":"<<z.logical<<",\"logical_classes\":{";bool f=0;for(auto [k,v]:z.lc){if(f)o<<",";f=1;o<<"\""<<k<<"\":"<<v;}o<<"}}";return o.str();};
  cout<<"{\n  \"version\":\"0.1\",\n  \"status\":\"EXACT_2PV_SPACETIME_DECODER_HOLONOMY\",\n";
  cout<<"  \"A4\":"<<jr(RA)<<",\n  \"D6\":"<<jr(RD)<<",\n";
  cout<<"  \"transported_decoder_rule\":\"D_frame(s') = T D_canonical(s) gives zero mixed-plaquette defect by construction; naive reuse of canonical decoder is scored above\",\n";
  cout<<"  \"spatial_cycles\":{\"A4_rank\":3,\"D6_rank\":1,\"strict_closure\":true},\n";
  cout<<"  \"temporal_controller\":\"2+PV acquisition/recovery/conditional verification; zero syndrome is invariant under all frame automorphisms\",\n";
  cout<<"  \"physical_promotion\":0\n}\n";
}
