[CmdletBinding()]
param([Parameter(Mandatory=$true)][ValidateNotNullOrEmpty()][string]$Destination)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$expectedHashes = [ordered]@{
    '.gitattributes' = '5550472b34249d85a794952825db528251956dd8bfff9dd17589ea767446f588'
    'ACTIVE_EIGHTEEN.md' = 'f64d70be58fea89e65d152c839f8e47a386f5e5db8c43ec81cda6008ad35881b'
    'LICENSE' = '950f20ff178debfcf2526200837304a7512f39c022dc1f9105a6e0af62788df0'
    'NOTICE' = 'ff71f002bf010747ebc6a65858605d93e07bdbf19e2514ea0bab67f6e8bb1420'
    'README.md' = 'dc8912d27817c0f0eb1bc4291cf03694b43ea14b30280945757ee77a5e007143'
    'SCORECARD.csv' = 'd3e52f7445f3ca0a454f9c705a270603544da594746c0af6286d2894a20e227e'
    'SCORECARD.md' = 'c598770bf842487cba7b7564a872d53838ef9266e65e99d0a1d74d137ff256f7'
    'SCORE_RULES.md' = '240671d2317b745170c35c77e8f029c10d871177d3b160b6f26e608c3ef13544'
    'STANDARD_SCORES.json' = '5dc2e8377652b3e4685b19d9563b518c8f016d0abbb644e2b7af6686011df434'
    'delivery-scope.json' = '3c9e8c2e1062db1b16f0abe8c7f4ce6f7565799a2b72f9df94dde60f50104c24'
    'facts/APP-01.json' = '96ffc5f9a4ce52fc1c0db7c26e63a7adbbd5e9e231355d5cb1ad1bc141a53525'
    'facts/APP-02.json' = 'e3295964a88e81f34b7202317670c447367e630523e2c82f48118b15d6fab1dd'
    'facts/APP-03.json' = '8b7a88a99fad271a0b184e2f0e107d7ac94a8760a164d3e7746869a3277a01d1'
    'facts/APP-11.json' = '42df89d5468e495c16993e5458a181aadcfdaa9ecf6d99199913abb528c0a4c3'
    'facts/APP-13.json' = '2e83d20400abf40330d71e12dce2ade30f8edf2652f74cd1b973bb7f35b12b40'
    'facts/APP-14.json' = '30b78306be3d690882db1e7de0c5a255397319cbeb0a94e4debba8c5ada865af'
    'facts/APP-15.json' = '9472160e3b33c3bd026c64d0333518610bcffb317ba3a6989bad7af209cb4dee'
    'facts/APP-16.json' = '69d384f0c5417a5fa4e232ccd0a7d9c56b9923f6d49a95ef2c7e806320750715'
    'facts/APP-17.json' = 'b23f608cea812efeec6f468b51200f6fee6acdd47b4a959d68928390da3e3ce4'
    'facts/FW-02.json' = 'ca34605215ab0bb16e77951435bd629a7ef87d4549f454f6fa93ad0efac74872'
    'facts/FW-03.json' = 'f3f5165f3406eddcfefb64eed7a9be86f83423768b317932fd737e1baf3e4f38'
    'facts/FW-07.json' = 'ae1adf76937474ebdffda6adf8e789f0b17298ac237b45531c55bc72c31e855a'
    'facts/FW-08.json' = '7655e5817bfe50a941002c077a5243e865678fc08c1012cbf3cee327a9f55a2c'
    'facts/FW-10.json' = '0d5f2dd22753aaa239e4805d4d563a9e9dbab103b7bfd4fb52c8d2573b430b0d'
    'facts/FW-14.json' = '7ccd0f39466788ff777bb3e861679d0c0a4a25830513ee4fcabc782dd89045f8'
    'facts/FW-15.json' = '29188755cf8744c00dd26af12acba6e7802e527f5ff46dd4460bc34f19642036'
    'facts/FW-16.json' = '158eb88bd3b51ea414a91f8eaeee6e6ded4866ad2f077c453c0ea65e4933620e'
    'facts/FW-18.json' = '8981b735ae21d82bcd3f7303122cd3df191b179f8fe34d7a7ccbe8ec7f3744a3'
    'manifest.json' = '3efb70308e0e331d4188bcb21477528b8413fc5c00d1d37280627aa4bd3a7474'
    'manifest.md' = 'a8130ed19f05673eb00fa8f8e6ede623513fa95c9210c964bd09d9b92f55ad87'
    'oracle/APP-01.json' = '331adb70a9a72b477730426893217229985cd170819ea5384e5258d6f021c859'
    'oracle/APP-02.json' = '978bebbd4cb77be5a54dd73febbcd101a9e933cebee335bdd70ee3569926a453'
    'oracle/APP-03.json' = '40f9bd288176c805d66ba31e0eccbb536b008cded6ea6a03e5558f74595f5ab5'
    'oracle/APP-11.json' = 'ccc779b61fccbfc5d13edc6c21fb438a402db570baf6d56e7d3bf4ce2b3c1e3f'
    'oracle/APP-13.json' = 'ff79383eca6dd40f9062f25b5e435f369a57b778e5fbed75ec12cf0e3cf5992c'
    'oracle/APP-14.json' = '24892f041ba89a3e235ca8c404a29532ed7b7319705d454667ff4d0b29f56b19'
    'oracle/APP-15.json' = 'd603d0e15ddc3e51281adff2c0069a2d7531fb5c95fda2a242a8f62edc79e8d8'
    'oracle/APP-16.json' = '3cfa7a8f366211bf3fe8283d8b9d2f86c34598a4a8089f224f3520a7db3be674'
    'oracle/APP-17.json' = '8444913da2385bb63bf3987deb39a3030e8aa64761a5ae5ec73e6b2c106abb63'
    'oracle/FW-02.json' = '9281ac733f8f14272eabbeaa1a8612e8c64fd0e5e1f682dd3712d2bdb5d5c66d'
    'oracle/FW-03.json' = '5b9e495472285ec14462cb85c983d0122a040325892d0566360d2f14dbb24268'
    'oracle/FW-07.json' = 'a13c7e04767d49deda5fa1e4c1005d2fcdb9e72c8c833767a568ae597a20afd6'
    'oracle/FW-08.json' = '0ff49bfbbf9d53ec4e766b5e404a60d5009c72f055c76430db18e9317acce560'
    'oracle/FW-10.json' = 'f6e403e9e360b3f06716b08b5221bc47c0c0d59c3ae7b9c38c3c6c1eb732729d'
    'oracle/FW-14.json' = '2b44098dbaa543f36c39202358abe5ceb1dca3576a9937256b0210c5839253f3'
    'oracle/FW-15.json' = '0cc22b77759d8523b8320f7b612009756aacf209bf6dcbc3e744567c756535df'
    'oracle/FW-16.json' = 'fa88ad715dcd8d6778616bedbd13f9b0ded5fdb96a0665639b5dbacc1d05bf4b'
    'oracle/FW-18.json' = 'ccf6bf33d34517c8032bc080fd0b7a1e98b9ac89ee6ee481af019fee5eca91b0'
}
function Invoke-CheckedGit {
    param([Parameter(ValueFromRemainingArguments=$true)][string[]]$GitArguments)
    $result = @(& git -c credential.helper= -c core.askPass= -c credential.interactive=false -c http.extraHeader= -c core.longpaths=true -c http.version=HTTP/1.1 @GitArguments)
    if ($LASTEXITCODE -ne 0) { throw "git failed ($LASTEXITCODE): $($GitArguments[0])" }
    return $result
}
if (-not (Get-Command git -ErrorAction SilentlyContinue)) { throw 'git is required.' }
foreach ($entry in $expectedHashes.GetEnumerator()) {
    $path = Join-Path $PSScriptRoot $entry.Key
    if (-not (Test-Path -LiteralPath $path -PathType Leaf)) { throw "Missing $($entry.Key)" }
    if ((Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant() -ne $entry.Value) {
        throw "SHA-256 mismatch: $($entry.Key)"
    }
}
$manifest = Get-Content -LiteralPath (Join-Path $PSScriptRoot 'manifest.json') -Raw | ConvertFrom-Json
$standard = Get-Content -LiteralPath (Join-Path $PSScriptRoot 'STANDARD_SCORES.json') -Raw | ConvertFrom-Json
$active = @($manifest.repositories | Where-Object { $_.delivery_status -eq 'active' })
$pending = @($manifest.repositories | Where-Object { $_.delivery_status -eq 'pending' })
$leafCount = 0
$maxScore = 0
foreach ($repo in $standard.repositories) {
    $leafCount += @($repo.leaves).Count
    foreach ($leaf in $repo.leaves) { $maxScore += $leaf.max_score }
}
if ($active.Count -ne 18 -or $pending.Count -ne 22 -or @($standard.repositories).Count -ne 18 -or $leafCount -ne 171 -or $maxScore -ne 828) {
    throw 'Invalid Validation-18 denominator.'
}
$destinationPath = [IO.Path]::GetFullPath($Destination)
$wrapperPath = [IO.Path]::GetFullPath($PSScriptRoot).TrimEnd([IO.Path]::DirectorySeparatorChar,[IO.Path]::AltDirectorySeparatorChar)
if ($destinationPath -eq $wrapperPath -or $destinationPath.StartsWith($wrapperPath+[IO.Path]::DirectorySeparatorChar,[StringComparison]::OrdinalIgnoreCase)) {
    throw 'Destination must be outside the wrapper so source cases cannot inherit answers.'
}
if (Test-Path -LiteralPath $destinationPath) {
    if (@(Get-ChildItem -LiteralPath $destinationPath -Force).Count -ne 0) { throw 'Destination must be empty.' }
} else { New-Item -ItemType Directory -Path $destinationPath | Out-Null }
$savedPrompt = $env:GIT_TERMINAL_PROMPT
$env:GIT_TERMINAL_PROMPT = '0'
try {
    foreach ($entry in $active) {
        if ($entry.name -notmatch '^[a-z0-9]+(?:-[a-z0-9]+)*$' -or $entry.delivery.repository_url -ne "https://github.com/cockpit-bench/$($entry.name).git") {
            throw "Invalid source target: $($entry.id)"
        }
        $advertised = @{}
        foreach ($line in (Invoke-CheckedGit ls-remote --heads --tags $entry.delivery.repository_url)) {
            if ($line -match '^([0-9a-f]{40,64})\s+(refs/(?:heads|tags)/\S+)$' -and -not $Matches[2].EndsWith('^{}')) {
                $advertised[$Matches[2]] = $Matches[1]
            }
        }
        $refProperties = @($entry.delivery.refs.PSObject.Properties)
        if ($advertised.Count -ne $refProperties.Count) { throw "Remote ref count differs: $($entry.id)" }
        foreach ($property in $refProperties) {
            if (-not $advertised.ContainsKey($property.Name) -or $advertised[$property.Name] -ne [string]$property.Value) {
                throw "Remote ref differs: $($entry.id) $($property.Name)"
            }
        }
        $kindDir = if ($entry.kind -eq 'APP') { 'app' } else { 'framework' }
        $parentPath = Join-Path $destinationPath $kindDir
        New-Item -ItemType Directory -Path $parentPath -Force | Out-Null
        $repoPath = Join-Path $parentPath $entry.name
        Invoke-CheckedGit clone --quiet --no-checkout $entry.delivery.repository_url $repoPath | Out-Null
        Invoke-CheckedGit -C $repoPath fetch --quiet --tags origin | Out-Null
        foreach ($property in $refProperties) {
            if ($property.Name.StartsWith('refs/heads/')) {
                Invoke-CheckedGit -C $repoPath update-ref $property.Name ([string]$property.Value) | Out-Null
            }
        }
        Invoke-CheckedGit -C $repoPath checkout --quiet $entry.default_branch | Out-Null
        Invoke-CheckedGit -C $repoPath remote remove origin | Out-Null
        $actual = @{}
        foreach ($line in (Invoke-CheckedGit -C $repoPath for-each-ref '--format=%(refname) %(objectname)' refs/heads refs/tags)) {
            if ($line -match '^(refs/(?:heads|tags)/\S+) ([0-9a-f]{40,64})$') { $actual[$Matches[1]]=$Matches[2] }
        }
        if ($actual.Count -ne $refProperties.Count) { throw "Restored ref count differs: $($entry.id)" }
        foreach ($property in $refProperties) {
            if (-not $actual.ContainsKey($property.Name) -or $actual[$property.Name] -ne [string]$property.Value) { throw "Restored ref differs: $($entry.id) $($property.Name)" }
        }
        $head = (@(Invoke-CheckedGit -C $repoPath rev-parse HEAD))[0].Trim()
        if ($head -ne $entry.delivery.expected_head) { throw "HEAD differs: $($entry.id)" }
        if (@(Invoke-CheckedGit -C $repoPath remote).Count -ne 0) { throw "Remote remains: $($entry.id)" }
        if (@(Invoke-CheckedGit -C $repoPath status --porcelain).Count -ne 0) { throw "Dirty restored worktree: $($entry.id)" }
        Write-Host "PASS $($entry.id) $head refs=$($actual.Count)"
    }
} finally { $env:GIT_TERMINAL_PROMPT = $savedPrompt }
Write-Host 'PASS: restored 18/18 with exact HEADs, all heads/tags, clean worktrees, and zero remotes; pending 22 not cloned.'
