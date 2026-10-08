# Family 102: proof-scope quantifier interventions

The source theorem reports an approximation-hardness reduction with quantifier order: FORALL fixed error parameters (epsilon,delta), EXISTS fixed alphabet dimension and reduction, FORALL SAT instances phi, completeness/soundness constraints hold. This is not the same as one universal alphabet for all error pairs, nor as choosing an alphabet separately per input.

This pilot builds a finite Boolean predicate P(e,s,phi) with e having 3 values, s 3 values, phi 2 values. It asks three logically ordered questions: STRONG exists s forall e forall phi, ORIGINAL forall e exists s forall phi, WEAK forall e forall phi exists s.

Mathematical fact: STRONG implies ORIGINAL implies WEAK. The converses are false, demonstrated by four exact finite countermodels:
- 111: one uniform s.
- 011: s depends on e but not phi.
- 001: s depends on both e and phi.
- 000: one input has no witness.

The oracle evaluates quantifier truth directly and independently via finite set intersections, with randomized row and witness permutations. Gold is separated from prompts. This establishes logical scope competence tasks, not the original Unique Games hardness theorem's truth, nor models' ability to reconstruct the full reduction.

Seven matched-information conditions parallel the family 017 experiment. There are no language model evaluations yet. This is deliberately lower level (statement and quantifier understanding); full proof-mechanism transfer remains the next research gate.
