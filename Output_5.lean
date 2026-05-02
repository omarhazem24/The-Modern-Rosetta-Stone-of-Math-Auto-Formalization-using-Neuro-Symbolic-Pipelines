import Mathlib

structure EquivalenceRelation (A : Type) where
  R : A → A → Prop
  reflexive : ∀ a, R a a
  symmetric : ∀ a b, R a b → R b a
  transitive : ∀ a b c, R a b → R b c → R a c