import Mathlib.Data.Set.Basic

def symmetricDifference {α : Type} (A B : Set α) : Set α :=
{ x | (x ∈ A ∨ x ∈ B) ∧ ¬ (x ∈ A ∧ x ∈ B) }