[CmdletBinding()]
param([Parameter(Mandatory=$true)][ValidateNotNullOrEmpty()][string]$Destination)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$expectedHashes = [ordered]@{
    'STANDARD_SCORES.json' = '74ee83b30cd637ce94620ada3a75d2851a60360e66551a726c3abb1511b4a279'
    'SCORECARD.md' = '68bb1430bfdf46b5c3aa6b5e170f26777dd16062c4f148c131209dd20d1eb26f'
    'SCORECARD.csv' = 'f5f690d32672274b2ee93c0c6f4e8e9cad87f030301c68b0149a5837c1fbc2f3'
    'SCORE_RULES.md' = 'c367412668bf3f96231462bad501cec04c0c2bce44a9dbc0206acdaf31ed9465'
    'manifest.json' = 'dc39792303862d5d0e08c2e84d286e4fa69adeedec4f15e6f457cf4db4c3848b'
    'manifest.md' = 'aa939b9e3212bbeeadf98f4a70837d7840b3daebe046c4de892a4b4977d7a5e0'
    'ACTIVE_EIGHTEEN.md' = '587a684e409a686992ebf5548088fe3c412eb671edad110493a1a1b7eeafd96d'
    'delivery-scope.json' = '7a76471a780de4d1fae58abc78a8388d52fe0f0c8171deaabb5c05a4bd3215cc'
    'oracle/APP-03.json' = '352d27805caf439b83930a4003fff4dd58cacc784c8e72bcbbdc0abf4fd229e1'
    'oracle/APP-02.json' = '84df9b6870252a5aefa862664779b277d3fe0388f694ab8a686c0855cb5c821c'
    'oracle/APP-01.json' = 'cd3344db669cb65a13deefe094ee1bf45b0e5abc59516ac087b470f698b480c6'
    'oracle/APP-13.json' = 'ecee0c19efd3a0b84000626ed3c2e051a6d1adcfb1fd9a47402097ba6dfe56c4'
    'oracle/APP-11.json' = '2ded94d007ec601bf84031a2d415d54e202b0dc23ff4b65e7acae961b29bc7ee'
    'oracle/APP-14.json' = 'abb83057502ac00a9bbcee020f6e587934bda93dd0e860ef29a265af3b44157f'
    'oracle/APP-17.json' = '934b584c3db4fd95e8bda054ce984ec0e4aa17319f1411d446c246fecd55acb5'
    'oracle/APP-16.json' = 'ddd1bd4fd607b5385da68a929df08965ecc4f850b2619c5c1d1ccb32f1a47322'
    'oracle/APP-15.json' = '08f62fdfa9ce0b92cea8b57ad3bd804b5dec62727f2e966c849b55524d0cd7e0'
    'oracle/FW-02.json' = '6aa30ed92054d87c4eabc5ff7315178751adabcf0ca1134b0b6549dd8f0abc66'
    'oracle/FW-03.json' = 'e6018c938a1ac43ed52dcc0c386b46a9977d0f4a66961aa1bcf82d977d55c4f6'
    'oracle/FW-07.json' = 'e09c4bda7cc28900cfe285fec8c8a38f846ac97fad4ae89f4271dc9a072d1b8e'
    'oracle/FW-10.json' = '3c875b952277574510a921bfecd7bd69ccafa736468a38186ab4713add5ab30d'
    'oracle/FW-08.json' = 'a3cbe15f0a1da11504b9230c9ec9df4e3f2374eaa00a13bcdf5d72493eb63446'
    'oracle/FW-14.json' = '462cca89f815b9a7dec5463ab1efca20062d536c4578af7a92515d04d51bac6b'
    'oracle/FW-15.json' = '2547ad0600dfe20f85372cd9383eebc5bec5cd492eb7f249b29d690efc40a4b0'
    'oracle/FW-18.json' = '177a144e1712c67e735dfcb3d311372f8803f87cb9bdc613af8a7f834557d768'
    'oracle/FW-16.json' = '169616acedf01424314aa3cd953b7236dfa2ffd12f41e8047d90c2025b39386f'
    'facts/APP-03.json' = '709a37b27d45221b9d690c8b0e31e6a6d5a6bd5ddc3e756f662c720ca3b58cc6'
    'facts/APP-02.json' = 'ac2924f9ffa4ac49b23254751c2051c0d6f7695c346b181e7fa79c450571bb38'
    'facts/APP-01.json' = '380adde1bcd7af55fed0d8c984a694dae12d3f7d8182ad310a0102b27aa8b9ff'
    'facts/APP-13.json' = '9c78d75b4a33201eec29283b70a9993a0123cdcd09781d6840511c653ad282cd'
    'facts/APP-11.json' = 'ff6391d2e45fff352964da1b66be0dbbb1d49b5c01a63413f771f5e4bd58ace2'
    'facts/APP-14.json' = '2d6e08133968e06fc0a479d37226d964803509d76efac3c5941e5157aeadaaa5'
    'facts/APP-17.json' = 'd84b73c8296375e47382f4d356d5e2e705f3f5657040457e214e884a1a5c8259'
    'facts/APP-16.json' = '440cbe98a0880ee8b388ec3637a546c1b41c324f6b08a89e8bbb7bc2d4ece597'
    'facts/APP-15.json' = '556da80652ecd4ddf28b3596d0a51cd47a5f0d68534310f88b846ec3ebbf560a'
    'facts/FW-02.json' = '30a5e647c57eb69dff7e1e5a70d91d9b2d71b3bf34cf42701ba98e3c69a1fc39'
    'facts/FW-03.json' = 'bf809b790a598101a1abf24ff60d96ca5e0c20433827a4467b8946a1c74a6573'
    'facts/FW-07.json' = '6c5e38b0fd19d1a68488b5cb9c5e2bc82befa100c54ee3fecb6e28b7a9de2940'
    'facts/FW-10.json' = '6a3154f9408cc19f50fac521d3a2af2efd824c2cec5cea8d4d0bc42a29e05530'
    'facts/FW-08.json' = '29ba476fb514a68786b6a648e3373fcfba409f6541cc6f0b2594f6708964f77a'
    'facts/FW-14.json' = 'a260767260f174761febf80b07f81376fbdf4dc5b691f6d87d80da0c5342b7ae'
    'facts/FW-15.json' = 'bebb4731ee7cc97700636fe7b3a3097bbd73158534016f46f88dba782f9e10b5'
    'facts/FW-18.json' = '8e88fdc06e327bd0f4f955122e6938a7c867175cfb5bc6ffef299ca02ba8d011'
    'facts/FW-16.json' = '75ab4c61c1a60210bd5f7a7a001ce31c5309db7bd1e0d6f460d29c8d8e5ac7c7'
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
