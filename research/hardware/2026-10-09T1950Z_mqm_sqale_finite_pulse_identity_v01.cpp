#include <bits/stdc++.h>
using namespace std;
using cd=complex<double>;
const int NQ=8,D=256;
struct Cnt{long long gr=0,rz=0,cz=0; double tpar=0,tser=0;};
struct Sim{vector<cd> U;Cnt c;bool actual;Sim(bool a):U(D*D),actual(a){for(int i=0;i<D;i++)U[i*D+i]=1.0;}};
void oneq(Sim&s,int q,cd a,cd b,cd c,cd d){
  int bit=1<<q;
  for(int base=0;base<D;base++)if(!(base&bit)){
    int r0=base,r1=base|bit;
    for(int col=0;col<D;col++){
      cd x=s.U[r0*D+col],y=s.U[r1*D+col];
      s.U[r0*D+col]=a*x+b*y;s.U[r1*D+col]=c*x+d*y;
    }
  }
}
void rz_site(Sim&s,int q,double th){
  s.c.rz++;
  double t=abs(th)/M_PI*0.25; s.c.tser+=t;
  double x=s.actual?1.012*th:th;
  cd a=exp(cd(0,-x/2)),d=exp(cd(0,x/2));oneq(s,q,a,0,0,d);
}
void rz_layer(Sim&s,const vector<int>&qs,double th){
  if(qs.empty())return;
  double t=abs(th)/M_PI*0.25;s.c.tpar+=t;
  for(int q:qs)rz_site(s,q,th);
}
void gr_y(Sim&s,double th){
  s.c.gr++;
  double t=abs(th)/M_PI*4.1;s.c.tpar+=t;s.c.tser+=t;
  double x=s.actual?th+0.0345:th;
  double C=cos(x/2),S=sin(x/2);
  for(int q=0;q<NQ;q++)oneq(s,q,C,-S,S,C);
}
void cz(Sim&s,int q1,int q2){
  s.c.cz++;s.c.tpar+=0.416;s.c.tser+=0.416;
  int b1=1<<q1,b2=1<<q2;for(int r=0;r<D;r++)if((r&b1)&&(r&b2))for(int col=0;col<D;col++)s.U[r*D+col]*=-1.0;
}
void Hsel(Sim&s,vector<int>T){
  sort(T.begin(),T.end());vector<int>S;for(int q=0;q<NQ;q++)if(!binary_search(T.begin(),T.end(),q))S.push_back(q);
  rz_layer(s,T,M_PI);
  gr_y(s,M_PI/4);
  rz_layer(s,S,M_PI);
  gr_y(s,M_PI/4);
  rz_layer(s,S,-M_PI);
}
void Slay(Sim&s,const vector<int>&T){rz_layer(s,T,M_PI/2);}
void HSH(Sim&s,const vector<int>&T){Hsel(s,T);Slay(s,T);Hsel(s,T);}
void cnot(Sim&s,int c,int t){Hsel(s,{t});cz(s,c,t);Hsel(s,{t});}
void swp(Sim&s,int a,int b){cnot(s,a,b);cnot(s,b,a);cnot(s,a,b);}
void step(Sim&s,string nm){
  if(nm=="I")return;
  if(nm=="a"){swp(s,1,2);return;} // one-based (2 3)
  if(nm=="b"){HSH(s,{0,1});swp(s,0,1);swp(s,0,2);return;} // (1 2 3)
  if(nm=="zb"){HSH(s,{2});swp(s,0,1);swp(s,0,2);return;}
  abort();
}
double favg(const vector<cd>&A,const vector<cd>&B){
  cd tr=0;for(size_t i=0;i<A.size();i++)tr+=conj(A[i])*B[i];
  double x=norm(tr);return (x+D)/(double(D)*(D+1));
}
double globalphase_identity_error(const vector<cd>&A){
  cd tr=0;for(int i=0;i<D;i++)tr+=A[i*D+i];
  return 1.0-((norm(tr)+D)/(double(D)*(D+1)));
}
int main(){
  map<string,int> T={{"I",1},{"a",2},{"b",6},{"zb",12}};
  cout<<setprecision(17);
  cout<<"{\n  \"version\":\"0.1\",\n  \"status\":\"FINITE_PULSE_SQALE_CROSS_PROFILE_STRESS\",\n  \"candidates\":{";
  bool first=true;
  for(auto [nm,per]:T){
    if(!first)cout<<",";first=false;
    Sim ideal(false),actual(true);
    for(int k=0;k<per;k++){step(ideal,nm);step(actual,nm);}
    double F=favg(ideal.U,actual.U), iid=globalphase_identity_error(ideal.U);
    auto &c=actual.c;
    double czsurv=pow(0.9962,c.cz),rzsurv=pow(1.0-0.00066,c.rz),grdiag=pow(0.99980,c.gr);
    double t2=12700.0;
    cout<<"\n    \""<<nm<<"\":{\"signed_period\":"<<per
        <<",\"GR\":"<<c.gr<<",\"Rz_site_requests\":"<<c.rz<<",\"CZ\":"<<c.cz
        <<",\"parallel_pulse_time_us\":"<<c.tpar<<",\"serial_Rz_pulse_time_us\":"<<c.tser
        <<",\"parallel_time_over_T2star\":"<<c.tpar/t2
        <<",\"exp_idle_diagnostic\":"<<exp(-c.tpar/t2)
        <<",\"cross_profile_unitary_Favg\":"<<F<<",\"cross_profile_unitary_infidelity\":"<<1-F
        <<",\"ideal_cycle_identity_infidelity\":"<<iid
        <<",\"CZ_survival_independent_diagnostic\":"<<czsurv
        <<",\"Rz_leakage_survival_envelope\":"<<rzsurv
        <<",\"GR_fidelity_product_diagnostic\":"<<grdiag
        <<",\"combined_product_diagnostic\":"<<czsurv*rzsurv*grdiag<<"}";
  }
  cout<<"\n  },\n  \"source_scope\":{\"timing\":\"PRX Quantum 6 030334 2025\",\"coherent_model\":\"npj Quantum Information 11 193 2025\",\"combined_profile\":\"cross-profile stress only\"},\n  \"physical_promotion\":0\n}\n";
}
