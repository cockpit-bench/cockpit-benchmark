[CmdletBinding()]
# After a network interruption: ./restore.ps1 -Destination <same-directory> -Resume
param([Parameter(Mandatory=$true)][ValidateNotNullOrEmpty()][string]$Destination, [switch]$Resume, [switch]$IncludeSubmodules)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$expectedHashes = [ordered]@{
    ".gitattributes" = "5550472b34249d85a794952825db528251956dd8bfff9dd17589ea767446f588"
    ".gitignore" = "6feaded4e28ea86e001a6751b4e3d960e8b7c31b9616ff9936b79297086e809b"
    "ACTIVE_EIGHTEEN.md" = "f64d70be58fea89e65d152c839f8e47a386f5e5db8c43ec81cda6008ad35881b"
    "LICENSE" = "950f20ff178debfcf2526200837304a7512f39c022dc1f9105a6e0af62788df0"
    "NOTICE" = "ff71f002bf010747ebc6a65858605d93e07bdbf19e2514ea0bab67f6e8bb1420"
    "README.md" = "7f07dbcb51a2cd9c2db30d75afdc682507a1fef7902f769bebf5108dc7fa5132"
    "SCORECARD.csv" = "5689fa70a5cef8229a2bf2ffc24854d2f8c236e2b6fad152d947b143f409ff6f"
    "SCORECARD.md" = "508efed7edc46b06b1901e5d3d26639a01541857ab5d0a28155850c8cc6d2c7f"
    "SCORE_RULES.md" = "fc488cf70619a1f72e7e9ca808c228a0a45e0a9dd8cda5a540438cb0602212d4"
    "STANDARD_SCORES.json" = "2627cb2f3ac353634af0ce4bd266947f52f24448e3621a6dd0b87f8b1beabb97"
    "delivery-scope.json" = "eaaf9dcaa5685b98904be4a404e1f1ce161a893d8c162c4d429a3d92f18ccb6c"
    "docs/BOUNDARY_CANDIDATES.md" = "b36c1913545682c23f7dce0c31ca10cd07e9ff8b7909c32d3a437808bc703fdd"
    "docs/COVERAGE.json" = "15d62231c42e43be111bb8f781cf577e54df56e92011bd213a4cf6dafe764841"
    "docs/COVERAGE.md" = "ece8d20d0747dd2a285dfea85558a27538c0f9a429b56273308928e8b2d5d0ef"
    "docs/EXECUTION_SPEC.md" = "4f2facff28ae746949c2facc991cd7749f356019709c064219afb12499808dee"
    "docs/REAL_REPOSITORY_GUIDANCE.md" = "862ad8541dccc85dd6c752aeb1c1645f5a4dfc6389c38158985945ef8a1b3051"
    "docs/REVIEW_FIXES.md" = "51c84eb2a69373646a16ed04b35241b87795336fd329d3721f7de5aeb3cdc7be"
    "docs/RULE_FIXES.md" = "2eac51b7ddc3877d9cf309e948af300a089e3ed416ba41a1919818fbb4abc154"
    "docs/VERIFICATION_INPUTS.md" = "d75b9449b76818769ee3b1bb41e89408cfd3a3a8893d76e918a11b66a6590d38"
    "docs/WEB_REVIEW.md" = "f3d9f91e8b2547a588f795387349ff73b47ab8c9847a9c7213327d2ee83fcf01"
    "docs/boundary-candidates.json" = "75a473e3ed461e2ab732e8db9dee9fcb2cab5fb16edc91994843efce3272c94f"
    "facts/APP-01.json" = "fc41170a0f2a11de0289ad5727298421202ce0a8254236307c203ef71e129d20"
    "facts/APP-02.json" = "ce13f4a95c600b2b28a0f40404e1de8a3e9b1990bc2759bc5a1793246b084869"
    "facts/APP-03.json" = "a08371fd039091700c1a2c351aa53236734af2f7ccca7da5cf1e95cd2da8f150"
    "facts/APP-11.json" = "03a7fd0aa474510d761aa5d5855cc7ef06189121d58ee4f4a85201874af8afcf"
    "facts/APP-13.json" = "976fdced28507742000597daf7b4b731aedddc5f917436c46ae500f6bdaeb83f"
    "facts/APP-14.json" = "a1862a774656ce6b7b4d5f3c18ce2096270279642b663564bcb16e30db8225c5"
    "facts/APP-15.json" = "6db1abda8dff2b679566fbfc65c91981b384d2f893f24df984df7847c52a46dd"
    "facts/APP-16.json" = "cd71bc4d680ee9e630a27964170e2cb61ffa95a6a683c2e69a28e7d9e6b167a5"
    "facts/APP-17.json" = "274b984f60161e947e5850ce0d9aae0f3b06d38cdca1cec6aa73efb5de0b9d84"
    "facts/FW-02.json" = "de2056bff95b027afc0a4619a8de124723ccdb1d8246079782535a6184aaeda5"
    "facts/FW-03.json" = "e624fbe9360c252e1d7bf4d780c353328ca5a62cb2023cd512bd5bdc3b2a8e65"
    "facts/FW-07.json" = "c58f0f8062cd4864d575cdaa9d60055b63490e894dedf7110859c52949e9a534"
    "facts/FW-08.json" = "034eef4643abd5b1e2b35b34425a8ecaad7c2b714e03a60a908a1e5b316183fe"
    "facts/FW-10.json" = "2f95cb89a8d9eda59552482b56bb0b28ce9187b5f1b01457d82b71fad410ca33"
    "facts/FW-14.json" = "b75070c714fa6b9e299d55c9bd1f697859b3b81bd07d657d5b165a4527579e0a"
    "facts/FW-15.json" = "4309bdcfcd0e5836b591044e8b1700923095da4ba6aab1c0597612d88bea9c63"
    "facts/FW-16.json" = "53adbc7c59acb2d9e85012811f303649b7a4619e663e72006c1fae3e298108da"
    "facts/FW-18.json" = "5f45507668cb0060404088941f3fd5b0ffe090c5289c7f33e3d0377ee5ce11f5"
    "manifest.json" = "0ba558d302775148ba781f97143e712b999f43e26e6b6aa8ccbe47f753ff49bd"
    "manifest.md" = "a8130ed19f05673eb00fa8f8e6ede623513fa95c9210c964bd09d9b92f55ad87"
    "oracle/APP-01.json" = "45f9a3edf0a28d1b54d51bbaf5c4da4f02819b6aebff69d0f94c7a1cdf21c360"
    "oracle/APP-02.json" = "88b4cee5f712d4bd6a6e31d2c459b6f0307013b24b9f78d7ef6bc5d76f099845"
    "oracle/APP-03.json" = "0ea56f2db282bcdae60d300e0cbdb98465303ec90829790ac152462a569b05c9"
    "oracle/APP-11.json" = "90f7f3ff1739881f7ab8cbbd9632a2382424a50eea5750a4a60a7437a6979a4a"
    "oracle/APP-13.json" = "d612fda0fc4cf4026a7e2763a49064d4c552b1ae16bf903f25d21b93237ffb82"
    "oracle/APP-14.json" = "2a568f2de62de5c9e0362627a48731b1d28a35f625c999406343f4639a07b350"
    "oracle/APP-15.json" = "fcf9be7ea353aead55a524c77f34a8efb182dbc91e0271510a4ec79bff22368c"
    "oracle/APP-16.json" = "02dd86d1265a45263e7ce1399ec2cdd7af8cfbc1dd03342d48ec41a0fb920b09"
    "oracle/APP-17.json" = "2a1143e3864fd7e0d5d5120dfc96186579188ba53f87f572c63559b86060bd81"
    "oracle/FW-02.json" = "e8b65f22458582facf2de6695cbd5f7f2d3e185273fd3a1e04048353a9712c84"
    "oracle/FW-03.json" = "dd3ca9d23784e34d8dbe0b9d0d500f9b3b1fdf621375287148e645348075a171"
    "oracle/FW-07.json" = "f9ecbe27a4320fc6a8f81828a02cd163f43559b1ea19cebbf3187cd7ec4e8f30"
    "oracle/FW-08.json" = "5a00c93a2000fcddc1240335f1f6bf9eaa5c5a17e16f699dcd3f740ff022f812"
    "oracle/FW-10.json" = "132f476e7dc093ac8a1d04037fc97967235c47a67c3c37254a3d1097d96cb0ce"
    "oracle/FW-14.json" = "f1c6f7e74fa854d5e280479784cafe4eaa9249fe9b86e8e158ba7fa1c8ccd0b3"
    "oracle/FW-15.json" = "66597fe66331a305c217eec5e83a6d5a585f20b12d98fdee021e5340bfa10c2d"
    "oracle/FW-16.json" = "aa14e89d47297fb101562acfa04998c2fcba9f9ac9f650b61a0ab31fb6fcc46d"
    "oracle/FW-18.json" = "da0b2ef699a79d6f2a9746e7f27be31ff6457b909942dbc9f83021e1d50253ca"
    "verification/README.md" = "7fa7b74201782ccf4337bb0bc0e18ec6b37a697b180862a74baf7c9847220774"
    "verification/check_split.py" = "7a85129e20da6e5d52b07bf35ee244fd68305f9b122c9cb6478b07b1c37d1c8e"
    "verification/counting.py" = "bf2e80b286bf89448620b4c1d92a54c1ea35c3692171ebb5dd16652f330aec2a"
    "verification/coverage.py" = "d3c1063a5f89503c02a216517c5a958d7a5aa772f8d06e49f640b6405d1cf5c1"
    "verification/examples/build_boundary_prototypes.py" = "27362d1e7c61330f65de0f60ef80030b4dd8758a8acabf93140f249b6e1875f0"
    "verification/rules.py" = "f8b0bb9299d68ac15eebbab06acf1971e0c0b0224ba04874b125e46c771a784e"
    "verification/test_lineage_split.py" = "a5ab7544a3bcfba9c80bef10238fa03713b07b9cf46d2845bd88db3ea3dedbb8"
    "verification/test_public_verification.py" = "5ef960a5004a3228aa73356ae67746737d14970f048ff02bc81e8d516f11c6f4"
    "verification/test_public_verification_consistency.py" = "8100627a20dd4d5b51724209069bf5b5f3cdb719e55536fe99938aa2ebde83a8"
    "verification/test_rule_boundaries.py" = "d28371efd0f11c968c2948a701a4f4503a2756adc7a2e8d3cf47445733d1749e"
    "verification/verify.py" = "80186f64df83231d0cacd9a39dff117f76ec48438c1953004b7dae2471429f4c"
}
function Invoke-CheckedGit {
    param([Parameter(ValueFromRemainingArguments=$true)][string[]]$GitArguments)
    $result = @(& git -c credential.helper= -c core.askPass= -c credential.interactive=false -c http.extraHeader= -c core.longpaths=true -c core.quotePath=false -c http.version=HTTP/1.1 @GitArguments)
    if ($LASTEXITCODE -ne 0) { throw "git failed ($LASTEXITCODE): $($GitArguments[0])" }
    return $result
}
function Get-PinnedSubmoduleState {
    param([string]$Repository, [string]$Prefix = '')
    foreach ($line in (Invoke-CheckedGit -C $Repository ls-tree -r --full-tree HEAD)) {
        if ($line -notmatch '^160000 commit ([0-9a-f]{40,64})\t(.+)$') { continue }
        $expected = $Matches[1]
        $relative = $Matches[2]
        if ($relative.StartsWith('/') -or $relative.Contains('\') -or $relative.Contains(':') -or @($relative.Split('/') | Where-Object { $_ -in @('..','.','') }).Count) {
            throw 'Unsafe submodule path'
        }
        $child = Join-Path $Repository $relative
        $display = $Prefix + $relative
        $initialized = Test-Path -LiteralPath (Join-Path $child '.git')
        $actual = $null
        $clean = $false
        if ($initialized) {
            # A download interrupted before checkout may already have a .git marker.
            $headResult = @(& git -c core.longpaths=true -C $child rev-parse --verify HEAD 2>$null)
            if ($LASTEXITCODE -eq 0 -and $headResult.Count -eq 1) {
                $actual = $headResult[0].Trim()
                $clean = @(Invoke-CheckedGit -C $child status --porcelain).Count -eq 0
            } else { $initialized = $false }
        }
        [pscustomobject]@{ path=$display; expected_commit=$expected; actual_commit=$actual; initialized=$initialized; exact_commit=($actual -eq $expected); clean=$clean }
        if ($initialized -and $actual -eq $expected) {
            Get-PinnedSubmoduleState -Repository $child -Prefix ($display + '/')
        }
    }
}
function Restore-PinnedSubmodules {
    param([string]$Repository, [string]$RepositoryUrl)
    # HTTPS only, pinned gitlink checkout; never --remote or an arbitrary update command.
    # Only dependency history may be shallow; exact gitlinks, not branch tips, remain required.
    Invoke-CheckedGit -c protocol.allow=never -c protocol.https.allow=always -c protocol.file.allow=never -c "remote.origin.url=$RepositoryUrl" -C $Repository submodule update --init --recursive --checkout --depth 1 --jobs 4 | Out-Null
    $states = @(Get-PinnedSubmoduleState -Repository $Repository)
    foreach ($state in $states) {
        if (-not $state.initialized -or -not $state.exact_commit -or -not $state.clean) { throw "Submodule not ready: $($state.path)" }
        $child = Join-Path $Repository $state.path
        foreach ($remote in @(Invoke-CheckedGit -C $child remote)) {
            Invoke-CheckedGit -C $child remote remove $remote | Out-Null
        }
        if (@(Invoke-CheckedGit -C $child remote).Count -ne 0) { throw "Submodule remote remains: $($state.path)" }
    }
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
    if (-not $Resume -and @(Get-ChildItem -LiteralPath $destinationPath -Force).Count -ne 0) { throw 'Destination must be empty; use -Resume to revalidate completed repositories after interruption.' }
} else { New-Item -ItemType Directory -Path $destinationPath | Out-Null }
$savedPrompt = $env:GIT_TERMINAL_PROMPT
$env:GIT_TERMINAL_PROMPT = '0'
$restoreResults = [System.Collections.Generic.List[object]]::new()
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
        if (Test-Path -LiteralPath $repoPath) {
            if (-not $Resume -or -not (Test-Path -LiteralPath (Join-Path $repoPath '.git') -PathType Container)) {
                throw "Existing destination is not a completed repository: $($entry.id)"
            }
            # Do not modify existing repositories. The checks below must all pass.
        } else {
            Invoke-CheckedGit clone --quiet --no-checkout $entry.delivery.repository_url $repoPath | Out-Null
            Invoke-CheckedGit -C $repoPath fetch --quiet --tags origin | Out-Null
            foreach ($property in $refProperties) {
                if ($property.Name.StartsWith('refs/heads/')) {
                    Invoke-CheckedGit -C $repoPath update-ref $property.Name ([string]$property.Value) | Out-Null
                }
            }
            Invoke-CheckedGit -C $repoPath checkout --quiet $entry.default_branch | Out-Null
            Invoke-CheckedGit -C $repoPath remote remove origin | Out-Null
        }
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
        if (@(Invoke-CheckedGit -C $repoPath status --porcelain --ignore-submodules=all).Count -ne 0) { throw "Dirty restored main worktree: $($entry.id)" }
        if ((@(Invoke-CheckedGit -C $repoPath rev-parse --is-shallow-repository))[0].Trim() -ne 'false') { throw "Shallow history: $($entry.id)" }
        if (Test-Path -LiteralPath (Join-Path $repoPath '.git/objects/info/alternates')) { throw "External object store: $($entry.id)" }
        if (@(Get-ChildItem -LiteralPath (Join-Path $repoPath '.git/objects/pack') -Filter '*.promisor').Count -ne 0) { throw "Partial clone: $($entry.id)" }
        $submodules = @(Get-PinnedSubmoduleState -Repository $repoPath)
        if ($IncludeSubmodules -and $submodules.Count -gt 0) {
            Restore-PinnedSubmodules -Repository $repoPath -RepositoryUrl $entry.delivery.repository_url
            $submodules = @(Get-PinnedSubmoduleState -Repository $repoPath)
        }
        $missing = @($submodules | Where-Object { -not $_.initialized -or -not $_.exact_commit -or -not $_.clean }).Count
        $restoreResults.Add([pscustomobject]@{
            id=$entry.id; head=$head; source_review_ready=$true; git_submodules_ready=($missing -eq 0);
            inspected_submodule_count=$submodules.Count; missing_or_mismatched_submodules=$missing;
            submodules=$submodules; complete_build_environment='not_verified'; build_executed=$false
        })
        [ordered]@{ schema_version='restore-state-1'; completed_main_repositories=$restoreResults.Count; include_submodules=[bool]$IncludeSubmodules; repositories=@($restoreResults.ToArray()) } |
            ConvertTo-Json -Depth 12 | Set-Content -LiteralPath (Join-Path $destinationPath 'restore-state.json') -Encoding utf8
        Write-Host "PASS $($entry.id) $head refs=$($actual.Count) source-review-ready; git-submodules-ready=$($missing -eq 0)"
    }
} finally { $env:GIT_TERMINAL_PROMPT = $savedPrompt }
Write-Host 'PASS: 18/18 main repositories ready for source review with exact HEADs/refs, clean worktrees and zero remotes; pending 22 not cloned. See restore-state.json for pinned submodules. Full SDK/platform/build readiness is not asserted.'
