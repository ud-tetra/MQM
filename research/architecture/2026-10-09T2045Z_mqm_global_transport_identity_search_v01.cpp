#define main mqm_lc_hidden_main
#include "2026-10-09T1432Z_mqm_local_clifford_automorphism_v01a.cpp"
#undef main
#include <numeric>
using namespace std; using VI=vector<int>;

long long GCD(long long a,long long b){return std::gcd(llabs(a),llabs(b));}
string rat(long long n,long long d){long long g=GCD(n,d);n/=g;d/=g;return d==1?to_string(n):to_string(n)+"/"+to_string(d);}

int main(){
 vector<string> gs={"IIIXXZZI","IIIYIYZZ","IIIXZIXZ","XXXXYYIX","XIIIIIII","ZIIIIIIZ","IXIIIIII","IZIIIIIZ","IIXIIIII","IIZIIIIZ"};
 vector<P> gen;for(auto&s:gs)gen.push_back(pv(s));auto Gv=spanv(gen);unordered_set<int>G;for(P x:Gv)G.insert(x);
 vector<int> sc(256);for(P x:Gv)sc[supp(x)]++;
 vector<array<uint8_t,8>> perms;array<uint8_t,8> p={0,1,2,3,4,5,6,7};
 do{bool ok=1;for(int m=0;m<256&&ok;m++)if(sc[m]){int y=0;for(int i=0;i<8;i++)if(m>>i&1)y|=1<<p[i];if(sc[y]!=sc[m])ok=0;}if(ok)perms.push_back(p);}while(next_permutation(p.begin(),p.end()));
 vector<T>A;const int N=1679616;for(auto &pp:perms)for(int code=0;code<N;code++){int q=code;T t;t.p=pp;for(int i=0;i<8;i++){t.m[i]=q%6;q/=6;}bool ok=1;for(P g:gen)if(!G.count(applyT(g,t))){ok=0;break;}if(ok)A.push_back(t);}
 P LX=pv("IIIYZIZI"),LZ=pv("IIIXIZIZ");
 auto lp=[&](int i){return make_pair(logical_class(applyT(LX,A[i]),G,LX,LZ),logical_class(applyT(LZ,A[i]),G,LX,LZ));};
 VI K;for(int i=0;i<(int)A.size();i++)if(lp(i)==make_pair(1,2))K.push_back(i);assert(K.size()==192);

 auto lmcomp=[&](int aa,int bb){int bx=LMS[bb].x1,bz=LMS[bb].z1;int ax=lmap(bx,LMS[aa]),az=lmap(bz,LMS[aa]);for(int k=0;k<6;k++)if(LMS[k].x1==ax&&LMS[k].z1==az)return k;return -1;};
 vector<int> ld(6,-1);vector<string> lw(6);queue<int>mq;ld[0]=0;lw[0]="";mq.push(0);int H=2,S=5;
 while(!mq.empty()){int u=mq.front();mq.pop();for(auto [g,ch]:vector<pair<int,char>>{{H,'H'},{S,'S'}}){int v=lmcomp(g,u);if(ld[v]<0){ld[v]=ld[u]+1;lw[v]=lw[u]+ch;mq.push(v);}}}
 auto sax=[&](int axis,const string&w){int sign=1,a0=axis;for(char ch:w){if(ch=='H'){if(a0==1)a0=2;else if(a0==2)a0=1;else sign=-sign;}else{if(a0==1)a0=3;else if(a0==3){a0=1;sign=-sign;}}}return pair<int,int>(a0,sign);};
 auto sapply=[&](P v0,const T&t){int x=v0&255,z=(v0>>8)&255,nx=0,nz=0,sg=1;for(int q=0;q<8;q++){int ax=((x>>q)&1)|(((z>>q)&1)<<1);if(!ax)continue;auto [ao,ss]=sax(ax,lw[t.m[q]]);sg*=ss;int j=t.p[q];if(ao&1)nx|=1<<j;if(ao&2)nz|=1<<j;}return pair<P,int>(P(nx|(nz<<8)),sg);};
 vector<P> W1,W2;for(int q=0;q<8;q++)for(char c:string("XYZ")){string st(8,'I');st[q]=c;W1.push_back(pv(st));}
 for(int i=0;i<8;i++)for(int j=i+1;j<8;j++)for(char a:string("XYZ"))for(char b:string("XYZ")){string st(8,'I');st[i]=a;st[j]=b;W2.push_back(pv(st));}
 auto sper=[&](int id){for(int T=1;T<=24;T++){bool ok=1;for(P e:W1){P x=e;int sg=1;for(int t=0;t<T;t++){auto y=sapply(x,A[id]);x=y.first;sg*=y.second;}if(x!=e||sg!=1){ok=0;break;}}if(ok)return T;}return 0;};
 auto a0=[&](int id,int T){long long n=0;for(P e:W2){map<P,int>c;P x=e;int sg=1;for(int t=0;t<T;t++){c[x]+=sg;auto y=sapply(x,A[id]);x=y.first;sg*=y.second;}for(auto [q,v]:c)n+=1LL*v*v;}return pair<long long,long long>(n,252LL*T*T);};
 struct R{int id,T,moved,wordH,wordS;string cls,word,a0s;double a0v;};
 vector<R> rows;
 for(int id:K){
   bool pure=1,uni=1;for(int q=0;q<8;q++){pure&=A[id].m[q]==0;uni&=A[id].m[q]==A[id].m[0];}
   if(!pure&&!uni)continue;
   int moved=0;for(int q=0;q<8;q++)moved+=A[id].p[q]!=q;
   int T=sper(id);auto [n,d]=a0(id,T);string w=uni?lw[A[id].m[0]]:"";int nh=count(w.begin(),w.end(),'H'),ns=count(w.begin(),w.end(),'S');
   rows.push_back({id,T,moved,nh,ns,pure?"transport_only":"global_uniform",w.empty()?"I":w,rat(n,d),(double)n/d});
 }
 sort(rows.begin(),rows.end(),[](R a,R b){return tie(a.a0v,a.moved,a.wordH,a.wordS,a.id)<tie(b.a0v,b.moved,b.wordH,b.wordS,b.id);});
 // Pareto on a0, moved-role exposure, GR-cycle count, Rz-layer-cycle count.
 auto dom=[&](R a,R b){int am=a.moved*a.T,bm=b.moved*b.T,ag=a.wordH*a.T,bg=b.wordH*b.T,ar=(a.wordH+a.wordS)*a.T,br=(b.wordH+b.wordS)*b.T;bool le=a.a0v<=b.a0v&&am<=bm&&ag<=bg&&ar<=br;bool st=a.a0v<b.a0v||am<bm||ag<bg||ar<br;return le&&st;};
 vector<R> front;for(auto r:rows){bool d=0;for(auto q:rows)if(q.id!=r.id&&dom(q,r)){d=1;break;}if(!d)front.push_back(r);}
 cout<<"{\n  \"version\":\"0.1\",\n  \"status\":\"EXACT_GLOBAL_TRANSPORT_IDENTITY_SEARCH\",\n  \"candidate_count\":"<<rows.size()<<",\n  \"rows\":[";
 for(int i=0;i<(int)rows.size();i++){auto r=rows[i];if(i)cout<<",";cout<<"{\"id\":"<<r.id<<",\"class\":\""<<r.cls<<"\",\"signed_period\":"<<r.T<<",\"moved_roles_per_step\":"<<r.moved<<",\"moved_role_exposure\":"<<r.moved*r.T<<",\"uniform_local_word\":\""<<r.word<<"\",\"global_GR_per_cycle\":"<<r.wordH*r.T<<",\"global_Rz_layers_per_cycle\":"<<(r.wordH+r.wordS)*r.T<<",\"zeroth_w2\":\""<<r.a0s<<"\"}";}
 cout<<"],\n  \"pareto_ids\":[";
 for(int i=0;i<(int)front.size();i++){if(i)cout<<",";cout<<front[i].id;}
 cout<<"],\n  \"physical_promotion\":0\n}\n";
}
