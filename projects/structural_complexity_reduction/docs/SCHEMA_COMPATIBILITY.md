# Frozen Schema Compatibility Note

The frozen `SCR_I_PREREG_v003/schema/result_schema.json` requires a field named `basin_count_base`.

The completed canonical runner writes the semantically identical baseline-basin count under the field name:

```text
basin_count
```

This is a **field-name mismatch**, not a scientific-quantity mismatch. The value is the number of independently identified target basins before preservation is evaluated. The frozen preregistration is not edited post hoc.

Canonical compatibility mapping:

```text
result_schema.basin_count_base  <->  PRIMARY_RESULT_v003.basin_count
```

All other frozen primary fields used by the v003 decision rules are present in the completed result. Any future benchmark should correct the schema name before preregistration freeze.
