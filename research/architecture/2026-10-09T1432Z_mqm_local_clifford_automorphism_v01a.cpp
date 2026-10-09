#include <bits/stdc++.h>
using namespace std;
using P=uint16_t;
P pv(const string&s){int x=0,z=0;for(int i=0;i<8;i++){if(s[i]=='X'||s[i]=='Y')x|=1<<i;if(s[i]=='Z'||s[i]=='Y')z|=1<<i;}return P(x|(z<<8));}
int supp(P v){return (v&255)|((v>>8)&255);}
vector<P> spanv(vector<P> g){vector<P>a={0};for(P v:g){int n=a.size();for(int i=0;i<n;i++)a.push_back(a[i]^v);}sort(a.begin(),a.end());a.erase(unique(a.begin(),a.end()),a.end());return a;}
struct LM{int x1,z1;}; // images of X,Z in {1=X,2=Z,3=Y}
vector<LM> LMS={{1,2},{1,3},{2,1},{2,3},{3,1},{3,2}};
int lmap(int v,const LM&m){if(v==0)return 0;if(v==1)return m.x1;if(v==2)return m.z1;return m.x1^m.z1;}
struct T{array<uint8_t,8> p,m;};
P applyT(P v,const T&t){int x=v&255,z=(v>>8)&255,nx=0,nz=0;for(int q=0;q<8;q++){int a=((x>>q)&1)|(((z>>q)&1)<<1);int b=lmap(a,LMS[t.m[q]]);int j=t.p[q];if(b&1)nx|=1<<j;if(b&2)nz|=1<<j;}return P(nx|(nz<<8));}
T compose(const T&a,const T&b){ // a after b
 T c;
 for(int q=0;q<8;q++){
   int mid=b.p[q], dst=a.p[mid]; c.p[q]=dst;
   int bx=lmap(1,LMS[b.m[q]]), bz=lmap(2,LMS[b.m[q]]);
   int ax=lmap(bx,LMS[a.m[mid]]), az=lmap(bz,LMS[a.m[mid]]);
   int id=-1;for(int k=0;k<6;k++)if(LMS[k].x1==ax&&LMS[k].z1==az){id=k;break;}
   c.m[q]=id;
 }
 return c;
}
bool eq(const T&a,const T&b){return a.p==b.p&&a.m==b.m;}
T ident(){T t;for(int i=0;i<8;i++){t.p[i]=i;t.m[i]=0;}return t;} // LMS[0] X->X,Z->Z
int ord(const T&t){T x=ident();for(int k=1;k<=120;k++){x=compose(t,x);if(eq(x,ident()))return k;}return 0;}
string key(const T&t){string s;for(int i=0;i<8;i++){s.push_back(char(t.p[i]));s.push_back(char(t.m[i]));}return s;}
int logical_class(P v,const unordered_set<int>&G,P LX,P LZ){
 for(int k=0;k<4;k++){P l=k==0?0:k==1?LX:k==2?LZ:(LX^LZ);if(G.count(v^l))return k;}return -1;
}
int main(){
 vector<string> gs={"IIIXXZZI","IIIYIYZZ","IIIXZIXZ","XXXXYYIX","XIIIIIII","ZIIIIIIZ","IXIIIIII","IZIIIIIZ","IIXIIIII","IIZIIIIZ"};
 vector<P> gen;for(auto&s:gs)gen.push_back(pv(s));auto Gv=spanv(gen);unordered_set<int>G;for(P x:Gv)G.insert(x);
 vector<int> sc(256);for(P x:Gv)sc[supp(x)]++;
 vector<array<uint8_t,8>> perms;array<uint8_t,8> p={0,1,2,3,4,5,6,7};
 do{
   bool ok=1;
   for(int m=0;m<256&&ok;m++)if(sc[m]){
     int y=0;for(int i=0;i<8;i++)if(m>>i&1)y|=1<<p[i];
     if(sc[y]!=sc[m])ok=0;
   }
   if(ok)perms.push_back(p);
 }while(next_permutation(p.begin(),p.end()));
 cerr<<"support automorphisms "<<perms.size()<<"\n";
 vector<T> A; const int N=1679616; // 6^8
 for(auto &pp:perms){
   for(int code=0;code<N;code++){
     int q=code;T t;t.p=pp;for(int i=0;i<8;i++){t.m[i]=q%6;q/=6;}
     bool ok=1;for(P g:gen)if(!G.count(applyT(g,t))){ok=0;break;}
     if(ok)A.push_back(t);
   }
 }
 cerr<<"LC automorphisms "<<A.size()<<"\n";
 P LX=pv("IIIYZIZI"),LZ=pv("IIIXIZIZ");
 map<int,long long> os;map<pair<int,int>,long long> la;
 for(auto&t:A){os[ord(t)]++;la[make_pair(logical_class(applyT(LX,t),G,LX,LZ),logical_class(applyT(LZ,t),G,LX,LZ))]++;}
 // Candidate group reopening tests from element orders, plus exact A4 witness search when feasible.
 bool has4=os.count(4),has5=os.count(5);
 bool A4=false,S4=false,A5=false;
 unordered_map<string,int> idx;idx.reserve(A.size()*2);for(int i=0;i<(int)A.size();i++)idx[key(A[i])]=i;
 auto subgroup_size=[&](int ia,int ib,int cap){
   unordered_set<int>S;queue<int>Q;S.insert(0);
   // identity index
   int iid=idx[key(ident())];S.clear();S.insert(iid);Q.push(iid);
   vector<int> gens={ia,ib};
   while(!Q.empty()&&S.size()<=size_t(cap)){int u=Q.front();Q.pop();for(int g:gens){T z=compose(A[g],A[u]);auto it=idx.find(key(z));if(it==idx.end())return cap+1;int v=it->second;if(S.insert(v).second)Q.push(v);}}
   return (int)S.size();
 };
 vector<int> o2,o3,o4,o5;for(int i=0;i<(int)A.size();i++){int o=ord(A[i]);if(o==2)o2.push_back(i);if(o==3)o3.push_back(i);if(o==4)o4.push_back(i);if(o==5)o5.push_back(i);}
 // Search witnesses; if absent reports only "not found" unless order obstruction proves no-go.
 for(int a:o2){for(int b:o3){int op=ord(compose(A[a],A[b]));if(!A4&&op==3&&subgroup_size(a,b,12)==12)A4=true;if(!S4&&op==4&&subgroup_size(a,b,24)==24)S4=true;if(!A5&&op==5&&subgroup_size(a,b,60)==60)A5=true;if(A4&&S4&&A5)break;}if(A4&&S4&&A5)break;}
 cout<<"{\n";
 cout<<"  \"version\":\"0.1\",\n  \"status\":\"EXACT_MONOMIAL_LOCAL_CLIFFORD_AUTOMORPHISM_ENUMERATION\",\n";
 cout<<"  \"support_permutation_candidates\":"<<perms.size()<<",\n  \"automorphism_group_size\":"<<A.size()<<",\n";
 cout<<"  \"element_order_spectrum\":{";bool f=0;for(auto [k,v]:os){if(f)cout<<",";f=1;cout<<"\""<<k<<"\":"<<v;}cout<<"},\n";
 cout<<"  \"logical_action_pairs\":{";f=0;for(auto [k,v]:la){if(f)cout<<",";f=1;cout<<"\""<<k.first<<","<<k.second<<"\":"<<v;}cout<<"},\n";
 cout<<"  \"candidate_shell_reopening\":{\n";
 cout<<"    \"A4\":{\"witness_subgroup_found\":"<<(A4?"true":"false")<<"},\n";
 cout<<"    \"S4\":{\"witness_subgroup_found\":"<<(S4?"true":"false")<<",\"order4_obstruction\":"<<(!has4?"true":"false")<<"},\n";
 cout<<"    \"A5\":{\"witness_subgroup_found\":"<<(A5?"true":"false")<<",\"order5_obstruction\":"<<(!has5?"true":"false")<<"}\n  },\n";
 cout<<"  \"physical_promotion\":0\n}\n";
}
