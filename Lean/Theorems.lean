import Lean.Definitions

namespace ManualFormalization

variable {α : Type}


theorem set_intersection_idemp (A : Set α) : set_intersection A A = A := by
  ext x
  simp [set_intersection]


theorem set_intersection_comm (A B : Set α) : set_intersection A B = set_intersection B A := by
  ext x
  simp [set_intersection]
  exact And.comm


theorem set_union_idemp (A : Set α) : set_union A A = A := by
  ext x
  simp [set_union]


theorem set_union_comm (A B : Set α) : set_union A B = set_union B A := by
  ext x
  simp [set_union]
  exact Or.comm


theorem subset_refl (A : Set α) : is_subset A A := by
  intro x hx
  exact hx


theorem subset_trans (A B C : Set α) (h1 : is_subset A B) (h2 : is_subset B C) : is_subset A C := by
  intro x hpx
  apply h2
  apply h1
  exact hpx

end ManualFormalization
