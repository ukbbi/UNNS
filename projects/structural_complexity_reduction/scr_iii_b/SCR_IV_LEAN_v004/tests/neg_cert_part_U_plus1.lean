import SCR_IV_CertReal
open SCR_IV
/-- NEGATIVE CONTROL: this file MUST FAIL to compile. -/
def Rp (d : Nat) : List Int := [[-2, 5, 5, 2, 9, -1, 1], [8, -8, 5, 8, 3, 0], [-6, -6, -7, 1, -6], [-9, 9, 1, 0], [9, -1, -6], [-3, 0], [7], []].getD d []
theorem bad : batchesOK Rp 8 (-63) (fun _ => false) 3 0 [[4, 1029, 65], [1075118165, 1091634245], [65, 1041, 4]] = true := by decide +kernel
