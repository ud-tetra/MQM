#define main mqm_lc_hidden_main
#include "2026-10-09T1432Z_mqm_local_clifford_automorphism_v01a.cpp"
#undef main
#include <numeric>
using namespace std; using VI=vector<int>;

struct RQ{long long n=0,d=1;};
long long gg(long long a,long long b){return std::gcd(llabs(a),llabs(b));}
RQ red(long long n,long long d){long long g=gg(n,d);return {n/g,d/g};}
string rs(RQ x){return x.d==1?to_string(x.n):to_string(x.n)+"/"+to_string(x.d);}

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
 vector<int> invv(A.size());for(int i=0;i<(int)A.size();i++){int x=eid;for(int k=1;k<=24;k++){x=mid(i,x);if(x==eid){int y=eid;for(int j=0;j<k-1;j++)y=mid(i,y);invv[i]=y;break;}}}
 auto sg=[&](VI gens,int cap=2000){unordered_set<int>S;queue<int>Q;S.insert(eid);Q.push(eid);while(!Q.empty()&&S.size()<=size_t(cap)){int u=Q.front();Q.pop();for(int g:gens){int v=mid(g,u);if(S.insert(v).second)Q.push(v);}}VI v(S.begin(),S.end());sort(v.begin(),v.end());return v;};
 auto spec=[&](const VI&H){map<int,int>c;for(int x:H)c[ord(A[x])]++;return c;};
 auto isS4=[&](const VI&H){return H.size()==24&&spec(H)==map<int,int>{{1,1},{2,9},{3,8},{4,6}};};
 P LX=pv("IIIYZIZI"),LZ=pv("IIIXIZIZ");
 auto lp=[&](int i){return make_pair(logical_class(applyT(LX,A[i]),G,LX,LZ),logical_class(applyT(LZ,A[i]),G,LX,LZ));};
 VI K;for(int i=0;i<(int)A.size();i++)if(lp(i)==make_pair(1,2))K.push_back(i);
 int a=-1,b=-1;VI H1;for(int x:K)if(ord(A[x])==2){for(int y:K)if(ord(A[y])==3){if(ord(compose(A[x],A[y]))==4){auto H=sg({x,y},24);if(isS4(H)){a=x;b=y;H1=H;break;}}}if(a>=0)break;}
 VI Z;for(int g=0;g<(int)A.size();g++){bool ok=1;for(int h=0;h<(int)A.size();h++)if(mid(g,h)!=mid(h,g)){ok=0;break;}if(ok)Z.push_back(g);}int z=Z[0]==eid?Z[1]:Z[0];
 auto eval=[&](string w){int x=eid;for(char c:w){int g=c=='a'?a:c=='b'?b:c=='z'?z:eid;x=mid(g,x);}return x;};
 map<string,int> cand={{"I",eid},{"a",a},{"b",b},{"ab",eval("ab")},{"zb",eval("zb")}};

 auto lmcomp=[&](int aa,int bb){int bx=LMS[bb].x1,bz=LMS[bb].z1;int ax=lmap(bx,LMS[aa]),az=lmap(bz,LMS[aa]);for(int k=0;k<6;k++)if(LMS[k].x1==ax&&LMS[k].z1==az)return k;return -1;};
 vector<int> ld(6,-1);vector<string> lw(6);queue<int>mq;ld[0]=0;lw[0]="";mq.push(0);int Hid=2,Sid=5;
 while(!mq.empty()){int u=mq.front();mq.pop();for(auto [g,ch]:vector<pair<int,char>>{{Hid,'H'},{Sid,'S'}}){int v=lmcomp(g,u);if(ld[v]<0){ld[v]=ld[u]+1;lw[v]=lw[u]+ch;mq.push(v);}}}
 auto sax=[&](int axis,const string&w){int sign=1,a0=axis;for(char c:w){if(c=='H'){if(a0==1)a0=2;else if(a0==2)a0=1;else sign=-sign;}else{if(a0==1)a0=3;else if(a0==3){a0=1;sign=-sign;}}}return pair<int,int>(a0,sign);};
 auto sapply=[&](P v,const T&t){int x=v&255,zz=(v>>8)&255,nx=0,nz=0,sgn=1;for(int q=0;q<8;q++){int ax=((x>>q)&1)|(((zz>>q)&1)<<1);if(!ax)continue;auto [ao,ss]=sax(ax,lw[t.m[q]]);sgn*=ss;int j=t.p[q];if(ao&1)nx|=1<<j;if(ao&2)nz|=1<<j;}return pair<P,int>(P(nx|(nz<<8)),sgn);};
 vector<P> W1,W2;for(int q=0;q<8;q++)for(char c:string("XYZ")){string s(8,'I');s[q]=c;W1.push_back(pv(s));}
 for(int i=0;i<8;i++)for(int j=i+1;j<8;j++)for(char x:string("XYZ"))for(char y:string("XYZ")){string s(8,'I');s[i]=x;s[j]=y;W2.push_back(pv(s));}
 vector<P> WB=W1;WB.insert(WB.end(),W2.begin(),W2.end());

 auto sper=[&](const T&t){for(int k=1;k<=48;k++){bool ok=1;for(P e:W1){P x=e;int sg=1;for(int q=0;q<k;q++){auto y=sapply(x,t);x=y.first;sg*=y.second;}if(x!=e||sg!=1){ok=0;break;}}if(ok)return k;}return 0;};
 auto stepcost=[&](int gid){int local=0,cyc=0;vector<int>vis(8);for(int i=0;i<8;i++)local+=ld[A[gid].m[i]];for(int i=0;i<8;i++)if(!vis[i]){cyc++;int j=i;while(!vis[j]){vis[j]=1;j=A[gid].p[j];}}return local+3*(8-cyc);};

 auto mulphase=[&](P a0,P b0){int ph=0;for(int q=0;q<8;q++){int a1=((a0>>q)&1)|(((a0>>(8+q))&1)<<1);int b1=((b0>>q)&1)|(((b0>>(8+q))&1)<<1);if(!a1||!b1||a1==b1)continue;if((a1==1&&b1==3)||(a1==3&&b1==2)||(a1==2&&b1==1))ph=(ph+1)&3;else ph=(ph+3)&3;}return ph;};
 auto comm=[&](P p0,int sp0,P q0,int sq0)->tuple<bool,P,int>{int ph=mulphase(p0,q0);if(ph==0||ph==2)return {false,0,0};int sg=(ph==1?1:-1)*sp0*sq0;return {true,P(p0^q0),sg};};
 auto toggles=[&](P e,int gid,int Tm){vector<pair<P,int>>v;P x=e;int sg=1;for(int t=0;t<Tm;t++){v.push_back({x,sg});auto y=sapply(x,A[gid]);x=y.first;sg*=y.second;}return v;};

 struct Stat{long long count=0,zero=0,sumN=0,sumD=1,maxN=0,maxD=1;};
 auto addstat=[&](Stat&s,long long n,long long d){s.count++;if(n==0)s.zero++;long long l=std::lcm(s.sumD,d);s.sumN=s.sumN*(l/s.sumD)+n*(l/d);s.sumD=l;long long g=gg(s.sumN,s.sumD);s.sumN/=g;s.sumD/=g;if((__int128)n*s.maxD>(__int128)s.maxN*d){s.maxN=n;s.maxD=d;}};
 auto k2single=[&](P e,int gid,int Tm){auto v=toggles(e,gid,Tm);map<P,long long>c;for(int j=0;j<Tm;j++)for(int k=0;k<j;k++){auto [ok,r,sg]=comm(v[j].first,v[j].second,v[k].first,v[k].second);if(ok)c[r]+=sg;}long long n=0;for(auto [r,x]:c)n+=x*x;return red(n,1LL*Tm*Tm);};
 auto k2pair=[&](P e,P f,int gid,int Tm){auto a0=toggles(e,gid,Tm),b0=toggles(f,gid,Tm);map<P,long long>c;for(int j=0;j<Tm;j++)for(int k=0;k<j;k++){pair<P,int> J[2]={a0[j],b0[j]},Kk[2]={a0[k],b0[k]};for(auto u:J)for(auto v:Kk){auto [ok,r,sg]=comm(u.first,u.second,v.first,v.second);if(ok)c[r]+=sg;}}long long n=0;for(auto [r,x]:c)n+=x*x;return red(n,4LL*Tm*Tm);};
 auto firstmean=[&](const vector<P>&basis,int gid,int Tm){long long n=0;for(P e:basis){map<P,int>c;auto v=toggles(e,gid,Tm);for(auto x:v)c[x.first]+=x.second;for(auto [q,z0]:c)n+=1LL*z0*z0;}return red(n,1LL*basis.size()*Tm*Tm);};

 cout<<"{\n  \"version\":\"0.1\",\n  \"status\":\"EXACT_SECOND_ORDER_IDENTITY_MOTION\",\n  \"candidates\":{";
 bool first=1;
 for(auto [nm,gid]:cand){
   if(!first)cout<<",";first=0;int Tm=sper(A[gid]);int exposure=stepcost(gid)*Tm;
   Stat s1,s2,sp;
   for(P e:W1){auto r=k2single(e,gid,Tm);addstat(s1,r.n,r.d);}
   for(P e:W2){auto r=k2single(e,gid,Tm);addstat(s2,r.n,r.d);}
   for(int i=0;i<(int)WB.size();i++)for(int j=i+1;j<(int)WB.size();j++){auto r=k2pair(WB[i],WB[j],gid,Tm);addstat(sp,r.n,r.d);}
   auto m1=red(s1.sumN,s1.sumD*s1.count),m2=red(s2.sumN,s2.sumD*s2.count),mp=red(sp.sumN,sp.sumD*sp.count),a0=firstmean(W2,gid,Tm);
   double A0=sqrt((double)a0.n/a0.d),B=sqrt((double)mp.n/mp.d);double cross=B>0?(1.0-A0)/B:1e99;
   cout<<"\""<<nm<<"\":{\"signed_period\":"<<Tm<<",\"corrected_cycle_primitive_exposure\":"<<exposure<<",\"zeroth_w2_mean_norm2\":\""<<rs(a0)<<"\",";
   cout<<"\"K2_w1\":{\"zero\":"<<s1.zero<<",\"mean_norm2\":\""<<rs(m1)<<"\",\"max_norm2\":\""<<rs(red(s1.maxN,s1.maxD))<<"\"},";
   cout<<"\"K2_w2\":{\"zero\":"<<s2.zero<<",\"mean_norm2\":\""<<rs(m2)<<"\",\"max_norm2\":\""<<rs(red(s2.maxN,s2.maxD))<<"\"},";
   cout<<"\"K2_two_term_276\":{\"cases\":"<<sp.count<<",\"zero\":"<<sp.zero<<",\"mean_norm2\":\""<<rs(mp)<<"\",\"max_norm2\":\""<<rs(red(sp.maxN,sp.maxD))<<"\"},";
   cout<<"\"diagnostic_eta_cross\":"<<setprecision(17)<<cross<<"}";
 }
 cout<<"},\n  \"physical_promotion\":0\n}\n";
}
