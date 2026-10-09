#define main mqm_lc_hidden_main
#include "2026-10-09T1432Z_mqm_local_clifford_automorphism_v01a.cpp"
#undef main
#include <numeric>
using namespace std;

int logical_order(pair<int,int> p){
    int X=p.first,Z=p.second;
    int Y=6-X-Z; // labels are 1,2,3 and images are distinct
    array<int,4> f{};f[1]=X;f[2]=Z;f[3]=Y;
    array<int,4> g={0,1,2,3};
    for(int k=1;k<=3;k++){
        array<int,4> h{};for(int a=1;a<=3;a++)h[a]=f[g[a]];
        g=h;
        if(g[1]==1&&g[2]==2&&g[3]==3)return k;
    }
    return 0;
}
string logical_type(pair<int,int> p){
    int o=logical_order(p);
    if(o==1)return "identity";
    if(o==2)return "axis_transposition";
    return "axis_3cycle";
}
int main(){
    vector<string> gs={"IIIXXZZI","IIIYIYZZ","IIIXZIXZ","XXXXYYIX","XIIIIIII","ZIIIIIIZ","IXIIIIII","IZIIIIIZ","IIXIIIII","IIZIIIIZ"};
    vector<P> gen;for(auto&s:gs)gen.push_back(pv(s));auto Gv=spanv(gen);unordered_set<int>G;for(P x:Gv)G.insert(x);
    vector<int> sc(256);for(P x:Gv)sc[supp(x)]++;
    vector<array<uint8_t,8>> perms;array<uint8_t,8> p={0,1,2,3,4,5,6,7};
    do{
        bool ok=1;for(int m=0;m<256&&ok;m++)if(sc[m]){
            int y=0;for(int i=0;i<8;i++)if(m>>i&1)y|=1<<p[i];
            if(sc[y]!=sc[m])ok=0;
        }
        if(ok)perms.push_back(p);
    }while(next_permutation(p.begin(),p.end()));
    vector<T>A;const int N=1679616;
    for(auto &pp:perms)for(int code=0;code<N;code++){
        int q=code;T t;t.p=pp;for(int i=0;i<8;i++){t.m[i]=q%6;q/=6;}
        bool ok=1;for(P g:gen)if(!G.count(applyT(g,t))){ok=0;break;}
        if(ok)A.push_back(t);
    }
    P LX=pv("IIIYZIZI"),LZ=pv("IIIXIZIZ");
    map<pair<int,int>,long long> joint;map<string,long long> typecount;
    map<int,long long> hidden_ratio;
    for(auto&t:A){
        int fo=ord(t);
        auto lp=make_pair(logical_class(applyT(LX,t),G,LX,LZ),logical_class(applyT(LZ,t),G,LX,LZ));
        int lo=logical_order(lp);
        joint[{fo,lo}]++;
        typecount[logical_type(lp)]++;
        hidden_ratio[fo/lo]++;
    }
    long long sum=0;for(auto &x:joint)sum+=x.second;assert(sum==1152);
    assert(typecount["identity"]==192&&typecount["axis_transposition"]==576&&typecount["axis_3cycle"]==384);
    cout<<"{\n  \"version\":\"0.1\",\n  \"status\":\"EXACT_SHAPE_MOTION_SEMANTICS_ENUMERATION\",\n";
    cout<<"  \"group_order\":1152,\n";
    cout<<"  \"logical_motion_types\":{";
    bool f=0;for(auto &x:typecount){if(f)cout<<",";f=1;cout<<"\""<<x.first<<"\":"<<x.second;}cout<<"},\n";
    cout<<"  \"joint_full_order_logical_order\":{";
    f=0;for(auto &x:joint){if(f)cout<<",";f=1;cout<<"\""<<x.first.first<<","<<x.first.second<<"\":"<<x.second;}cout<<"},\n";
    cout<<"  \"hidden_frame_period_ratio\":{";
    f=0;for(auto &x:hidden_ratio){if(f)cout<<",";f=1;cout<<"\""<<x.first<<"\":"<<x.second;}cout<<"},\n";
    cout<<"  \"logical_periods\":[1,2,3],\n  \"full_frame_periods\":[1,2,3,4,6,12],\n";
    cout<<"  \"physical_promotion\":0\n}\n";
}
