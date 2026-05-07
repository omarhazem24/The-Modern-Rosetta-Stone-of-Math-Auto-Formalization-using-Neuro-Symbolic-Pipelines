dataset = [
    {
        'informal': 'The sum of any two even integers is even.',
        'formal': 'lemma sum_even (a b : \Z) (ha : Even a) (hb : Even b) : Even (a + b) := by\n  exact Even.add ha hb'
    },
    {
        'informal': 'If x is odd, then x^2 is odd.',
        'formal': 'lemma odd_sq (x : \Z) (hx : Odd x) : Odd (x^2) := by\n  exact Odd.pow hx'
    },
    {
        'informal': 'For any positive integer n, n > 0.',
        'formal': 'lemma pos_gt_zero (n : \N) (hn : n > 0) : n > 0 := by\n  exact hn'
    },
    {
        'informal': 'The union of two sets A and B is the set of all elements that are in A or in B.',
        'formal': 'def Set.union {a : Type} (A B : Set a) : Set a := {x | x ? A \lor x ? B}'
    },
    {
        'informal': 'For any sets A, B, and C, if A is a subset of B and B is a subset of C, then A is a subset of C.',
        'formal': 'lemma subset_trans {a : Type} {A B C : Set a} (hab : A \subset B) (hbc : B \subset C) : A \subset C := by\n  exact Set.Subset.trans hab hbc'
    },
    {
        'informal': 'The intersection of any set with the empty set is the empty set.',
        'formal': 'lemma inter_empty {a : Type} (A : Set a) : A \inter \emptyset = \emptyset := by\n  exact Set.inter_empty A'
    },
    {
        'informal': 'A prime number is an integer greater than 1 that is only divisible by 1 and itself.',
        'formal': 'def Prime (p : \N) : Prop := p > 1 \land \forall m, m \mid p \to m = 1 \lor m = p'
    },
    {
        'informal': 'The sum of a rational number and an irrational number is irrational.',
        'formal': 'lemma rat_add_irrat {x y : \R} (hx : IsRat x) (hy : \neg IsRat y) : \neg IsRat (x + y) := by\n  sorry'
    },
    {
        'informal': 'The composition of two injective functions is injective.',
        'formal': 'lemma comp_injective {a ß ? : Type} {f : a \to ß} {g : ß \to ?} (hf : Function.Injective f) (hg : Function.Injective g) : Function.Injective (g \circ f) := by\n  exact Function.Injective.comp hg hf'
    },
    {
        'informal': 'If an integer is divisible by 4, then it is divisible by 2.',
        'formal': 'lemma div4_div2 (n : \Z) (hn : 4 \mid n) : 2 \mid n := by\n  sorry'
    }
    # (Generating 50+ lines would take too long in shell, I will write a generator python script to output a full 52 prompt dataset)
]
