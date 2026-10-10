# Iteration 10: narrow automatic producer and symbolic transfer gates

This directory introduces the FIRST code path in the pilot that actually reads the **original 197 LaTeX** and emits an evidence-carrying, source-anchored JSON artifact without a manually pasted JSON artifact. It is deterministic and sharply template-restricted, **not** a trained/LLM producer and not a general proof-understanding solution.

Run from the repository root:

    python3 -m unittest discover -s research/proof_understanding/design_v1/producer/tests -p 'test_*.py' -v
    python3 research/proof_understanding/design_v1/producer/source197_producer.py \
      --source preprints/A-Counterexample-to-Kaplanskys-Direct-Finiteness-Conjecture-in-Characteristic-Two-September-23-2026/build/sections/06-cellular-automata.tex \
      --output /tmp/produced_197.json
    python3 research/proof_understanding/design_v1/producer/finite_boundary.py

The source parser checks local TeX labels, lemma scope, proposition premises, operator orientation, multiplication ordering, delta-coefficient formula, image formula, and TWO proof-line tokens. On any mismatch it emits BLOCKED with no reusable claims rather than silently replacing a suspect original proof with a correct different argument. The synthetic mutation tests change neighbor side, product ordering, proof index order, the one-sided inverse hypothesis, finite alphabet field premise, and the nonzero coefficient step. This rejects only explicitly recognized perturbations: adversarially constructed false TeX can still pass. Claims in the successful output carry **conditional** algebraic evidence, not independent universal semantic verification.

The word-normalization check uses tuples of formal monoid index letters, and assumes associativity, finite sums and a field. Generalizing the *conditional local operator lemma* from group to monoid does not generalize the source's exotic group-algebra existence claim. In particular, finite-dimensional unital algebras cannot have ab=1 and ba!=1. The second script exhausts 16 elements in F2[T2] (256 ordered coefficient pairs), including associativity checks, as a local numeric sanity check only; the general finite-dimensional obstruction has a separate mathematical proof in the iteration report.

Six public manually constructed boundary cards contain YES/NO/UNKNOWN classifications with reasons; they are **not model performance data** or a held-out benchmark. Source and reference artifacts should be frozen before future blinded transfer task creation. No paid inference, open-model rerun, or new source-level theorem verification occurs here.

The GitHub Actions workflow deliberately checks out the original source without modifying it, executes exact tests, prints and archives the actual produced JSON and finite-algebra enumeration, and never writes to main.
