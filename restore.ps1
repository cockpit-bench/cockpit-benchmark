[CmdletBinding()]
param([string]$Destination = (Join-Path $PSScriptRoot 'repos'))
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$expectedHashes = [ordered]@{
    'STANDARD_SCORES.json' = '19a13fa0e57a19cd2793bb924e0a1bb9fda314e3836c983e41a1b53cf852929a'
    'SCORECARD.md' = '7fc86963bea885acb092f56a3c36a76468e0dc842300f82fed1fd5a2bb1a54f8'
    'SCORECARD.csv' = '14207a6253bdf2b9c921fbda3ffdc83bdcf323a659ddd1be9df92ee80580b1aa'
    'SCORE_RULES.md' = '28c456ddf16a7d85ae642f11785ce94689412bd715d0cd5140bc51ceb35ca5d9'
    'manifest.json' = '0eb8b5d2e6d98322a85143b396bd6ec0041ed1eeec050b9d2e4399fc0dd2fee6'
}
if (-not (Get-Command git -ErrorAction SilentlyContinue)) { throw 'git is required.' }
foreach ($entry in $expectedHashes.GetEnumerator()) {
    $path = Join-Path $PSScriptRoot $entry.Key
    if (-not (Test-Path -LiteralPath $path -PathType Leaf)) { throw "Missing $($entry.Key)" }
    $actual = (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($actual -ne $entry.Value) { throw "SHA-256 mismatch for $($entry.Key)" }
}
$manifest = Get-Content (Join-Path $PSScriptRoot 'manifest.json') -Raw | ConvertFrom-Json
$active = @($manifest.repositories | Where-Object { $_.delivery_status -eq 'active' })
if ($active.Count -ne 18) { throw "Expected 18 active repositories, got $($active.Count)" }
$destinationPath = [IO.Path]::GetFullPath($Destination)
if (Test-Path -LiteralPath $destinationPath) {
    if (@(Get-ChildItem -LiteralPath $destinationPath -Force).Count -ne 0) { throw "Destination is not empty: $destinationPath" }
} else { New-Item -ItemType Directory -Path $destinationPath | Out-Null }
$results = @()
foreach ($entry in $active) {
    $kindDir = if ($entry.kind -eq 'APP') { 'app' } else { 'framework' }
    $repoPath = Join-Path (Join-Path $destinationPath $kindDir) $entry.name
    New-Item -ItemType Directory -Path (Split-Path $repoPath) -Force | Out-Null
    & git clone --quiet $entry.delivery.repository_url $repoPath
    if ($LASTEXITCODE -ne 0) { throw "Clone failed: $($entry.id)" }
    foreach ($property in $entry.delivery.refs.PSObject.Properties) {
        if ($property.Name.StartsWith('refs/heads/')) { & git -C $repoPath update-ref $property.Name ([string]$property.Value) }
        if ($LASTEXITCODE -ne 0) { throw "Cannot restore ref $($property.Name)" }
    }
    & git -C $repoPath checkout --quiet $entry.default_branch
    & git -C $repoPath remote remove origin
    $actual = @{}
    & git -C $repoPath for-each-ref '--format=%(refname) %(objectname)' refs/heads refs/tags | ForEach-Object {
        if ($_ -match '^(refs/(?:heads|tags)/\S+) ([0-9a-f]{40,64})$') { $actual[$Matches[1]] = $Matches[2] }
    }
    if ($actual.Count -ne $entry.delivery.refs.PSObject.Properties.Count) { throw "Ref count mismatch: $($entry.id)" }
    foreach ($property in $entry.delivery.refs.PSObject.Properties) {
        if (-not $actual.ContainsKey($property.Name) -or $actual[$property.Name] -ne [string]$property.Value) { throw "Ref mismatch: $($entry.id) $($property.Name)" }
    }
    $head = (& git -C $repoPath rev-parse HEAD).Trim()
    if ($head -ne $entry.delivery.expected_head) { throw "HEAD mismatch: $($entry.id)" }
    if (@(& git -C $repoPath remote).Count -ne 0) { throw "Remote was not removed: $($entry.id)" }
    $results += [pscustomobject]@{ ID=$entry.id; Name=$entry.name; Head=$head.Substring(0,12); Refs=$actual.Count; Status='PASS' }
}
$results | Format-Table -AutoSize
Write-Host "PASS: restored 18/18 repositories with exact refs and zero remotes."
