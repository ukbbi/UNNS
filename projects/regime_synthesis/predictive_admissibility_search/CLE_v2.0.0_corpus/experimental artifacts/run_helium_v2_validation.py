from pathlib import Path

from cle.rigidity_engine import RigidityEngine
from cle.rigidity_models import classify_rigidity_class


ROOT = Path(__file__).parent

RIGIDITY_DIR = ROOT / "CLE_PILOT_I" / "helium" / "rigidity"
INTERACTION_DIR = ROOT / "CLE_PILOT_I" / "helium" / "rigidity_interaction"
ANISO_DIR = ROOT / "anisotropic_outputs"


def collect_json_files(directory):
    return sorted(directory.glob("*.json"))


def print_family(title, result):

    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)

    print(f"topology_universal = {result.topology_universal}")
    print(f"rigidity_universal = {result.rigidity_universal}")
    print(f"layers_split       = {result.layers_split}")

    print("\nRigidity ordering:\n")

    ordered = sorted(
        result.results,
        key=lambda r: r.rigidity_profile.persistence_depth,
        reverse=True,
    )

    for rank, dual in enumerate(ordered, start=1):

        profile = dual.rigidity_profile

        rigidity_class = classify_rigidity_class(
            profile.persistence_depth,
            profile.gr_variance,
            profile.bifurcation_sharpness,
            profile.collapse_onset_radius,
        )

        # Support both Enum-based and string-based class systems
        if hasattr(rigidity_class, "name"):
            class_name = rigidity_class.name
        else:
            class_name = str(rigidity_class)

        print(
            f"{rank:02d} | "
            f"{dual.encoding_id:<32} | "
            f"class={class_name:<18} | "
            f"GR={profile.persistence_depth:.5f} | "
            f"persist={profile.admissibility_persistence:.5f} | "
            f"frag={profile.fragmentation_rate:.5f}"
        )


def main():

    engine = RigidityEngine()

    rigidity_files = collect_json_files(RIGIDITY_DIR)
    interaction_files = collect_json_files(INTERACTION_DIR)
    anisotropic_files = collect_json_files(ANISO_DIR)

    print("\nLoading rigidity family...")

    rigidity_result = engine.evaluate_family(
        encoding_ids=[
            "qmi_spectrum",
            "zeeman",
        ],
        grid_files=rigidity_files[:2],
        topology_classes=[
            "FULL",
            "FULL",
        ],
        topology_scores=[
            0.867,
            0.867,
        ],
        system_id="helium_rigidity",
    )

    print("\nLoading interaction family...")

    interaction_result = engine.evaluate_family(
        encoding_ids=[
            "zeeman",
            "zeeman_singlet",
            "zeeman_triplet",
            "delta_zeeman_singlet",
            "delta_zeeman_triplet",
        ],
        grid_files=interaction_files[:5],
        topology_classes=[
            "FULL",
            "FULL",
            "FULL",
            "FULL",
            "FULL",
        ],
        topology_scores=[
            0.867,
            0.867,
            0.867,
            0.867,
            0.867,
        ],
        system_id="helium_interaction",
    )

    print("\nLoading anisotropic family...")

    anisotropic_result = engine.evaluate_anisotropic_family(
        grid_dir=ANISO_DIR,
        system_id="helium_anisotropic",
    )

    print_family(
        "HELIUM RIGIDITY FAMILY",
        rigidity_result,
    )

    print_family(
        "HELIUM INTERACTION FAMILY",
        interaction_result,
    )

    print_family(
        "ANISOTROPIC HELIUM FAMILY",
        anisotropic_result,
    )

    print("\n" + "=" * 70)
    print("FINAL CLE v2 VALIDATION")
    print("=" * 70)

    all_results = [
        rigidity_result,
        interaction_result,
        anisotropic_result,
    ]

    topology_ok = all(r.topology_universal for r in all_results)
    rigidity_split = any(not r.rigidity_universal for r in all_results)
    layers_split = any(r.layers_split for r in all_results)

    print(f"topology_universal = {topology_ok}")
    print(f"rigidity_universal = {not rigidity_split}")
    print(f"layers_split       = {layers_split}")

    if topology_ok and rigidity_split and layers_split:

        print("\nCLE v2 VALIDATION PASSED")
        print("----------------------------------------")
        print("Topology layer converges universally.")
        print("Rigidity layer diverges by representation.")
        print("Layer separation operationally confirmed.")

    else:

        print("\nCLE v2 VALIDATION FAILED")
        print("----------------------------------------")
        print("Expected topology/rigidity split not reproduced.")

    print("\nDone.")


if __name__ == "__main__":
    main()