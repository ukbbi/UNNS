import SCR_IV_CertReal
open SCR_IV
/-- NEGATIVE CONTROL: this file MUST FAIL to compile (batches do not cover 2^3 prefixes). -/
def Rp (d : Nat) : List Int := [[-2, 5, 5, 2, 9, -1, 1], [8, -8, 5, 8, 3, 0], [-6, -6, -7, 1, -6], [-9, 9, 1, 0], [9, -1, -6], [-3, 0], [7], []].getD d []
theorem bad : ([[4, 1029, 65], [1075118165, 1091634245]].flatten.length = 2 ^ 3) := by decide
