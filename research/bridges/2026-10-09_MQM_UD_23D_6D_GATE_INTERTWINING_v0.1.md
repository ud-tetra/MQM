# MQM–UD 23D→6D gated interface audit v0.1

Evidence: EXACT symbolic/computational under declared incidence model. Physical promotion 0.

Carrier: tetrahedra 0123 and 0124, f=(5,9,7,2), 23 coordinates. Oriented shared face 012 has B3 row (-1,-1). Full block skew generator A has +B_k^T / -B_k couplings. R retains (q1,q2,v1,v2,f,w) with v=B3^T c2 and w=f'. Verified R A = C R, rank(R)=6, dim ker(R)=17; C has q'=v, v'=-[[4,1],[1,4]]q, f'=w, w'=-5f.

Cell kick q1 += eta*f induces q1 += eta*f, w += eta*f (canonical orientation); exact R M_cell=K_cell R. Face kick f += eta*q1 induces f += eta*q1, v1 -= eta*q1, v2 -= eta*q1; exact R M_face=K_face R. Both have nonzero commutators with C for generic eta. 20 rational initial states with six alternating kick checks and free-generator intertwining each passed; check is constructor-derived, not independent scientific review.

Quantum operational analogy: Z-projective instrument outcomes P(0)=(1+z)/2 and P(1)=(1-z)/2 depend only on retained z=Tr(rho Z). Outcome-conditioned X maps state |1> to |0>; Kraus E0=|0><0| and E1=|0><1| satisfy sum E†E=I and reset output is |0><0|. Thus a specified CPTP instrument has closed z-level outcome/control semantics. NO-GO for arbitrary gates: if rho has real off-diagonal a, Y rotation gives z'=z cos(theta)-2a sin(theta), dependent on hidden coherence. Reduced quantum closure is gate-set-specific.

The UD classical kicks are not asserted to be quantum physical gates; no hardware, threshold, fault-tolerance or advantage claim is promoted. Admission time/interval is not derived.
