import Lean.Definitions

namespace ManualFormalization

variable {α : Type}

-- THEOREM 1: The intersection of any set with itself is the set itself.
theorem set_intersection_idemp (A : Set α) : set_intersection A A = A := by
  ext x
  simp [set_intersection]

-- THEOREM 2: The intersection of sets is commutative.
theorem set_intersection_comm (A B : Set α) : set_intersection A B = set_intersection B A := by
  ext x
  simp [set_intersection]
  exact And.comm

-- THEOREM 3: The union of any set with itself is the set itself.
theorem set_union_idemp (A : Set α) : set_union A A = A := by
  ext x
  simp [set_union]

-- THEOREM 4: The union of sets is commutative.
theorem set_union_comm (A B : Set α) : set_union A B = set_union B A := by
  ext x
  simp [set_union]
  exact Or.comm

-- THEOREM 5: For any set A, A is a subset of itself.
theorem subset_refl (A : Set α) : is_subset A A := by
  intro x hx
  exact hx

-- THEOREM 6: Subset relation is transitive.
theorem subset_trans (A B C : Set α) (h1 : is_subset A B) (h2 : is_subset B C) : is_subset A C := by
  intro x hpx
  apply h2
  apply h1
  exact hpx

end ManualFormalization
