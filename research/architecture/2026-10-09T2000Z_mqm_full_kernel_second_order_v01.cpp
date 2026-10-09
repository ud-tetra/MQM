#define main mqm_lc_hidden_main
#include "2026-10-09T1432Z_mqm_local_clifford_automorphism_v01a.cpp"
#undef main
#include <numeric>
using namespace std; using VI=vector<int>;
struct Rat{long long n=0,d=1;};
long long gcdll(long long a,long long b){return std::gcd(llabs(a),llabs(b));}
Rat rr(long long n,long long d){long long g=gcdll(n,d);return {n/g,d/g};}
bool leq(Rat a,Rat b){return (__int128)a.n*b.d<=(__int128)b.n*a.d;}
bool lt(Rat a,Rat b){return (__int128)a.n*b.d<(__int128)b.n*a.d;}
string rs(Rat a){return a.d==1?to_string(a.n):to_string(a.n)+"/"+to_string(a.d);}

int main(){
 vector<string> gs={"IIIXXZZI","IIIYIYZZ","IIIXZIXZ","XXXXYYIX","XIIIIIII","ZIIIIIIZ","IXIIIIII","IZIIIIIZ","IIXIIIII","IIZIIIIZ"};
 vector<P> gen;for(auto&s:gs)gen.push_back(pv(s));auto Gv=spanv(gen);unordered_set<int>G;for(P x:Gv)G.insert(x);
 vector<int> sc(256);for(P x:Gv)sc[supp(x)]++;
 vector<array<uint8_t,8>> perms;array<uint8_t,8> p={0,1,2,3,4,5,6,7};
 do{bool ok=1;for(int m=0;m<256&&ok;m++)if(sc[m]){int y=0;for(int i=0;i<8;i++)if(m>>i&1)y|=1<<p[i];if(sc[y]!=sc[m])ok=0;}if(ok)perms.push_back(p);}while(next_permutation(p.begin(),p.end()));
 vector<T>A;const int NN=1679616;
 for(auto &pp:perms)for(int code=0;code<NN;code++){int q=code;T t;t.p=pp;for(int i=0;i<8;i++){t.m[i]=q%6;q/=6;}bool ok=1;for(P g:gen)if(!G.count(applyT(g,t))){ok=0;break;}if(ok)A.push_back(t);}
 unordered_map<string,int> idx;idx.reserve(A.size()*2);for(int i=0;i<(int)A.size();i++)idx[key(A[i])]=i;int eid=idx[key(ident())];
 auto mid=[&](int a,int b){return idx[key(compose(A[a],A[b]))];};
 vector<int> invv(A.size());
 for(int i=0;i<(int)A.size();i++){int x=eid;for(int k=1;k<=24;k++){x=mid(i,x);if(x==eid){int y=eid;for(int j=0;j<k-1;j++)y=mid(i,y);invv[i]=y;break;}}}
 auto sg=[&](VI gens,int cap=2000){unordered_set<int>S;queue<int>Q;S.insert(eid);Q.push(eid);while(!Q.empty()&&S.size()<=size_t(cap)){int u=Q.front();Q.pop();for(int g:gens){int v=mid(g,u);if(S.insert(v).second)Q.push(v);}}VI v(S.begin(),S.end());sort(v.begin(),v.end());return v;};
 auto spec=[&](const VI&H){map<int,int>c;for(int x:H)c[ord(A[x])]++;return c;};
 auto isS4=[&](const VI&H){return H.size()==24&&spec(H)==map<int,int>{{1,1},{2,9},{3,8},{4,6}};};
 P LX=pv("IIIYZIZI"),LZ=pv("IIIXIZIZ");
 auto lp=[&](int i){return make_pair(logical_class(applyT(LX,A[i]),G,LX,LZ),logical_class(applyT(LZ,A[i]),G,LX,LZ));};
 VI K;for(int i=0;i<(int)A.size();i++)if(lp(i)==make_pair(1,2))K.push_back(i);assert(K.size()==192);

 int a=-1,b=-1;VI H1;
 for(int x:K)if(ord(A[x])==2){for(int y:K)if(ord(A[y])==3){if(ord(compose(A[x],A[y]))==4){auto H=sg({x,y},24);if(isS4(H)){a=x;b=y;H1=H;break;}}}if(a>=0)break;}
 VI Cent;for(int g=0;g<(int)A.size();g++)if(mid(g,a)==mid(a,g)&&mid(g,b)==mid(b,g))Cent.push_back(g);
 int c=-1,d=-1;VI H2;
 for(int x:Cent)if(ord(A[x])==2){for(int y:Cent)if(ord(A[y])==3){if(ord(compose(A[x],A[y]))!=4)continue;auto H=sg({x,y},24);if(!isS4(H))continue;int inter=0;for(int q:H)if(binary_search(H1.begin(),H1.end(),q))inter++;if(inter==1){c=x;d=y;H2=H;break;}}if(c>=0)break;}
 VI H2K;for(int x:H2)if(lp(x)==make_pair(1,2))H2K.push_back(x);sort(H2K.begin(),H2K.end());assert(H2K.size()==4);
 VI Z;for(int g=0;g<(int)A.size();g++){bool ok=1;for(int h=0;h<(int)A.size();h++)if(mid(g,h)!=mid(h,g)){ok=0;break;}if(ok)Z.push_back(g);}int z=Z[0]==eid?Z[1]:Z[0];
 int u=-1,v=-1;for(int x:H2K)if(x!=eid){u=x;break;}for(int x:H2K)if(x!=eid&&x!=u){if(sg({u,x},4).size()==4){v=x;break;}}assert(u>=0&&v>=0);
 vector<int> alphabet={z,a,b,invv[b],u,v};
 vector<int> wordlen(A.size(),-1);queue<int>Q;wordlen[eid]=0;Q.push(eid);
 while(!Q.empty()){int x=Q.front();Q.pop();for(int g:alphabet){int y=mid(g,x);if(wordlen[y]<0){wordlen[y]=wordlen[x]+1;Q.push(y);}}}
 for(int x:K)assert(wordlen[x]>=0);

 auto lmcomp=[&](int aa,int bb){int bx=LMS[bb].x1,bz=LMS[bb].z1;int ax=lmap(bx,LMS[aa]),az=lmap(bz,LMS[aa]);for(int k=0;k<6;k++)if(LMS[k].x1==ax&&LMS[k].z1==az)return k;return -1;};
 vector<int> ld(6,-1);vector<string> lw(6);queue<int>mq;ld[0]=0;lw[0]="";mq.push(0);int Hid=2,Sid=5;
 while(!mq.empty()){int x=mq.front();mq.pop();for(auto [g,ch]:vector<pair<int,char>>{{Hid,'H'},{Sid,'S'}}){int y=lmcomp(g,x);if(ld[y]<0){ld[y]=ld[x]+1;lw[y]=lw[x]+ch;mq.push(y);}}}
 auto sax=[&](int axis,const string&w){int sign=1,a0=axis;for(char ch:w){if(ch=='H'){if(a0==1)a0=2;else if(a0==2)a0=1;else sign=-sign;}else{if(a0==1)a0=3;else if(a0==3){a0=1;sign=-sign;}}}return pair<int,int>(a0,sign);};
 auto sapply=[&](P v0,const T&t){int x=v0&255,zz=(v0>>8)&255,nx=0,nz=0,sgn=1;for(int q=0;q<8;q++){int ax=((x>>q)&1)|(((zz>>q)&1)<<1);if(!ax)continue;auto [ao,ss]=sax(ax,lw[t.m[q]]);sgn*=ss;int j=t.p[q];if(ao&1)nx|=1<<j;if(ao&2)nz|=1<<j;}return pair<P,int>(P(nx|(nz<<8)),sgn);};
 vector<P> B;for(int q=0;q<8;q++)for(char ch:string("XYZ")){string s(8,'I');s[q]=ch;B.push_back(pv(s));}
 for(int i=0;i<8;i++)for(int j=i+1;j<8;j++)for(char x:string("XYZ"))for(char y:string("XYZ")){string s(8,'I');s[i]=x;s[j]=y;B.push_back(pv(s));}
 assert(B.size()==276);
 array<int,65536> bi;bi.fill(-1);for(int i=0;i<276;i++)bi[B[i]]=i;
 struct CR{P p=0;int s=0;}; static CR CT[276][276];
 auto mulphase=[&](P aa,P bb){int ph=0;for(int q=0;q<8;q++){int x=((aa>>q)&1)|(((aa>>(8+q))&1)<<1);int y=((bb>>q)&1)|(((bb>>(8+q))&1)<<1);if(!x||!y||x==y)continue;if((x==1&&y==3)||(x==3&&y==2)||(x==2&&y==1))ph=(ph+1)&3;else ph=(ph+3)&3;}return ph;};
 for(int i=0;i<276;i++)for(int j=0;j<276;j++){int ph=mulphase(B[i],B[j]);if(ph==1)CT[i][j]={P(B[i]^B[j]),1};else if(ph==3)CT[i][j]={P(B[i]^B[j]),-1};}
 auto stepcost=[&](int gid){int local=0,cyc=0;vector<int>vis(8);for(int i=0;i<8;i++)local+=ld[A[gid].m[i]];for(int i=0;i<8;i++)if(!vis[i]){cyc++;int j=i;while(!vis[j]){vis[j]=1;j=A[gid].p[j];}}return local+3*(8-cyc);};
 auto sper=[&](int gid){vector<int>cur(276),sg(276,1);iota(cur.begin(),cur.end(),0);for(int t=1;t<=24;t++){for(int e=0;e<276;e++){auto y=sapply(B[cur[e]],A[gid]);cur[e]=bi[y.first];sg[e]*=y.second;}bool ok=1;for(int e=0;e<276;e++)if(cur[e]!=e||sg[e]!=1){ok=0;break;}if(ok)return t;}return 0;};

 struct M{int id,T,cost,exposure,word;Rat a0,k2;};
 vector<M> met;met.reserve(192);
 static int acc[65536];vector<int> touched;touched.reserve(512);
 const long long PAIRS=276LL*275/2;
 for(int gi:K){
   int Tm=sper(gi);assert(Tm>0);
   vector<vector<int>> qi(276,vector<int>(Tm)),qs(276,vector<int>(Tm));
   for(int e=0;e<276;e++){P x=B[e];int sg0=1;for(int t=0;t<Tm;t++){qi[e][t]=bi[x];qs[e][t]=sg0;auto y=sapply(x,A[gi]);x=y.first;sg0*=y.second;}}
   long long a0num=0;
   for(int e=24;e<276;e++){int cnt[276]={0};for(int t=0;t<Tm;t++)cnt[qi[e][t]]+=qs[e][t];for(int q=0;q<276;q++)a0num+=1LL*cnt[q]*cnt[q];}
   Rat a0=rr(a0num,252LL*Tm*Tm);
   long long sumK=0;
   for(int e=0;e<276;e++)for(int f=e+1;f<276;f++){
     touched.clear();
     for(int j=0;j<Tm;j++)for(int k=0;k<j;k++){
       int ei=qi[e][j],fi=qi[f][j],ek=qi[e][k],fk=qi[f][k];
       int seJ=qs[e][j],sfJ=qs[f][j],seK=qs[e][k],sfK=qs[f][k];
       int A1[2]={ei,fi},A2[2]={ek,fk},S1[2]={seJ,sfJ},S2[2]={seK,sfK};
       for(int u0=0;u0<2;u0++)for(int v0=0;v0<2;v0++){auto cr=CT[A1[u0]][A2[v0]];if(!cr.s)continue;int val=cr.s*S1[u0]*S2[v0];if(acc[cr.p]==0)touched.push_back(cr.p);acc[cr.p]+=val;}
     }
     long long n=0;for(int q:touched){n+=1LL*acc[q]*acc[q];acc[q]=0;}sumK+=n;
   }
   Rat k2=rr(sumK,PAIRS*4LL*Tm*Tm);
   int cst=stepcost(gi);
   met.push_back({gi,Tm,cst,cst*Tm,wordlen[gi],a0,k2});
 }
 auto dom=[&](const M&a0,const M&b0){
   bool all=leq(a0.a0,b0.a0)&&leq(a0.k2,b0.k2)&&a0.exposure<=b0.exposure&&a0.cost<=b0.cost&&a0.word<=b0.word;
   bool strict=lt(a0.a0,b0.a0)||lt(a0.k2,b0.k2)||a0.exposure<b0.exposure||a0.cost<b0.cost||a0.word<b0.word;
   return all&&strict;
 };
 vector<M> front,db;for(auto &x:met){bool d0=0;for(auto &y:met)if(y.id!=x.id&&dom(y,x)){d0=1;break;}if(!d0)front.push_back(x);}
 auto itb=find_if(met.begin(),met.end(),[&](M x){return x.id==b;});assert(itb!=met.end());
 for(auto &x:met)if(x.id!=b&&dom(x,*itb))db.push_back(x);
 sort(front.begin(),front.end(),[](M a,M b){return tie(a.exposure,a.cost,a.word,a.id)<tie(b.exposure,b.cost,b.word,b.id);});
 auto jm=[&](M x){stringstream o;o<<"{\"id\":"<<x.id<<",\"signed_period\":"<<x.T<<",\"step_cost\":"<<x.cost<<",\"cycle_exposure\":"<<x.exposure<<",\"word_length\":"<<x.word<<",\"zeroth_w2\":\""<<rs(x.a0)<<"\",\"K2_two_term\":\""<<rs(x.k2)<<"\"}";return o.str();};
 cout<<"{\n  \"version\":\"0.1\",\n  \"status\":\"EXACT_FULL_K192_SECOND_ORDER_SEARCH\",\n  \"kernel_size\":"<<K.size()<<",\n";
 cout<<"  \"kernel_word_generators\":{\"z\":"<<z<<",\"a\":"<<a<<",\"b\":"<<b<<",\"B\":"<<invv[b]<<",\"u\":"<<u<<",\"v\":"<<v<<"},\n";
 cout<<"  \"reference_b\":"<<jm(*itb)<<",\n  \"pareto\":[";
 for(int i=0;i<(int)front.size();i++){if(i)cout<<",";cout<<jm(front[i]);}
 cout<<"],\n  \"dominates_b\":[";
 for(int i=0;i<(int)db.size();i++){if(i)cout<<",";cout<<jm(db[i]);}
 cout<<"],\n  \"physical_promotion\":0\n}\n";
}
