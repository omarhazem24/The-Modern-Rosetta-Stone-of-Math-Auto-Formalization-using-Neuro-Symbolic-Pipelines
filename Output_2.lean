import Mathlib

def injective {A B : Type} (f : A → B) : Prop :=
∀ (x y : A), f x = f y → x = y