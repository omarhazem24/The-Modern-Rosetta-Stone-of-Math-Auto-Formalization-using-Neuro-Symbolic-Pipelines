import Mathlib.Data.Set.Basic

def intersection_contains {α : Type u} (A B : Set α) (x : α) (h : x ∈ A ∩ B) : x ∈ A ∧ x ∈ B :=
by rw [Set.mem_inter_iff] at h; exact h