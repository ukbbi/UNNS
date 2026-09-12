$ErrorActionPreference = "Stop"

$PilotDir = $PSScriptRoot
$Project = (Resolve-Path (Join-Path $PilotDir "..\..\..")).Path
$Out = Join-Path $PilotDir "FREEZE_SHA256.txt"
$Record = Join-Path $PilotDir "FREEZE_RECORD.json"

$Targets = @(
    "analysis\replication\jhtdb_pilot_b\PROTOCOL.md",
    "analysis\replication\jhtdb_pilot_b\PROTOCOL.json",
    "analysis\replication\jhtdb_pilot_b\CRITERIA.md",
    "analysis\replication\jhtdb_pilot_b\WORKFLOW.md",
    "analysis\synthesis\jhtdb_pilot_a\SYNTHESIS_v02.md",
    "analysis\synthesis\jhtdb_pilot_a\SYNTHESIS_v02.json",
    "chambers\STRUC_ROUTE_I_v0_1_2",
    "chambers\STRUC_I_v1_0_4",
    "chambers\STRUC_PERC_I_v2_5_0",
    "tools\derive\JHTDB_ROUTE_ADAPTER_v0_1_0",
    "tools\analyze\STITCH_MECH_v0_1_1"
)

$Files = New-Object System.Collections.Generic.List[System.IO.FileInfo]
foreach ($rel in $Targets) {
    $p = Join-Path $Project $rel
    if (-not (Test-Path $p)) {
        throw "Required freeze target not found: $rel"
    }
    $item = Get-Item $p
    if ($item.PSIsContainer) {
        Get-ChildItem $p -File -Recurse | Sort-Object FullName | ForEach-Object { $Files.Add($_) }
    } else {
        $Files.Add($item)
    }
}

$Lines = New-Object System.Collections.Generic.List[string]
foreach ($f in ($Files | Sort-Object FullName -Unique)) {
    $h = (Get-FileHash $f.FullName -Algorithm SHA256).Hash.ToLower()
    $rel = $f.FullName.Substring($Project.Length + 1).Replace("\","/")
    $Lines.Add("$h  $rel")
}
$Lines | Set-Content -Encoding UTF8 $Out

$recordObj = [ordered]@{
    record = "JHTDB_PILOT_B_PROTOCOL_FREEZE"
    protocol_version = "0.1"
    frozen_utc = (Get-Date).ToUniversalTime().ToString("o")
    project_root = $Project
    file_count = $Lines.Count
    checksum_file = "analysis/replication/jhtdb_pilot_b/FREEZE_SHA256.txt"
    status = "LOCKED_BEFORE_PILOT_B_ANALYSIS"
}
$recordObj | ConvertTo-Json -Depth 4 | Set-Content -Encoding UTF8 $Record

Write-Host ""
Write-Host "PILOT B PROTOCOL LOCKED."
Write-Host "Files hashed:" $Lines.Count
Write-Host "Checksum:" $Out
Write-Host "Record:" $Record
