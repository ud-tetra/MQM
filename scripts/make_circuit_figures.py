from pathlib import Path
import stim
D=Path(__file__).resolve().parents[1]/'dist/circuits'
D.mkdir(exist_ok=True)
configs=[('core-x',4,(((0,0),(3,2)),((0,1),(1,0)),((0,2),(2,1)))),('core-x5',5,(((0,0),(2,1)),((0,1),(3,2)),((0,2),(4,3)),((0,3),(1,0))))]
for name,n,layers in configs:
 c=stim.Circuit();c.append('R',range(n,2*n-1))
 for layer in layers:
  for q,a in layer:c.append('CX',[q,n+a])
  c.append('TICK')
 c.append('M',range(n,2*n-1))
 (D/(name+'.stim')).write_text('# Ideal syndrome round. Data input is not reset. No noise or hardware timings.\n'+str(c)+'\n')
 (D/(name+'.svg')).write_text(str(c.diagram('timeline-svg')))
 # Enumerate basis inputs; confirm measured parities in listed generator order.
 for value in range(1<<n):
  sim=stim.TableauSimulator()
  for q in range(n):
   if value>>q&1:sim.x(q)
  sim.do_circuit(c)
  expected=[bool((value&1)^((value>>q)&1)) for q in range(1,n)]
  assert sim.current_measurement_record()==expected
center=['IIIXXZZI','IIIYIYZZ','IIIXZIXZ','XXXXYYIX']
c=stim.Circuit()
for p in center:
 c+=stim.Circuit('MPP '+'*'.join(ch+str(q) for q,ch in enumerate(p) if ch!='I')+'\nTICK')
(D/'subsystem.stim').write_text('# Ideal abstract center measurements only. MPP is not an ancilla-resolved extraction schedule.\n'+str(c)+'\n')
(D/'subsystem.svg').write_text(str(c.diagram('timeline-svg')))
# Commuting center measurements have stable repeat outcomes in an ideal round.
sim=stim.TableauSimulator();sim.do_circuit(c);first=sim.current_measurement_record();sim.do_circuit(c);assert sim.current_measurement_record()[4:]==first
print('Three Stim-generated figures; repetition parities and repeated center measurements checked')
