[CmdletBinding()]
param([Parameter(Mandatory=$true)][ValidateNotNullOrEmpty()][string]$Destination)
$ErrorActionPreference = 'Stop'
throw 'Unreviewed draft: 63 FW leaves await independent review; restore is disabled.'
Set-StrictMode -Version Latest
$expectedHashes = [ordered]@{
    'STANDARD_SCORES.json' = '173eb5ab253a363046d9379d9a2d9e31a8d822dc15e1f661cedc89f10a8eef50'
    'SCORECARD.md' = '49f6a98a595e42f563a4e9507cf823ebca4e8376f4d543b14a1097bcc358dfd8'
    'SCORECARD.csv' = 'c3c39e72d8d6af4203571a2c5766ddf6987262fe0ce7d49899cc2362d6f81224'
    'SCORE_RULES.md' = 'c367412668bf3f96231462bad501cec04c0c2bce44a9dbc0206acdaf31ed9465'
    'manifest.json' = '5a667b7e085f68bb80226e520f7cb8563bcfb3c066a37d81915739e7ee94de3d'
    'manifest.md' = 'aa939b9e3212bbeeadf98f4a70837d7840b3daebe046c4de892a4b4977d7a5e0'
    'ACTIVE_EIGHTEEN.md' = '587a684e409a686992ebf5548088fe3c412eb671edad110493a1a1b7eeafd96d'
    'delivery-scope.json' = 'e796d24c5ca158ea89fd2d8675424d3c32150498f10373f52d458a15a975093a'
    'oracle/APP-01.json' = '8b2d40d68b72555d00aebabc76c540fa8391d9513d557f17ace0f219fa2f2177'
    'oracle/APP-02.json' = '84df9b6870252a5aefa862664779b277d3fe0388f694ab8a686c0855cb5c821c'
    'oracle/APP-03.json' = '9829e16af4d81e978043405070310f4fb2b5ce2bf62773957719bc4a615d2390'
    'oracle/APP-11.json' = '2ded94d007ec601bf84031a2d415d54e202b0dc23ff4b65e7acae961b29bc7ee'
    'oracle/APP-13.json' = 'ecee0c19efd3a0b84000626ed3c2e051a6d1adcfb1fd9a47402097ba6dfe56c4'
    'oracle/APP-14.json' = '6fd3e8d147a698c1f822f15e91e5d1a38bce51b7e280b31983ab0e988cee2ac5'
    'oracle/APP-15.json' = '2d29d4001f8d3216c7b6126bec0dd5336548f03d84eb8f424edaaa650c6d1a57'
    'oracle/APP-16.json' = 'fba15c3146b18f2794b9e4806a6cc547504a94952113f16c1705939fe317de64'
    'oracle/APP-17.json' = 'fdb8d22a0c161143927a4f0805769ce455453e7b57b353aebfdec14866098e01'
    'oracle/FW-02.json' = '0374950311dbac47eeb374fb625e539a4eb33cae8cb582615d732a3cea1d401e'
    'oracle/FW-03.json' = '0503d5b51a2dc39835ec384131d35b9e99fdc0e6e890ac9313187060bc6eefe7'
    'oracle/FW-07.json' = '541d907d1aa731b6b9f3f211320a6d5847e845c3f055371ad3dd881cceae5cff'
    'oracle/FW-08.json' = 'e0949dc7dfb3bc49e7ea78f2dec9f70b012d7b3d02474e1843a5419452b93b32'
    'oracle/FW-10.json' = '890cb95047c80d663b82d170b4760c1a0a37bad82659d97dd4c929268f79b26f'
    'oracle/FW-14.json' = '3082202c2b7df6b5c9fcc7bcb636c3bb765daf8f04071e1c00f9c945c0584765'
    'oracle/FW-15.json' = '19dd1e67aef671e7b344156d538ab906afc4135e887120fc747aefc5fdc6243a'
    'oracle/FW-16.json' = '8d54582b681764d63c046a35be937c3020571bbd870ebdb23bf438106cefd6dc'
    'oracle/FW-18.json' = 'b846dc4423dd9e0e423d49876fe281d4217adfbe6de49f81640eac08eefe23f4'
    'facts/APP-01.json' = '380adde1bcd7af55fed0d8c984a694dae12d3f7d8182ad310a0102b27aa8b9ff'
    'facts/APP-02.json' = 'ac2924f9ffa4ac49b23254751c2051c0d6f7695c346b181e7fa79c450571bb38'
    'facts/APP-03.json' = '709a37b27d45221b9d690c8b0e31e6a6d5a6bd5ddc3e756f662c720ca3b58cc6'
    'facts/APP-11.json' = 'ff6391d2e45fff352964da1b66be0dbbb1d49b5c01a63413f771f5e4bd58ace2'
    'facts/APP-13.json' = '9c78d75b4a33201eec29283b70a9993a0123cdcd09781d6840511c653ad282cd'
    'facts/APP-14.json' = '2d6e08133968e06fc0a479d37226d964803509d76efac3c5941e5157aeadaaa5'
    'facts/APP-15.json' = '556da80652ecd4ddf28b3596d0a51cd47a5f0d68534310f88b846ec3ebbf560a'
    'facts/APP-16.json' = '440cbe98a0880ee8b388ec3637a546c1b41c324f6b08a89e8bbb7bc2d4ece597'
    'facts/APP-17.json' = 'd84b73c8296375e47382f4d356d5e2e705f3f5657040457e214e884a1a5c8259'
    'facts/FW-02.json' = '30a5e647c57eb69dff7e1e5a70d91d9b2d71b3bf34cf42701ba98e3c69a1fc39'
    'facts/FW-03.json' = 'af241f50d41c882870ec8c1e7c84d5c5872af782fd39cccaaf40a33fd2fe2154'
    'facts/FW-07.json' = '6c5e38b0fd19d1a68488b5cb9c5e2bc82befa100c54ee3fecb6e28b7a9de2940'
    'facts/FW-08.json' = '988516a428789c78cdaf067d7ac1c60cc12966d8f214d6d3b2cb6c7c2c7a9466'
    'facts/FW-10.json' = '6a3154f9408cc19f50fac521d3a2af2efd824c2cec5cea8d4d0bc42a29e05530'
    'facts/FW-14.json' = 'a260767260f174761febf80b07f81376fbdf4dc5b691f6d87d80da0c5342b7ae'
    'facts/FW-15.json' = 'bebb4731ee7cc97700636fe7b3a3097bbd73158534016f46f88dba782f9e10b5'
    'facts/FW-16.json' = '75ab4c61c1a60210bd5f7a7a001ce31c5309db7bd1e0d6f460d29c8d8e5ac7c7'
    'facts/FW-18.json' = '8e88fdc06e327bd0f4f955122e6938a7c867175cfb5bc6ffef299ca02ba8d011'
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
