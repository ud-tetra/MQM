#define main mqm_lc_hidden_main
#include "2026-10-09T1432Z_mqm_local_clifford_automorphism_v01a.cpp"
#undef main
using VI=vector<int>;

int main(){
  vector<string> gs={"IIIXXZZI","IIIYIYZZ","IIIXZIXZ","XXXXYYIX","XIIIIIII","ZIIIIIIZ","IXIIIIII","IZIIIIIZ","IIXIIIII","IIZIIIIZ"};
  vector<P> gen;for(auto&s:gs)gen.push_back(pv(s));auto Gv=spanv(gen);unordered_set<int>G;for(P x:Gv)G.insert(x);
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
  P LX=pv("IIIYZIZI"),LZ=pv("IIIXIZIZ");
  auto lp=[&](int i){return make_pair(logical_class(applyT(LX,A[i]),G,LX,LZ),logical_class(applyT(LZ,A[i]),G,LX,LZ));};
  VI K;for(int i=0;i<(int)A.size();i++)if(lp(i)==make_pair(1,2))K.push_back(i);
  int h1a=-1,h1b=-1;VI H1;
  for(int a:K)if(ord(A[a])==2){for(int b:K)if(ord(A[b])==3){if(ord(compose(A[a],A[b]))==4){auto H=sg({a,b},24);if(isS4(H)){h1a=a;h1b=b;H1=H;break;}}}if(h1a>=0)break;}
  VI Cent;for(int g=0;g<(int)A.size();g++)if(mid(g,h1a)==mid(h1a,g)&&mid(g,h1b)==mid(h1b,g))Cent.push_back(g);
  int h2a=-1,h2b=-1;VI H2;
  for(int a:Cent)if(ord(A[a])==2){for(int b:Cent)if(ord(A[b])==3){if(ord(compose(A[a],A[b]))!=4)continue;auto H=sg({a,b},24);if(!isS4(H))continue;int inter=0;for(int x:H)if(binary_search(H1.begin(),H1.end(),x))inter++;if(inter==1){h2a=a;h2b=b;H2=H;break;}}if(h2a>=0)break;}
  VI Z;for(int g=0;g<(int)A.size();g++){bool ok=1;for(int h=0;h<(int)A.size();h++)if(mid(g,h)!=mid(h,g)){ok=0;break;}if(ok)Z.push_back(g);}
  int z=Z[0]==eid?Z[1]:Z[0];

  vector<pair<int,string>> alph={{z,"z"},{h1a,"a"},{h1b,"b"},{invv[h1b],"B"},{h2a,"c"},{h2b,"d"},{invv[h2b],"D"}};
  vector<int> dist(A.size(),-1),par(A.size(),-1),pg(A.size(),-1);queue<int>Q;dist[eid]=0;Q.push(eid);
  while(!Q.empty()){int u=Q.front();Q.pop();for(int gi=0;gi<(int)alph.size();gi++){int v=mid(alph[gi].first,u);if(dist[v]<0){dist[v]=dist[u]+1;par[v]=u;pg[v]=gi;Q.push(v);}}}
  for(int d:dist)assert(d>=0);
  auto word=[&](int x){vector<string>w;while(x!=eid){w.push_back(alph[pg[x]].second);x=par[x];}reverse(w.begin(),w.end());string s;for(auto&a:w)s+=a;return s.empty()?string("I"):s;};

  // local Clifford minimum word lengths in H,S
  vector<int> ld(6,-1);vector<string> lw(6);queue<int>mq;ld[0]=0;lw[0]="I";mq.push(0);
  auto lmcomp=[&](int a,int b){int bx=LMS[b].x1,bz=LMS[b].z1;int ax=lmap(bx,LMS[a]),az=lmap(bz,LMS[a]);for(int k=0;k<6;k++)if(LMS[k].x1==ax&&LMS[k].z1==az)return k;return -1;};
  int Hid=2,Sid=5;
  while(!mq.empty()){int u=mq.front();mq.pop();for(auto [g,nm]:vector<pair<int,string>>{{Hid,"H"},{Sid,"S"}}){int v=lmcomp(g,u);if(ld[v]<0){ld[v]=ld[u]+1;lw[v]=(lw[u]=="I"?"":lw[u])+nm;mq.push(v);}}}
  auto ccost=[&](int x){int local=0,cyc=0;vector<int>vis(8);for(int i=0;i<8;i++)local+=ld[A[x].m[i]];for(int i=0;i<8;i++)if(!vis[i]){cyc++;int j=i;while(!vis[j]){vis[j]=1;j=A[x].p[j];}}int sw=8-cyc;return tuple<int,int,int>(local,sw,local+3*sw);};

  auto logical_order=[&](pair<int,int> p){if(p==make_pair(1,2))return 1;int X=p.first,Z=p.second,Y=6-X-Z;array<int,4>f{};f[1]=X;f[2]=Z;f[3]=Y;array<int,4>g={0,1,2,3};for(int k=1;k<=3;k++){array<int,4>h{};for(int a=1;a<=3;a++)h[a]=f[g[a]];g=h;if(g[1]==1&&g[2]==2&&g[3]==3)return k;}return 0;};

  vector<pair<int,int>> targets={{1,2},{2,1},{2,3}};
  cout<<"{\n  \"version\":\"0.1\",\n  \"status\":\"EXACT_SHORT_MOTION_WORD_SEARCH\",\n";
  cout<<"  \"alphabet\":{\"z\":\"central C2\",\"a,b/B\":\"kernel S4 generators\",\"c,d/D\":\"logical S4 generators\"},\n";
  cout<<"  \"targets\":{";
  bool firstT=true;
  for(auto tar:targets){
    if(!firstT)cout<<",";firstT=false;
    string tname=tar==make_pair(1,2)?"identity":tar==make_pair(2,1)?"swap_XZ":"cycle_X_to_Z_to_Y";
    map<int,int> best;
    for(int i=0;i<(int)A.size();i++)if(lp(i)==tar){
      int lo=logical_order(tar),h=ord(A[i])/lo;
      if(!best.count(h)){best[h]=i;continue;}
      auto ci=ccost(i),cb=ccost(best[h]);
      if(make_tuple(dist[i],get<2>(ci),get<0>(ci),get<1>(ci),i)<make_tuple(dist[best[h]],get<2>(cb),get<0>(cb),get<1>(cb),best[h]))best[h]=i;
    }
    cout<<"\""<<tname<<"\":{";
    bool fh=true;for(auto [h,i]:best){if(!fh)cout<<",";fh=false;auto c=ccost(i);cout<<"\"h"<<h<<"\":{\"word\":\""<<word(i)<<"\",\"word_length\":"<<dist[i]<<",\"frame_order\":"<<ord(A[i])<<",\"logical_order\":"<<logical_order(tar)<<",\"local_HS_cost\":"<<get<0>(c)<<",\"swaps\":"<<get<1>(c)<<",\"primitive_cost\":"<<get<2>(c)<<"}";}
    cout<<"}";
  }
  cout<<"},\n  \"physical_promotion\":0\n}\n";
}
