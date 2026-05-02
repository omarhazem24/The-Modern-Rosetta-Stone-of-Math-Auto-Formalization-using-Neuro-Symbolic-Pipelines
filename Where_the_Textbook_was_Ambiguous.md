# Where the Textbook was Ambiguous
## Uncovering Hidden Logic in Mathematical Texts via Auto-Formalization

Through the process of formalizing definitions and theorems from standard textbooks (such as Rosen's *Discrete Mathematics*) into Lean 4, several inherent ambiguities in human-readable mathematical literature were uncovered. A human reader uses context and intuition to fill these logical gaps, but a rigid compiler like Lean 4 instantly rejects them.

### 1. Implicit Universe Levels
**Textbook phrasing:** "Let S be a set."
**The ambiguity:** In human mathematics, "Set" is an absolute, universal notion. However, in dependent type theory (and Lean 4), sets must exist within a specific type universe (e.g., `Type u`). 
**Compiler consequence:** Translating this directly causes universe mismatches. The textbook assumes the reader knows we are operating within a single coherent universe, but the compiler demands explicit declarations of `(α : Type)` before defining `Set α`.

### 2. Overloaded Notation
**Textbook phrasing:** "The sum of elements in graph G..."
**The ambiguity:** Is the graph directed or undirected? Are the edges weighted with natural numbers, integers, or real numbers? Textbooks often overload the `+` operator or edge definitions depending on the chapter context.
**Compiler consequence:** Lean 4 requires explicit type coercion classes (e.g., `[Add α]`) for the objects being summed.

### 3. Assumed Non-Emptiness
**Textbook phrasing:** "Choose an element x from X..."
**The ambiguity:** The textbook silently assumes set X is inhabited (non-empty). 
**Compiler consequence:** Lean 4 requires an explicit hypothesis `(h : X.Nonempty)` or a `[Nonempty X]` typeclass instance. Without it, the proof gets halted because the AI logically cannot summon an element out of nowhere.

### 4. Fuzzy Topological Constraints
**Textbook phrasing:** "Let f be a mapping from X to Y..."
**The ambiguity:** When transitioning from discrete math to Algebraic Topology, the text often forgets to explicitly state `f` must be continuous, as it is implied by the chapter title.
**Compiler consequence:** Lean 4's `Mathlib.Topology.ContinuousFunction` expects `C(X, Y)`. Generative AI models often failed here because they parsed the text literally (`f : X → Y`) instead of extracting the continuous wrapper implied by human domain knowledge.

**Conclusion:** 
The "Truth Scanner" acts not only as a translator but as an ultimate editorial auditor. It proves that informal mathematics heavily leans on the reader's neurological ability to infer context, something purely symbolic systems refuse to do.
