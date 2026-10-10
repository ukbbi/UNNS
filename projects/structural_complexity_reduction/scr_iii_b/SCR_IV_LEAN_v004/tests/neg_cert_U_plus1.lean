import SCR_IV_CertReal
open SCR_IV
/-- NEGATIVE CONTROL: this file MUST FAIL to compile. -/
def R0 (d : Nat) : List Int := [[-5, -9, 3, 3, 1, -1], [-4, 7, 6, -9, 6], [-4, -5, 9, 6], [-6, -9, -5], [7, -5], [-4], []].getD d []
theorem bad : checkAll R0 7 (-61) (fun _ => false) 4634292273868244053 = true := by decide +kernel
