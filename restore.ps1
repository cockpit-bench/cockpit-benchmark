[CmdletBinding()]
param([Parameter(Mandatory=$true)][ValidateNotNullOrEmpty()][string]$Destination)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$expectedHashes = [ordered]@{
    'STANDARD_SCORES.json' = '4f31ce7e0a94c0e781b5a0b6eec20096102e29585dd05a3b86934affa72c2f9a'
    'SCORECARD.md' = '4553fa5b6f6f4f2f75c5908421e85c8ee33142c3a88498a7582431a3a8b40cca'
    'SCORECARD.csv' = 'a0ef8cb67dcb2531101e20208e0355c0ab937c9ef50eb58c2784b7bf50be4988'
    'SCORE_RULES.md' = '5ddc67686e0f7f6f485fa12cc77463b6d8fa8fc4cf69ff012f39d1e98205446e'
    'manifest.json' = '9f7e56b65c04ffb63ae91b208fd923cf381ba8bdeb28435680c404b1e089b21b'
    'manifest.md' = 'aa939b9e3212bbeeadf98f4a70837d7840b3daebe046c4de892a4b4977d7a5e0'
    'ACTIVE_EIGHTEEN.md' = '587a684e409a686992ebf5548088fe3c412eb671edad110493a1a1b7eeafd96d'
    'delivery-scope.json' = '53009c8c22349d2a4b5c080e411f035c77ad9fd92463b3fa0f561bf81255bd4e'
    'oracle/APP-03.json' = 'aee3e164260608ec2d77327448c3ee8efc2c8d2cd20b5887c95b0c43e3c0d26a'
    'oracle/APP-02.json' = 'cc14fe77fd0c251f74c9eec78341c60b6d3a4eaaf6295e0982234e4b5ceb9055'
    'oracle/APP-01.json' = 'df82544129c4e5bd8f9ff8ce490d58aea2aed52273f4566ee97b2ba1556abd97'
    'oracle/APP-13.json' = '1dfe4ea655f01a6f4443472eee39b5e40b80b102b52c31dcc7a505295cd24c9d'
    'oracle/APP-11.json' = '3d40b6dfb5f0c5a633f14971f13a32d343628fafd53484ba3099ae2193583846'
    'oracle/APP-14.json' = '758df28f007a9198890bb37a4ae464eb70b8f7fded9ae817e59d3fd24e62b8a2'
    'oracle/APP-17.json' = '0c8182530598a2c8854ab28f42c0249afe7e801ba3badbfdc7b848d21330a2a0'
    'oracle/APP-16.json' = '7ebb9afba592a7b71fd99f70002a2f07dc2f8832ddde4e8fdacc2a45014daff8'
    'oracle/APP-15.json' = '124fa8b963c83cf8472ee649220b531df2f3cca051db86982df946e7fe68d41c'
    'oracle/FW-02.json' = 'f02385dc6b8bff34be2369b8f39bb0f76b36eb6a41e6c55eb9b9d1f2aa798172'
    'oracle/FW-03.json' = '81bbab84d0c1dd560e48777acf94d2ce5b20de7bd833485f58cf4f96ffc14991'
    'oracle/FW-07.json' = '5a436bc0ed987195fed973134413d3a4f17e43c79694d8bcdf24f4b35adf45de'
    'oracle/FW-10.json' = '71a232f17d6f35170f55f6b2c84f0f44ee8428dc672dd7af9b9f009d298f6cce'
    'oracle/FW-08.json' = '6cde573e28507324f4519a442cdea468a0bfb35e0400e58d232cee4c7d8a787c'
    'oracle/FW-14.json' = '05c4d7855e71972a11fb925f778d6fac940ca250004d35235fdc973ac0026e5b'
    'oracle/FW-15.json' = 'd2ec72f2a5ae869979b3c4647de1573fbe342908571bb339bbf9bd7f7ca19eee'
    'oracle/FW-18.json' = '0241822610fcef6f5af34b3500cf474f4f1294d454191dc365d490aa8cfc0865'
    'oracle/FW-16.json' = 'f95ee382fadc3506f742fb6afd1aaa27ce7a886efa19dd6128eed62166d88f94'
    'facts/APP-03.json' = '709a37b27d45221b9d690c8b0e31e6a6d5a6bd5ddc3e756f662c720ca3b58cc6'
    'facts/APP-02.json' = 'ac2924f9ffa4ac49b23254751c2051c0d6f7695c346b181e7fa79c450571bb38'
    'facts/APP-01.json' = '380adde1bcd7af55fed0d8c984a694dae12d3f7d8182ad310a0102b27aa8b9ff'
    'facts/APP-13.json' = '9c78d75b4a33201eec29283b70a9993a0123cdcd09781d6840511c653ad282cd'
    'facts/APP-11.json' = 'ff6391d2e45fff352964da1b66be0dbbb1d49b5c01a63413f771f5e4bd58ace2'
    'facts/APP-14.json' = '2d6e08133968e06fc0a479d37226d964803509d76efac3c5941e5157aeadaaa5'
    'facts/APP-17.json' = 'd84b73c8296375e47382f4d356d5e2e705f3f5657040457e214e884a1a5c8259'
    'facts/APP-16.json' = '440cbe98a0880ee8b388ec3637a546c1b41c324f6b08a89e8bbb7bc2d4ece597'
    'facts/APP-15.json' = '556da80652ecd4ddf28b3596d0a51cd47a5f0d68534310f88b846ec3ebbf560a'
    'facts/FW-02.json' = 'f430bd99aff7f8fe299592bbffa2474c13a19d1ea6f483be6f1130c1a269e9bb'
    'facts/FW-03.json' = 'cb550d98d457a0f6ca6571574a1340dbd1b46bc0457725892f3cfc3c93c40b7d'
    'facts/FW-07.json' = 'dd637a7301ac4f2c06551670779ac1d2542fae9802d8ad39eae9061e63cb53c6'
    'facts/FW-10.json' = '177865f4488b4ad292fce4b8f3e1c311f84ac09f96e9258083f90060fc528606'
    'facts/FW-08.json' = '3656e8a48a7b7755bcd2d1d595b8dd473aced26c221992dc18567f820e29332a'
    'facts/FW-14.json' = '764758cfea638a416da54b9ca16235357d976b7605355c02ca21065bd7ddb6be'
    'facts/FW-15.json' = 'c5ecc5892029e10b443cc2b0a29864b5bd2713f08106a66877aab4008d8f9612'
    'facts/FW-18.json' = 'f2274f5cd698a47bb6ab436490de2b2cf82fe87ae12a9132153515af9f81a3f8'
    'facts/FW-16.json' = 'd8cb06a99aff5b2139ad03d925bf38faa4a76045f3d75623f19443f94dfe162a'
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
$wrapperPath = [IO.Path]::GetFullPath($PSScriptRoot).TrimEnd([IO.Path]::DirectorySeparatorChar, [IO.Path]::AltDirectorySeparatorChar)
$wrapperPrefix = $wrapperPath + [IO.Path]::DirectorySeparatorChar
if ($destinationPath -eq $wrapperPath -or $destinationPath.StartsWith($wrapperPrefix, [StringComparison]::OrdinalIgnoreCase)) {
    throw 'Destination must be outside the benchmark wrapper so source cases cannot inherit Gold files.'
}
if (Test-Path -LiteralPath $destinationPath) {
    if (@(Get-ChildItem -LiteralPath $destinationPath -Force).Count -ne 0) { throw "Destination is not empty: $destinationPath" }
} else { New-Item -ItemType Directory -Path $destinationPath | Out-Null }
$results = @()
foreach ($entry in $active) {
    $kindDir = if ($entry.kind -eq 'APP') { 'app' } else { 'framework' }
    $repoPath = Join-Path (Join-Path $destinationPath $kindDir) $entry.name
    New-Item -ItemType Directory -Path (Split-Path $repoPath) -Force | Out-Null
    & git -c core.longpaths=true -c http.version=HTTP/1.1 clone --quiet $entry.delivery.repository_url $repoPath
    if ($LASTEXITCODE -ne 0) { throw "Clone failed: $($entry.id)" }
    foreach ($property in $entry.delivery.refs.PSObject.Properties) {
        if ($property.Name.StartsWith('refs/heads/')) { & git -c core.longpaths=true -C $repoPath update-ref $property.Name ([string]$property.Value) }
        if ($LASTEXITCODE -ne 0) { throw "Cannot restore ref $($property.Name)" }
    }
    & git -c core.longpaths=true -C $repoPath checkout --quiet $entry.default_branch
    & git -c core.longpaths=true -C $repoPath remote remove origin
    $actual = @{}
    & git -c core.longpaths=true -C $repoPath for-each-ref '--format=%(refname) %(objectname)' refs/heads refs/tags | ForEach-Object {
        if ($_ -match '^(refs/(?:heads|tags)/\S+) ([0-9a-f]{40,64})$') { $actual[$Matches[1]] = $Matches[2] }
    }
    $expectedRefProperties = @($entry.delivery.refs.PSObject.Properties)
    if ($actual.Count -ne $expectedRefProperties.Count) { throw "Ref count mismatch: $($entry.id)" }
    foreach ($property in $expectedRefProperties) {
        if (-not $actual.ContainsKey($property.Name) -or $actual[$property.Name] -ne [string]$property.Value) { throw "Ref mismatch: $($entry.id) $($property.Name)" }
    }
    $head = (& git -c core.longpaths=true -C $repoPath rev-parse HEAD).Trim()
    if ($head -ne $entry.delivery.expected_head) { throw "HEAD mismatch: $($entry.id)" }
    if (@(& git -c core.longpaths=true -C $repoPath remote).Count -ne 0) { throw "Remote was not removed: $($entry.id)" }
    $results += [pscustomobject]@{ ID=$entry.id; Name=$entry.name; Head=$head.Substring(0,12); Refs=$actual.Count; Status='PASS' }
}
$results | Format-Table -AutoSize
Write-Host "PASS: restored 18/18 repositories with exact refs and zero remotes."
