[CmdletBinding()]
param(
    [string]$Destination = (Join-Path $PSScriptRoot 'repos')
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

$expectedHashes = [ordered]@{
    'STANDARD_SCORES.json' = '9cd98719a64e789ff72a8a344e808870b58bd632f6cde4c2b1d08faf67dd4f60'
    'SCORECARD.md'         = '9f43ce3d9aec75f4b1d98a25ac47652d696dd33fdbf596a0137cfdb76d5b5056'
    'SCORECARD.csv'        = '68d57979ff209b849fa114ed6d27f05dc3e8296f6bff52148d532d6afc3917e2'
    'SCORE_RULES.md'       = '190613d83db6baab49bb66069d1de78fe7ba673f1969ff4e4a5b4c87ecbf7d74'
}

function Invoke-Git {
    param(
        [Parameter(Mandatory = $true)][string]$Repository,
        [Parameter(Mandatory = $true)][string[]]$Arguments
    )

    $output = @(& git -C $Repository @Arguments 2>&1)
    if ($LASTEXITCODE -ne 0) {
        throw "git -C '$Repository' $($Arguments -join ' ') failed:`n$($output -join "`n")"
    }
    return $output
}

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    throw 'git is required but was not found on PATH.'
}

foreach ($entry in $expectedHashes.GetEnumerator()) {
    $path = Join-Path $PSScriptRoot $entry.Key
    if (-not (Test-Path -LiteralPath $path -PathType Leaf)) {
        throw "Required benchmark file is missing: $($entry.Key)"
    }
    $actual = (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($actual -ne $entry.Value) {
        throw "SHA-256 mismatch for $($entry.Key): expected $($entry.Value), got $actual"
    }
}

$manifestPath = Join-Path $PSScriptRoot 'manifest.json'
$manifest = Get-Content -LiteralPath $manifestPath -Raw | ConvertFrom-Json
$active = @($manifest.repositories | Where-Object { $_.delivery.status -eq 'active' })
if ($active.Count -ne 6) {
    throw "Manifest must contain exactly 6 active repositories; found $($active.Count)."
}

$destinationPath = [IO.Path]::GetFullPath($Destination)
if (Test-Path -LiteralPath $destinationPath) {
    if (@(Get-ChildItem -LiteralPath $destinationPath -Force).Count -ne 0) {
        throw "Destination already exists and is not empty: $destinationPath"
    }
} else {
    New-Item -ItemType Directory -Path $destinationPath | Out-Null
}

$results = @()
foreach ($repo in $active) {
    $kindDirectory = if ($repo.kind -eq 'APP') { 'app' } else { 'framework' }
    $kindRoot = Join-Path $destinationPath $kindDirectory
    New-Item -ItemType Directory -Path $kindRoot -Force | Out-Null
    $repoPath = Join-Path $kindRoot $repo.name
    if (Test-Path -LiteralPath $repoPath) {
        throw "Repository destination already exists: $repoPath"
    }

    Write-Host "Cloning $($repo.id) $($repo.name)..."
    $cloneOutput = @(& git clone --quiet $repo.delivery.repository_url $repoPath 2>&1)
    if ($LASTEXITCODE -ne 0) {
        throw "git clone failed for $($repo.id):`n$($cloneOutput -join "`n")"
    }

    $expectedRefs = [ordered]@{}
    foreach ($property in $repo.delivery.refs.PSObject.Properties) {
        $expectedRefs[$property.Name] = [string]$property.Value
    }

    foreach ($ref in $expectedRefs.GetEnumerator()) {
        if ($ref.Key.StartsWith('refs/heads/')) {
            $branch = $ref.Key.Substring('refs/heads/'.Length)
            Invoke-Git -Repository $repoPath -Arguments @('update-ref', "refs/heads/$branch", $ref.Value) | Out-Null
        }
    }

    Invoke-Git -Repository $repoPath -Arguments @('checkout', '--quiet', $repo.default_branch) | Out-Null
    Invoke-Git -Repository $repoPath -Arguments @('remote', 'remove', 'origin') | Out-Null

    $actualRefs = [ordered]@{}
    $refLines = Invoke-Git -Repository $repoPath -Arguments @('for-each-ref', '--format=%(refname) %(objectname)', 'refs/heads', 'refs/tags')
    foreach ($line in $refLines) {
        if ($line -match '^(refs/(?:heads|tags)/\S+) ([0-9a-f]{40,64})$') {
            $actualRefs[$Matches[1]] = $Matches[2]
        }
    }

    if ($actualRefs.Count -ne $expectedRefs.Count) {
        throw "Ref count mismatch for $($repo.id): expected $($expectedRefs.Count), got $($actualRefs.Count)."
    }
    foreach ($ref in $expectedRefs.GetEnumerator()) {
        if (-not $actualRefs.Contains($ref.Key)) {
            throw "Missing ref for $($repo.id): $($ref.Key)"
        }
        if ($actualRefs[$ref.Key] -ne $ref.Value) {
            throw "OID mismatch for $($repo.id) $($ref.Key): expected $($ref.Value), got $($actualRefs[$ref.Key])"
        }
    }

    $head = (@(Invoke-Git -Repository $repoPath -Arguments @('rev-parse', 'HEAD')))[0].Trim()
    if ($head -ne $repo.delivery.expected_head) {
        throw "HEAD mismatch for $($repo.id): expected $($repo.delivery.expected_head), got $head"
    }

    $remoteCount = @(Invoke-Git -Repository $repoPath -Arguments @('remote')).Count
    $results += [pscustomobject]@{
        ID      = $repo.id
        Name    = $repo.name
        Head    = $head.Substring(0, 12)
        Refs    = $actualRefs.Count
        Remotes = $remoteCount
        Status  = 'PASS'
    }
}

$results | Format-Table -AutoSize
Write-Host "PASS: restored and verified 6 repositories in $destinationPath"
