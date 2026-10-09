#define main mqm_lc_hidden_main
#include "2026-10-09T1432Z_mqm_local_clifford_automorphism_v01a.cpp"
#undef main
#include <numeric>
using namespace std;
using VI=vector<int>;

struct Frac{long long n=0,d=1;Frac(){}Frac(long long a,long long b=1):n(a),d(b){long long g=std::gcd(llabs(n),d);if(g){n/=g;d/=g;}}};
string fs(Frac x){return x.d==1?to_string(x.n):to_string(x.n)+"/"+to_string(x.d);}

int main(){
 vector<string> gs={"IIIXXZZI","IIIYIYZZ","IIIXZIXZ","XXXXYYIX","XIIIIIII","ZIIIIIIZ","IXIIIIII","IZIIIIIZ","IIXIIIII","IIZIIIIZ"};
 vector<string> cs={"IIIXXZZI","IIIYIYZZ","IIIXZIXZ","XXXXYYIX"};
 vector<P> gen;for(auto&s:gs)gen.push_back(pv(s));auto Gv=spanv(gen);unordered_set<int>G;for(P x:Gv)G.insert(x);
 vector<P>C;for(auto&s:cs)C.push_back(pv(s));
 auto syndrome=[&](P e){int s=0,ex=e&255,ez=(e>>8)&255;for(int i=0;i<4;i++){int cx=C[i]&255,cz=(C[i]>>8)&255;int b=((__builtin_popcount(ex&cz)+__builtin_popcount(ez&cx))&1);s|=b<<i;}return s;};
 map<string,string> dl={{"1000","IIIIIYII"},{"1001","IIIIZIII"},{"1010","IIIIYIII"},{"1011","IIIYIIII"},{"1100","IIIIIIXI"},{"1101","IIIIIXII"},{"1110","IIIIIIYI"},{"1111","IIIZIIII"},{"0000","IIIIIIII"},{"0110","IIIIIIIX"},{"0111","IIIIIIIY"},{"0001","IIIIIIIZ"},{"0010","IIIIIIZI"},{"0100","IIIXIIII"},{"0101","IIIIIZII"},{"0011","IIIIXIII"}};
 array<P,16>D{};for(auto [k,v]:dl){int s=0;for(int i=0;i<4;i++)if(k[i]=='1')s|=1<<i;D[s]=pv(v);}
 P LX=pv("IIIYZIZI"),LZ=pv("IIIXIZIZ");
 auto fail=[&](P e){P r=e^D[syndrome(e)];int c=logical_class(r,G,LX,LZ);assert(c>=0);return c!=0;};

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
 int a=-1,b=-1;VI H1;
 for(int x:K)if(ord(A[x])==2){for(int y:K)if(ord(A[y])==3){if(ord(compose(A[x],A[y]))==4){auto H=sg({x,y},24);if(isS4(H)){a=x;b=y;H1=H;break;}}}if(a>=0)break;}
 VI Z;for(int g=0;g<(int)A.size();g++){bool ok=1;for(int h=0;h<(int)A.size();h++)if(mid(g,h)!=mid(h,g)){ok=0;break;}if(ok)Z.push_back(g);}assert(Z.size()==2);int z=Z[0]==eid?Z[1]:Z[0];
 auto eval=[&](string w){int x=eid;for(char c:w){int g=c=='a'?a:c=='b'?b:c=='z'?z:eid;x=mid(g,x);}return x;};
 map<string,int> cand={{"I",eid},{"a",a},{"b",b},{"ab",eval("ab")},{"zb",eval("zb")}};
 assert(ord(A[cand["a"]])==2&&ord(A[cand["b"]])==3&&ord(A[cand["ab"]])==4&&ord(A[cand["zb"]])==6);

 // minimum H/S words for each local phase-quotiented Clifford
 auto lmcomp=[&](int aa,int bb){int bx=LMS[bb].x1,bz=LMS[bb].z1;int ax=lmap(bx,LMS[aa]),az=lmap(bz,LMS[aa]);for(int k=0;k<6;k++)if(LMS[k].x1==ax&&LMS[k].z1==az)return k;return -1;};
 vector<int> ld(6,-1);vector<string> lw(6);queue<int>mq;ld[0]=0;lw[0]="";mq.push(0);int Hid=2,Sid=5;
 while(!mq.empty()){int u=mq.front();mq.pop();for(auto [g,ch]:vector<pair<int,char>>{{Hid,'H'},{Sid,'S'}}){int v=lmcomp(g,u);if(ld[v]<0){ld[v]=ld[u]+1;lw[v]=lw[u]+ch;mq.push(v);}}}

 auto sax=[&](int axis,const string&w){int sign=1,a0=axis;for(char c:w){if(c=='H'){if(a0==1)a0=2;else if(a0==2)a0=1;else sign=-sign;}else{if(a0==1)a0=3;else if(a0==3){a0=1;sign=-sign;}}}return pair<int,int>(a0,sign);};
 auto sapply=[&](P v,const T&t){int x=v&255,zz=(v>>8)&255,nx=0,nz=0,sgn=1;for(int q=0;q<8;q++){int ax=((x>>q)&1)|(((zz>>q)&1)<<1);if(!ax)continue;auto [ao,ss]=sax(ax,lw[t.m[q]]);sgn*=ss;int j=t.p[q];if(ao&1)nx|=1<<j;if(ao&2)nz|=1<<j;}return tuple<P,int>(P(nx|(nz<<8)),sgn);};

 vector<P> W1,W2;
 for(int q=0;q<8;q++)for(char c:string("XYZ")){string s(8,'I');s[q]=c;W1.push_back(pv(s));}
 for(int i=0;i<8;i++)for(int j=i+1;j<8;j++)for(char a0:string("XYZ"))for(char b0:string("XYZ")){string s(8,'I');s[i]=a0;s[j]=b0;W2.push_back(pv(s));}
 assert(W1.size()==24&&W2.size()==252);

 auto signed_period=[&](const T&t){for(int k=1;k<=48;k++){bool ok=1;for(P e:W1){P x=e;int sg=1;for(int q=0;q<k;q++){auto [y,s]=sapply(x,t);x=y;sg*=s;}if(x!=e||sg!=1){ok=0;break;}}if(ok)return k;}return 0;};
 struct Coh{int period=0,rank=0,zero=0;long long norm_num=0,norm_den=1;};
 auto coherent=[&](const vector<P>&basis,const T&t){
   Coh c;c.period=signed_period(t);unordered_set<P>seen;
   for(P e:basis){
     map<P,int>sum;P x=e;int sg=1;
     for(int k=0;k<c.period;k++){sum[x]+=sg;auto [y,s]=sapply(x,t);x=y;sg*=s;}
     long long n2=0;for(auto [q,v]:sum)n2+=1LL*v*v;
     if(n2==0)c.zero++;
     c.norm_num+=n2;
     if(!seen.count(e)){
       vector<P>orb;P y=e;int ss=1;int prod=1;
       do{orb.push_back(y);seen.insert(y);auto [yy,s]=sapply(y,t);y=yy;prod*=s;}while(y!=e);
       if(prod==1)c.rank++;
     }
   }
   c.norm_den=1LL*basis.size()*c.period*c.period;
   long long g=std::gcd(c.norm_num,c.norm_den);c.norm_num/=g;c.norm_den/=g;
   return c;
 };
 struct Sto{int improved=0,worsened=0,equal=0;long long sum_num=0;int den=1;map<int,int> orbit_hist;map<string,Frac> fam;};
 auto stochastic=[&](int gid){
   Sto s;int T=ord(A[gid]);s.den=T*252;
   map<string,pair<long long,long long>> fa; string axes="XYZ";
   for(P e:W2){
     int base=fail(e),bad=0;set<P>orb;P x=e;
     for(int t=0;t<T;t++){bad+=fail(x);orb.insert(x);x=applyT(x,A[gid]);}
     s.orbit_hist[orb.size()]++;s.sum_num+=bad;
     if(bad<base*T)s.improved++;else if(bad>base*T)s.worsened++;else s.equal++;
   }
   // 9 fixed-Pauli-type families averaged over 28 pairs and clock phase
   for(char aa:axes)for(char bb:axes){
     string nm;nm+=aa;nm+=bb;long long bad=0,tot=0;
     for(int i=0;i<8;i++)for(int j=i+1;j<8;j++){
       string st(8,'I');st[i]=aa;st[j]=bb;P x=pv(st);
       for(int t=0;t<T;t++){bad+=fail(x);tot++;x=applyT(x,A[gid]);}
     }
     fa[nm]={bad,tot};
   }
   for(auto [nm,v]:fa)s.fam[nm]=Frac(v.first,v.second);
   return s;
 };
 auto primitive_cost=[&](int gid){int local=0,cyc=0;vector<int>vis(8);for(int i=0;i<8;i++)local+=ld[A[gid].m[i]];for(int i=0;i<8;i++)if(!vis[i]){cyc++;int j=i;while(!vis[j]){vis[j]=1;j=A[gid].p[j];}}int sw=8-cyc;return local+3*sw;};

 cout<<"{\n  \"version\":\"0.1\",\n  \"status\":\"EXACT_IDENTITY_MOTION_DYNAMICAL_BENCHMARK\",\n  \"candidates\":{";
 bool first=1;
 for(auto [nm,gid]:cand){
   if(!first)cout<<",";first=0;Coh c1=coherent(W1,A[gid]),c2=coherent(W2,A[gid]);Sto st=stochastic(gid);int pc=primitive_cost(gid);int fo=ord(A[gid]);
   cout<<"\""<<nm<<"\":{\"frame_order\":"<<fo<<",\"signed_period\":"<<c1.period<<",\"cycle_primitive_exposure\":"<<pc*fo;
   cout<<",\"coherent_w1\":{\"rank\":"<<c1.rank<<",\"zeroed_basis\":"<<c1.zero<<",\"mean_norm2\":\""<<c1.norm_num<<"/"<<c1.norm_den<<"\"}";
   cout<<",\"coherent_w2\":{\"rank\":"<<c2.rank<<",\"zeroed_basis\":"<<c2.zero<<",\"mean_norm2\":\""<<c2.norm_num<<"/"<<c2.norm_den<<"\"}";
   cout<<",\"stochastic_w2\":{\"improved\":"<<st.improved<<",\"worsened\":"<<st.worsened<<",\"equal\":"<<st.equal<<",\"global_bad_mean\":\""<<st.sum_num<<"/"<<st.den<<"\",\"orbit_hist\":{";
   bool f=0;for(auto [k,v]:st.orbit_hist){if(f)cout<<",";f=1;cout<<"\""<<k<<"\":"<<v;}cout<<"},\"families\":{";
   f=0;for(auto [k,v]:st.fam){if(f)cout<<",";f=1;cout<<"\""<<k<<"\":\""<<fs(v)<<"\"";}cout<<"}}}";
 }
 cout<<"},\n  \"loss_rule\":\"For independent primitive loss ell>0, physical-cycle survival is (1-ell)^N with N=cycle_primitive_exposure; virtual frame tracking adds N=0.\",\n  \"physical_promotion\":0\n}\n";
}
