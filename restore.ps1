[CmdletBinding()]
param([Parameter(Mandatory=$true)][ValidateNotNullOrEmpty()][string]$Destination)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$expectedHashes = [ordered]@{
    'STANDARD_SCORES.json' = 'a2e4c996bad1fefcab68fd9f9154c766508189a5bd90fdb56d047ff149342981'
    'SCORECARD.md' = '86c1577ea40e3118e29533fc8fd8e360709963f948c1b5450e62381f705273ca'
    'SCORECARD.csv' = '57b2e3598ef023355c5d802b4dcfd5964d4c544f0606ae318989ee21285ee70d'
    'SCORE_RULES.md' = 'c367412668bf3f96231462bad501cec04c0c2bce44a9dbc0206acdaf31ed9465'
    'manifest.json' = '887d2e81bddb188047224a7de145800db6e3d4c12509a1cf9cbe757272da4c9e'
    'manifest.md' = 'aa939b9e3212bbeeadf98f4a70837d7840b3daebe046c4de892a4b4977d7a5e0'
    'ACTIVE_EIGHTEEN.md' = '587a684e409a686992ebf5548088fe3c412eb671edad110493a1a1b7eeafd96d'
    'delivery-scope.json' = '440f57ca6412379a7b7613d10dcb9614f8309b8c0b6e3a59f8314ecc4c6284f2'
    'oracle/APP-03.json' = 'b9c83a8ab7965b2564c086c47ac2912862df40d7b66f5fef31921c57fddcd5fe'
    'oracle/APP-02.json' = '941990dd6634dc21aa105699a9d983d53949013e0482b317bbf2ec6b9b3c36a8'
    'oracle/APP-01.json' = 'bcdf2998030fa637cfa56bacb1ebf58d32ab980e6ffaaa4850e4eefd456d35db'
    'oracle/APP-13.json' = '1ade314c207d1ab3508c886b99b04906b5a2525ccff6ed146793cdcb71b773b6'
    'oracle/APP-11.json' = '71722cbfcbbb46a6c595cbd737b0da85ab96cf99d5ee00a60bd378b975a084d7'
    'oracle/APP-14.json' = '50ea5d2cd09cba948ff22b02845da9d20e8e0f94f70a95a359a2ffa468d69b8c'
    'oracle/APP-17.json' = '584fc8b17dea7f52e2f16d93278699f3a252d2440ea5876c82c018f78dd7d053'
    'oracle/APP-16.json' = '938a91d7a5176ad2ef88fd4e6701932df912a71f2dd72fb5559f44bb77788a60'
    'oracle/APP-15.json' = '0832954b58ae2705e75079feb29da7a5d13a4ffb7efd1a42c1faaa24ebfaf326'
    'oracle/FW-02.json' = '4fa4a88dcd3be6eef36d7dd34b1164f8d48f48dfb0c6c74c93d8d44a39d54c83'
    'oracle/FW-03.json' = '664c70d6871f6d52e8f44ab9f92212b219838f5b096c6a9e2b3d1599a97c18d8'
    'oracle/FW-07.json' = 'b521e383817def995af30500178faf3cea23673f0ee68ce6b9b43c23e6460a44'
    'oracle/FW-10.json' = '46e3ec1d3ef4a15bcbb020c500274b16f210e1d671b9737e6192cd4976a584c3'
    'oracle/FW-08.json' = '4fe4946d1acb435e63f7bf442bac13df402d69515509d5986be43e5ac6045821'
    'oracle/FW-14.json' = '9cc55bd53f017993067085680a71b58c958b5a48b5fbb7954af0cc77a7ca77fe'
    'oracle/FW-15.json' = '00a4d3aa0efacf7c492562e11ad37384f2b1b7d578f1a2531872b1f3a3e043f4'
    'oracle/FW-18.json' = '01cadbdfd93aefa049952bed7c518c285fcefc1671c249aaa2023ca70d67ef09'
    'oracle/FW-16.json' = 'a26636e18580d5b36e64a56043c9ea0e317a381d98e5a877433403550d5c006e'
    'facts/APP-03.json' = 'f513f12d1d7b722611d33e9107095740c50c86ac6178827cc8fce150c598360f'
    'facts/APP-02.json' = 'c8bddded56d43825b3e1ebe651ca17a20bb99a8395f870e9328109ee1817ec4b'
    'facts/APP-01.json' = '4e4090e4a92e8f9b6d8ac4a0cbb4f9e6af1b5ff748088bc5b93994426deb90c1'
    'facts/APP-13.json' = '66a30642b35f4eb5fddd400ee4d10ac119a0f857ef6aff29b0ff800b8b90ad1e'
    'facts/APP-11.json' = '0c930d051e378b3a8155c32fd597cd4fa825bf5ab0c03d9716f30e5256db072e'
    'facts/APP-14.json' = '41b0881194a1a6ee5ce17840520005890f83022a0230f1cba2cc2708e50bb169'
    'facts/APP-17.json' = '92fa92387e0e502d2267140c49f2b0837ea9aaab93926c86991f6d069212e210'
    'facts/APP-16.json' = 'a130022e3b02960cfc7a306ebc1dcaa268967b16887e3eec8ca761537337ce36'
    'facts/APP-15.json' = '067bc3e97e98d0e2ba79e32ceee8984aaa521a06306fb26b3c7f4317eba53788'
    'facts/FW-02.json' = '4da8a0fd8da09ce29e9eade9acb63cb9a28e4f6988cd27ddaac87b07df3bb8f0'
    'facts/FW-03.json' = 'bd24da16afb1cdd5933e8f35ed131cb211c05c76092ac01841afc4a7830611aa'
    'facts/FW-07.json' = '1a0772ee96b251f7f24e183f1834c0cfac1376cc073f2f3b43d83355b5ef11cc'
    'facts/FW-10.json' = '2714ca278cf2f03e7d62a004a9ca40270b4df2b0d69ef5f6951ea6e5c992b5ac'
    'facts/FW-08.json' = '68c8abcca1ed1e48b588d031379b3144d757372ca0b14105bf6a3524d9c83a4d'
    'facts/FW-14.json' = 'de2eefff556055d8c2f996645d2acb632102967239d6b4bad05d6e8c65863793'
    'facts/FW-15.json' = '92bcefaf3e9017188d68c75a111579e4d7c31551079c75fe1e523888164507c7'
    'facts/FW-18.json' = '4d57cddb5784aa9b5e4fd218255e3e5a8767a0411e312c5715837be66eaf9028'
    'facts/FW-16.json' = 'b267a93341b2a991e0290b1bdd6bd7cad4bffe1f4502f046d2a38cf98f486047'
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
