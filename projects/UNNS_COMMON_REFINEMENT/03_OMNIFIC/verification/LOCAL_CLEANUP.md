# Conway Verification Cleanup

After the local verification evidence has been recorded, the temporary checkout and Mathlib cache
can be removed.

## Keep

Do not delete:

```text
C:\leancheck\hold
```

until the earlier local experimental files stored there have been reviewed.

## Safe to delete

Temporary Conway checkout:

```bat
rmdir /s /q C:\leancheck\conway
```

Optional Mathlib cache cleanup:

```bat
rmdir /s /q "%USERPROFILE%\.cache\mathlib"
```

Keeping the Mathlib cache will make future Mathlib builds faster; deleting it reclaims disk space.

After all Lean verification work is finished, unused Lean toolchains can be inspected with:

```bat
elan toolchain list
```

Do not uninstall Lean 4.31.0 until all Conway verification work is complete.
