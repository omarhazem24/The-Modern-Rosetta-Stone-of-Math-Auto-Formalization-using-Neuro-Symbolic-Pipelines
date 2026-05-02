import Mathlib.Data.Set.Basic

def union {α : Type} (s : Set (Set α)) : Set α :=
  {x | ∃ t ∈ s, x ∈ t}

def union' {α : Type} (s : Set (Set α)) : Set α :=
  ⋃₀ s