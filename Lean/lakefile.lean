import Lake
open Lake DSL

package definitions

require mathlib from git
  "https://github.com/leanprover-community/mathlib4.git"

@[default_target]
lean_lib Definitions
lean_lib Theorems
