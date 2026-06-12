import Definitions
import Mathlib.Tactic
import Mathlib.Combinatorics.SimpleGraph.Basic
namespace ManualFormalization
theorem intersection_contains_common_elements {α : Type} {A B : Set α} :
  ∀ x, x ∈ set_intersection A B → x ∈ A ∧ x ∈ B :=
by intros x hx; exact hx
end ManualFormalization