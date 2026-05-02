import Mathlib.Data.Set.Basic

def powerSet {α : Type u} (S : Set α) : Set (Set α) :=
{ s | s ⊆ S }