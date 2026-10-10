import SCR_IV_Spins
import SCR_IV_Data
/-! # IV-1 (grammar): the 16 frozen vertex constraints, the 2-in/2-out predicate and violation counts.
Frozen convention (same as solver_v010 / make_instance_v010): a vertex is (mask, plusIn); island i is incident iff mask bit i is set;
island i points INTO the vertex iff (s_i = +1) == (plusIn bit i). The vertex is satisfied iff exactly 2 incident islands point in. -/
namespace SCR_IV

/-- Number of incident islands of the vertex (mask, plusIn) that point into it in configuration `id`. -/
def inCount (mask plusIn id : Nat) : Nat :=
  (List.range nSpins).foldl
    (fun a i => if mask.testBit i && (id.testBit i == plusIn.testBit i) then a + 1 else a) 0

def vertexOK (v : Nat × Nat) (id : Nat) : Bool := inCount v.1 v.2 id == 2

/-- Number of violated constrained vertices. -/
def violations (id : Nat) : Nat := vertices.countP (fun v => !vertexOK v id)

/-- Indices (file order) of violated vertices. -/
def violatingVertices (id : Nat) : List Nat :=
  ((List.range vertices.length).filter (fun k => !vertexOK (vertices.getD k (0, 0)) id))

/-- Per-vertex inward counts. -/
def inCounts (id : Nat) : List Nat := vertices.map (fun v => inCount v.1 v.2 id)

/-- Grammar membership: every constrained vertex is 2-in/2-out. -/
def IsGrammar (id : Nat) : Prop := violations id = 0

instance (id : Nat) : Decidable (IsGrammar id) := inferInstanceAs (Decidable (violations id = 0))

/-- Number of set bits among the low 40 bits. -/
def popcount40 (m : Nat) : Nat := (List.range nSpins).countP (fun i => m.testBit i)

/-- Structural well-formedness of the frozen vertex table. -/
def tableWellFormed : Bool :=
  vertices.length == 16 &&
  vertices.all (fun v => popcount40 v.1 == 4 && popcount40 v.2 == 2 && v.1 < 2 ^ nSpins && (v.2 &&& v.1) == v.2)

theorem table_wellFormed : tableWellFormed = true := by decide +kernel

theorem masks_distinct : (vertices.map Prod.fst).Nodup := by decide +kernel

/-- Every island is incident to at least one and at most two constrained vertices. -/
theorem island_coverage :
    (List.range nSpins).all (fun i =>
      let c := vertices.countP (fun v => v.1.testBit i)
      decide (1 ≤ c ∧ c ≤ 2)) = true := by decide +kernel

/-- Violations are bounded by the number of vertices. -/
theorem violations_le (id : Nat) : violations id ≤ vertices.length := by
  unfold violations; exact List.countP_le_length

end SCR_IV
