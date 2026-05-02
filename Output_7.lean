import Mathlib

def is_prime (p : Nat) : Prop :=
p > 1 ∧ ∀ (d : Nat), d ∣ p → (d = 1 ∨ d = p)