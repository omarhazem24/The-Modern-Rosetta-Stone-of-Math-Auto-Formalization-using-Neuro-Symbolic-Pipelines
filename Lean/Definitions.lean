import Mathlib.Data.Set.Basic
import Mathlib.Logic.Basic

namespace ManualFormalization

variable {α β : Type}

-- SECTION 1: LOGIC (Rosen Chapter 1)
/-- Def 1: Logical Implication -/ def implies (p q : Prop) : Prop := p → q
/-- Def 2: Logical Equivalence -/ def iff_def (p q : Prop) : Prop := p ↔ q

-- SECTION 2: SET THEORY (Rosen Chapter 2)
/-- Def 3: Subset -/ def is_subset (A B : Set α) : Prop := ∀ (x : α), x ∈ A → x ∈ B
/-- Def 4: Union -/ def set_union (A B : Set α) : Set α := {x : α | x ∈ A ∨ x ∈ B}
/-- Def 5: Intersection -/ def set_intersection (A B : Set α) : Set α := {x : α | x ∈ A ∧ x ∈ B}
/-- Def 6: Disjoint Sets -/ def are_disjoint (A B : Set α) : Prop := set_intersection A B = ∅
/-- Def 7: Set Complement -/ def set_complement (A : Set α) : Set α := {x : α | x ∉ A}
/-- Def 8: Set Difference -/ def set_difference (A B : Set α) : Set α := {x : α | x ∈ A ∧ x ∉ B}
/-- Def 9: Symmetric Difference -/ def symmetric_difference (A B : Set α) : Set α := set_union (set_difference A B) (set_difference B A)
/-- Def 10: Cartesian Product -/ def cartesian_product (A : Set α) (B : Set β) : Set (α × β) := {p : α × β | p.1 ∈ A ∧ p.2 ∈ B}
/-- Def 11: Power Set -/ def power_set (A : Set α) : Set (Set α) := {S : Set α | is_subset S A}

-- SECTION 3: FUNCTIONS (Rosen Chapter 2.3)
/-- Def 12: Injective -/ def is_injective (f : α → β) : Prop := ∀ (x₁ x₂ : α), f x₁ = f x₂ → x₁ = x₂
/-- Def 13: Surjective -/ def is_surjective (f : α → β) : Prop := ∀ (y : β), ∃ (x : α), f x = y
/-- Def 14: Bijective -/ def is_bijective (f : α → β) : Prop := is_injective f ∧ is_surjective f

-- SECTION 4: RELATIONS (Rosen Chapter 9)
/-- Def 15: Reflexive -/ def is_reflexive (R : α → α → Prop) : Prop := ∀ (x : α), R x x
/-- Def 16: Symmetric -/ def is_symmetric (R : α → α → Prop) : Prop := ∀ (x y : α), R x y → R y x
/-- Def 17: Transitive -/ def is_transitive (R : α → α → Prop) : Prop := ∀ (x y z : α), R x y → R y z → R x z

end ManualFormalization
