structure Set (α : Type) where
  carrier : α → Prop

instance (α : Type) : Membership α (Set α) where
  mem x s := s.carrier x

def inter {α : Type} (A B : Set α) : Set α :=
  { carrier := fun x => (A.carrier x) ∧ (B.carrier x) }

infixr:70 " ∩ " => inter

theorem mem_inter_iff {α : Type} (A B : Set α) (x : α) : x ∈ A ∩ B ↔ x ∈ A ∧ x ∈ B := by
  rfl