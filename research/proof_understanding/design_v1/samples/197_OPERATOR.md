# Sample 197: representation convention is a reusable proof obligation

Source anchor: 197 family, section 06-cellular-automata.tex. This sample establishes only the elementary CONDITIONAL operator transport, not existence of the exotic group and group-ring witnesses.

For a group G and field K, let c=sum_u c_u u in K[G] have finite support. Define T_c on every configuration x in K^G by
(T_c x)(g)=sum_u c_u*x(g*u).
Finite support ensures every coordinate is a finite sum. Direct computation gives:
(T_c(T_d x))(g)=sum_{u,v} c_u d_v x(g*u*v)=(T_{cd} x)(g).
Thus T_c composed with T_d equals T_cd, not T_dc. The assignment is faithful: if T_c=0, testing x=delta_h at g=identity recovers every coefficient c_h.

If a*b=1 in K[G], then T_a composed with T_b=I, so T_b is injective. Its image is exactly {y:T_ba(y)=y}: in-image vectors are fixed, while a fixed y equals T_b(T_a y) and is therefore in-image. If additionally b*a!=1, faithfulness supplies a delta_h not fixed by T_ba, showing T_b is not surjective. This implication is valid for full K^G, not only finitely supported configurations.

Intervention: the superficially similar left-neighbor action S_c x(g)=sum c_u x(u*g) reverses multiplication order: S_c composed with S_d=S_{dc}. An explanation or graph omitting the convention would induce a false inference in noncommutative groups.

Finite control: the local exhaustive F2[S3] code finds all 4,096 algebra-element pairs, tests operator identities on a complete vector-space basis and detects an incorrect orientation. Because this finite-dimensional algebra has no one-sided-only inverse, the control cannot witness the high-level manuscript result. CI tests and local execution logs are recorded separately.

Reusable knowledge: (i) left-inverse injectivity, (ii) fixed-point image certificate, (iii) basis-vector detection of nonzero algebra elements, (iv) sensitivity of composition to neighbor order. Unknown: whether a specific source manuscript has correctly constructed a*b=1 and b*a!=1.
