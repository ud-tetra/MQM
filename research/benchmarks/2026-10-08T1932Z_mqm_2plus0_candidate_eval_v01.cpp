#define main mqm_parent_hidden_main
#include "mqm_full_stochastic_tail_v01.cpp"
#undef main

int main(){
    init_code();
    Proto pr=make_proto("2+0",2,0);
    vector<double> rates={0,ldexp(1.0,-21),ldexp(1.0,-19),ldexp(1.0,-17),ldexp(1.0,-15)};
    const int SHOTS=200000; const double alpha=1.0/3000000.0;
    double h=sqrt(log(2/alpha)/(2.0*SHOTS)); uint64_t master=0x4D514D5F32303236ULL;
    array<string,7> mn={"Y","HOLD","QUARANTINE","L_AND_ACCEPT","ACCEPT_DW1","Y_CLEAN","Y_GOOD"};
    ofstream out("/mnt/data/mqm_full/MQM_2PLUS0_CANDIDATE_RESULTS_v0.1.json");
    out<<"{\n\"version\":\"0.1\",\"status\":\"POSTEXPOSURE_EXPLORATORY_2PLUS0\",\"locations\":{\"p\":"<<pr.Np<<",\"q\":"<<pr.Nq<<",\"l\":"<<pr.Nl<<"},\"tail_shots\":"<<SHOTS<<",\"hoeffding_conditional_halfwidth\":"<<setprecision(17)<<h<<",\"single_raw\":{";
    // exact single raw summaries
    for(int k=0;k<7;k++){if(k)out<<",";out<<"\""<<mn[k]<<"\":{\"f0\":"<<pr.raw[k].f0<<",\"sp\":"<<pr.raw[k].sp<<",\"sq\":"<<pr.raw[k].sq<<",\"sl\":"<<pr.raw[k].sl<<"}";}
    out<<"},\"pair_raw\":{";
    for(int k=0;k<7;k++){if(k)out<<",";out<<"\""<<mn[k]<<"\":{\"spp\":"<<pr.raw[k].spp<<",\"spq\":"<<pr.raw[k].spq<<",\"spl\":"<<pr.raw[k].spl<<",\"sqq\":"<<pr.raw[k].sqq<<",\"sql\":"<<pr.raw[k].sql<<",\"sll\":"<<pr.raw[k].sll<<"}";}
    out<<"},\"grid\":[";
    bool first=true;
    for(int ip=0;ip<5;ip++)for(int iq=0;iq<5;iq++)for(int il=0;il<5;il++){
        double p=rates[ip],q=rates[iq],l=rates[il]; CountSampler cs(pr.Np,pr.Nq,pr.Nl,p,q,l);
        array<double,7> low{},est{},lo{},hi{}; for(int k=0;k<7;k++)low[k]=lowprob(pr.raw[k],pr.Np,pr.Nq,pr.Nl,p,q,l);
        array<long long,7> cnt{};
        if(cs.tail>0){uint64_t seed=splitmix64(master^uint64_t(4)^((uint64_t)ip<<8)^((uint64_t)iq<<16)^((uint64_t)il<<24)); mt19937_64 rng(seed); vector<int>a,b,c; uniform_int_distribution<int>u3(0,2),u15(0,14);
            for(int s=0;s<SHOTS;s++){int N=cs.sampleN(rng);auto[kp,kq,kl]=cs.sampleComp(N,rng);sample_distinct(pr.ip,kp,rng,a);sample_distinct(pr.iq,kq,rng,b);sample_distinct(pr.il,kl,rng,c);Comb comb;for(int idx:a){auto&ls=pr.ls[idx];int rr=ls.loc.rcount==15?u15(rng):u3(rng);add_event(comb,ls,rr,pr.acq);}for(int idx:b)add_event(comb,pr.ls[idx],0,pr.acq);for(int idx:c)add_event(comb,pr.ls[idx],0,pr.acq);auto m=mv(classify(pr.acq,pr.ver,comb));for(int k=0;k<7;k++)cnt[k]+=m[k];}
        }
        for(int k=0;k<7;k++){double frac=cs.tail?double(cnt[k])/SHOTS:0;est[k]=low[k]+cs.tail*frac;double d=cs.tail*h;lo[k]=max(0.0,est[k]-d);hi[k]=min(1.0,est[k]+d);}double eps=est[0]>0?est[3]/est[0]:0;double epslo=lo[3]/(hi[0]>0?hi[0]:1);double epshi=(lo[0]>0)?hi[3]/lo[0]:1;double r1=est[0]>0?est[4]/est[0]:0;double good=est[6];
        if(!first)out<<",";first=false;out<<"{\"i\":["<<ip<<","<<iq<<","<<il<<"],\"rates\":["<<jnum(p)<<","<<jnum(q)<<","<<jnum(l)<<"],\"tail\":"<<jnum(cs.tail)<<",\"metrics\":{";for(int k=0;k<7;k++){if(k)out<<",";out<<"\""<<mn[k]<<"\":{\"v\":"<<jnum(est[k])<<",\"lo\":"<<jnum(lo[k])<<",\"hi\":"<<jnum(hi[k])<<"}";}out<<",\"EPSILON_L_GIVEN_A\":{\"v\":"<<jnum(eps)<<",\"lo\":"<<jnum(epslo)<<",\"hi\":"<<jnum(epshi)<<"},\"R1_GIVEN_A\":{\"v\":"<<jnum(r1)<<"},\"GATES_PER_GOOD\":{\"v\":"<<jnum(78/good)<<"},\"MEAS_PER_GOOD\":{\"v\":"<<jnum(28/good)<<"}}}";
    }
    out<<"],\"physical_promotion\":0}\n";out.close();
    cerr<<"done 2+0\n";
}