from adapters.plasma_discharge_adapter import PlasmaDischargeAdapter
import pandas as pd


def test_adapter_minimal():
    src = pd.DataFrame({"t": [0.0, 0.1, 0.2], "p": [1.0, 1.2, 1.5]})
    adapter = PlasmaDischargeAdapter(device="TEST")
    out = adapter.from_dataframe(src, {"time": "t", "P_heat": "p"}, shot_id="shot001")
    adapter.validate_minimal(out)
    assert list(out["time"]) == [0.0, 0.1, 0.2]
    assert list(out["P_heat"]) == [1.0, 1.2, 1.5]
