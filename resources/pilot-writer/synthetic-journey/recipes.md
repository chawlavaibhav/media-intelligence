# RES-007 synthetic journey — full transform parameters

This is the `params_location` referenced by the archive's transform recipes. A recipe's
`params_hash` is the SHA-256 of the exact parameter string below (computed by the writer,
never hand-typed). The tool version `7.0.1-synthetic` marks that no real ffmpeg ran —
the "transforms" in this zero-spend journey are deterministic byte operations standing in
for real ones (concat = A-bytes then B-bytes; overlay composite = cut-bytes then logo-bytes).

## TR-CONCAT (operation: concat)

```
-f concat -safe 0 -i list.txt -c copy cut.bin
```

## TR-OVERLAY (operation: overlay)

```
-i cut.bin -i logo.bin -filter_complex overlay=10:10 final.bin
```
