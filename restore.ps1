[CmdletBinding()]
param([Parameter(Mandatory=$true)][ValidateNotNullOrEmpty()][string]$Destination)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$expectedHashes = [ordered]@{
    'STANDARD_SCORES.json' = '36049ecbd26550efe4a7c6512090d0a329186ee91887c49d50dc49b16c5a714d'
    'SCORECARD.md' = '5f8072888178ad905c9a03b71b04609b59cde2a836bc8bc37b5cceb335e242ac'
    'SCORECARD.csv' = '5b831e8400bc478dafbe27e3252ac9b82c824e1b51a72d2cb853754d22ffc2f8'
    'SCORE_RULES.md' = '617c6d8772466f51aa31142eaf4d87198ee70c78a42dbaa52b6821401a5e57d7'
    'manifest.json' = 'fbd7a5d2df241bdffeb25cdd6f3300027265b65dbbc4bf1933102b0b75fac6dc'
    'manifest.md' = 'aa939b9e3212bbeeadf98f4a70837d7840b3daebe046c4de892a4b4977d7a5e0'
    'ACTIVE_EIGHTEEN.md' = '587a684e409a686992ebf5548088fe3c412eb671edad110493a1a1b7eeafd96d'
    'delivery-scope.json' = 'eae536c4fedb81f4947e351540bc7577e14fbce08f5bf7a9b2bfa624d90093de'
    'oracle/APP-03.json' = 'a99972df57090c7c30f8f922662a89c2139eded096fc07c66861748e7800de62'
    'oracle/APP-02.json' = '298d5684a0aa3a234890889f7707a2a7d18dca37fd9d0033ced2260ae809f6c9'
    'oracle/APP-01.json' = '8fdc554e9a113fddc32d2e9877eea6986588db4740f5d27bf3827f45a7974efb'
    'oracle/APP-13.json' = '97bdc4f9974a8c3ae0d4517d2a939baeb7777e546bb035edc655962fa7d7cef0'
    'oracle/APP-11.json' = 'fd8bcb2f468fee5f5ec5bb63b3d3535ac99edcf1cd48bb32d7b86352f4a9873b'
    'oracle/APP-14.json' = 'f56d33649c42ad6e8e0287477afb0602ab1d39aaa49f58a9b7cf33cac44032b6'
    'oracle/APP-17.json' = '60d0fd9ce5b21bde0db032dea9bdc6c59ba3e58b7952e3b10206223f139069aa'
    'oracle/APP-16.json' = 'b2f9d408f13fe7f855a7ee5437882840cf58938f6b03c1cfdf63978d7e3e9726'
    'oracle/APP-15.json' = 'dd3eef49e1dab2f2eee52563554ee77166d0c967a8ee9bf13fc8f5080861182e'
    'oracle/FW-02.json' = '560cc16d3eb57955631284a55b9bfa2c79d008f050c7297cadfe5c58aeac7aa7'
    'oracle/FW-03.json' = '728056bd64705419b19089c4d78b0e4b002acb41c7c34c1ace5e6b0013fd2f90'
    'oracle/FW-07.json' = 'd5dc659659eb3839cb3e44bea03a59a61fd6399c4845de99323ae5697500d9ee'
    'oracle/FW-10.json' = '616fa2f6d7ae63d09db3e5da8f41c9ed6f0de07651ac6f659f5cde6bf3a3bce8'
    'oracle/FW-08.json' = '92d2cf26c1cae7dfbe5dc659af539fdb5c767f4fb9714f2bf3f7dd9fbb2b6a93'
    'oracle/FW-14.json' = 'd25d2df009302250148ecda761636f4493a55a5622f17df0e1397f78f48a6b48'
    'oracle/FW-15.json' = 'd9dd1ea163f1787134bd008b4b76adc224dedcbfda7f83b75ebc3f5fa32132da'
    'oracle/FW-18.json' = '7ea10104c2035aeef36558bb0a72f2a25df6ec6c79ddf46f5c906649d623757b'
    'oracle/FW-16.json' = 'da2ad02d56eb8614f6d73f8ebbfd22662d06e6238be785ca0006770e8863b91f'
    'facts/APP-03.json' = '9aceacabdf4298dcefd6a99e4ce8eca1d4660ad7bf4835c2ae40fd14ae0a4649'
    'facts/APP-02.json' = '5f6217067eb70f98c0186361dc94c8a7034a53e26239bddaea1d7bb8259c0bb9'
    'facts/APP-01.json' = '70ad1fa516d07ccda410bc68c3f818209e728f7fc91c1dc5bfbb5cd4ee6c6843'
    'facts/APP-13.json' = '7b2bcc524ae7e80aab4f1c5564fede333671246ce8b5201779c639f77fed1d8a'
    'facts/APP-11.json' = 'b7404065f88560c7c4166faa696f7aaa395fb4d0b1c1fbe696a0fb12fb83d11f'
    'facts/APP-14.json' = '7d2ff2ed674cbd5cb7cb625853fa6af4239df670069ea57cfe7b5418ba889a75'
    'facts/APP-17.json' = '40d21a5ebfbae0f7a43398ed568099e4960e0f6c2a6020729bf42dc7bacf770d'
    'facts/APP-16.json' = '8674726ceb247086c2d6206694c27311f869e061419624fafbf7dde5a9f01531'
    'facts/APP-15.json' = '49caa4eec1c3a3361dd60d0c4618f119e85ced962a1c4425d1cafa4920512556'
    'facts/FW-02.json' = 'b42891899cffd912885b284c1b5e101266fa963b86e9a012fdbc2b7cbb330a2c'
    'facts/FW-03.json' = 'c45382fb17afc25f4b49358e0b247c08233d7125a1753c52d8824ed9bcccf6fa'
    'facts/FW-07.json' = 'aa7f170622030959e9bbdb8cc61547c19cd8fd9412e0e4e52c067bfee58987a2'
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
