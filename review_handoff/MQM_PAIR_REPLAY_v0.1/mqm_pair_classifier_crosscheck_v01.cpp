#define main mqm_full_tail_hidden_main
#include "mqm_full_stochastic_tail_v01.cpp"
#undef main

int main(){
    init_code();
    vector<tuple<string,int,int>> defs={{"1+0",1,0},{"2+1",2,1},{"3+1",3,1}};
    array<string,7> names={"Y","HOLD","QUARANTINE","L_AND_ACCEPT","ACCEPT_DW1","Y_CLEAN","Y_GOOD"};
    cout << "{\n  \"version\":\"0.1\",\n  \"status\":\"SEPARATE_PSTRUCT_FAULT_PAIR_CLASSIFIER\",\n  \"protocols\":{\n";
    bool fp=true;
    for(auto [name,a,v]:defs){
        auto p=make_proto(name,a,v);
        if(!fp) cout<<",\n"; fp=false;
        cout<<"    \""<<name<<"\":{\"locations\":{\"p\":"<<p.Np<<",\"q\":"<<p.Nq<<",\"l\":"<<p.Nl<<"},\"raw\":{";
        for(int k=0;k<7;k++){
            if(k) cout<<",";
            auto&r=p.raw[k];
            cout<<"\""<<names[k]<<"\":{"
                <<"\"f0\":"<<setprecision(17)<<r.f0<<","<<"\"sp\":"<<r.sp<<","<<"\"sq\":"<<r.sq<<","<<"\"sl\":"<<r.sl<<","<<"\"spp\":"<<r.spp<<","<<"\"spq\":"<<r.spq<<","<<"\"spl\":"<<r.spl<<","<<"\"sqq\":"<<r.sqq<<","<<"\"sql\":"<<r.sql<<","<<"\"sll\":"<<r.sll<<"}";
        }
        cout<<"}}";
    }
    cout<<"\n  },\n  \"notes\":\"Reconstructs circuits and pair labels without reading primary raw aggregates. Uses explicit Pauli{x,z} representation.\"\n}\n";
}