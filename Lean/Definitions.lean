import Mathlib.Data.Set.Basic
import Mathlib.Logic.Basic

namespace ManualFormalization
variable {α β : Type}
def implies (p q : Prop) : Prop := p → q
def iff_def (p q : Prop) : Prop := p ↔ q

def is_subset (A B : Set α) : Prop := ∀ (x : α), x ∈ A → x ∈ B
def set_union (A B : Set α) : Set α := {x : α | x ∈ A ∨ x ∈ B}
def set_intersection (A B : Set α) : Set α := {x : α | x ∈ A ∧ x ∈ B}
def are_disjoint (A B : Set α) : Prop := set_intersection A B = ∅
def set_complement (A : Set α) : Set α := {x : α | x ∉ A}
def set_difference (A B : Set α) : Set α := {x : α | x ∈ A ∧ x ∉ B}
def symmetric_difference (A B : Set α) : Set α := set_union (set_difference A B) (set_difference B A)
def cartesian_product (A : Set α) (B : Set β) : Set (α × β) := {p : α × β | p.1 ∈ A ∧ p.2 ∈ B}
def power_set (A : Set α) : Set (Set α) := {S : Set α | is_subset S A}

def is_injective (f : α → β) : Prop := ∀ (x₁ x₂ : α), f x₁ = f x₂ → x₁ = x₂
def is_surjective (f : α → β) : Prop := ∀ (y : β), ∃ (x : α), f x = y
def is_bijective (f : α → β) : Prop := is_injective f ∧ is_surjective f

def is_reflexive (R : α → α → Prop) : Prop := ∀ (x : α), R x x
def is_symmetric (R : α → α → Prop) : Prop := ∀ (x y : α), R x y → R y x
def is_transitive (R : α → α → Prop) : Prop := ∀ (x y z : α), R x y → R y z → R x z

end ManualFormalization
