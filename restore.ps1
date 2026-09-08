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
    "README.md" = "190a9d024b3970a1a57999474c4d00da4f66a088f5d0c47ced08bce30e1beb59"
    "SCORECARD.csv" = "6770ff2c2d6f889a9f5aa0f04756b9eec5ac468c0ebc4546cf7d45fb1eded242"
    "SCORECARD.md" = "22af3d29dbce400819e4748904804da73de92a658976dbef970e4f81634a8edd"
    "SCORE_RULES.md" = "bcbbe577dd3b62862d48efb18bfcd17a86d749631ac6c282b73a1f2215b5689a"
    "STANDARD_SCORES.json" = "e9cd19b528cfdf06a4a6f095de8910c3ff3a0a6bf3a028656ba9fd844293c807"
    "delivery-scope.json" = "81154b9ffac9871ee948e7eb50ea19e0b18dce2ff33e15abd4fbb00dd48c964f"
    "docs/API_GOVERNANCE.md" = "e5532fe6eb54ad3c39bfda450b0900ef6fbad51320fee428c5c42a169f8db37d"
    "docs/BOUNDARY_CANDIDATES.md" = "833cb1786bdba58e3586d92805c4a7f0494d5d846002b8e1ce7a6f36ddbdc265"
    "docs/BOUNDARY_REGRESSION.md" = "4895a639ed08bc349888b7a5394e1fc7a03aa943a7a8dfb73021dd0e77c93f2c"
    "docs/COVERAGE.json" = "1a8f00b0283169a4e24b5f814146c8bbab247e3df04661a24bd9176369138a18"
    "docs/COVERAGE.md" = "2f4cdc1d1a37cc7cf094a1f06a2d154d097d81ee8a48ee949c6eb4942bed0f84"
    "docs/DISCRIMINATION_FIXES.md" = "8b2e528e8ab652140344513c690a7f15100b08abcfd34e31363e92ab40048cc1"
    "docs/EVIDENCE_AVAILABILITY.md" = "436e76d41513901d7801827e84c63f88c792828e0bd6085fcd85ca8e3e6d06f4"
    "docs/EVIDENCE_PROTOCOL.md" = "d16e11265a3af1a3fff29469121fb161cdaf7f93258f5010ea2d9bd66e7c526c"
    "docs/EXECUTION_SPEC.md" = "ce9211163bab73116efdeed7c2913517d11c8f02e0fbea5c6f0c1942d8d0f0a0"
    "docs/INTEGRATION_EXECUTION.md" = "2b5b369751f52ee224d040fb2845df0451c31b6d1ef5f1c4269a89233f818e9d"
    "docs/REAL_REPOSITORY_GUIDANCE.md" = "862ad8541dccc85dd6c752aeb1c1645f5a4dfc6389c38158985945ef8a1b3051"
    "docs/REVIEW_FIXES.md" = "601899e42f1da145fb60929efffdc4e70c0a9d1205a9cf9aac99a9b7dd535cb2"
    "docs/RULE_FIXES.md" = "2eac51b7ddc3877d9cf309e948af300a089e3ed416ba41a1919818fbb4abc154"
    "docs/VERIFICATION_INPUTS.md" = "c45759c030f664282452c2df9a9388c0e9a6a99543a88563d37e0c6cbe9dca5b"
    "docs/WEB_REVIEW.md" = "d6f07e22a0bf46497276d77c04465727db9e5b8fa481e35be9aa06aaf12e5e2c"
    "docs/boundary-candidates.json" = "373a07b7fe67e5f76e023b088399f3dddb83c4e701aeae1661b31e40121ae228"
    "docs/boundary-reference.json" = "599559ca960174566fc54995c44f268077008a1b43f1773b78f589c69ff99947"
    "docs/evaluation-context.json" = "311226166483ec7ce279e7ef990085e361b52298e993202318e62ecf947d767c"
    "docs/evidence-availability.json" = "c210767480ac7ef134fbdf965e2b23a27108019bd86b3adc8fec17b8317bed6c"
    "facts/APP-01.json" = "e15368ef1550afcb4d7769b0fff71af47ed6cffde0f018ca47489dab7e904068"
    "facts/APP-02.json" = "9ec9e7693df03328dca349b1029958b93330e51cec77f700c0882751dd7193f7"
    "facts/APP-03.json" = "3ad910b27da35f71a4330d71de368ca0a74825ee9e02a208da1f265576d38213"
    "facts/APP-11.json" = "3338cb0ee5828f900a0a2e78e81b00b07179dabf655fcae7a67d3e3bf4b08945"
    "facts/APP-13.json" = "4c857c59df2d7a1ed503a6d11cd0deaf739c22cfe0d22a480cb867f222b3f26c"
    "facts/APP-14.json" = "e79e524c97dcd288909726dd9206d7ba1472709eedb19ee0f71712b67a29efd8"
    "facts/APP-15.json" = "cbe3da78d789e9e20052196b0f781bc1a3222fd885958a52464d0e70429877c8"
    "facts/APP-16.json" = "1a3bb3a2220d3ded32254926e8d5bbb748eb147cf1efa0169bcd1a7bc42ab37f"
    "facts/APP-17.json" = "b70c1617ca6e4acbf9a2c5801a9fedf4d0cf8b2d0baf46c3a076c400c483db08"
    "facts/FW-02.json" = "360c6c77f410403ebce9ce55570bc3d578543851477c2c88a90a3e64a45a2108"
    "facts/FW-03.json" = "437422c1d03be74b9d413d6ec68cca2f2c51b2b2f5102d4cda7730915f85ec9f"
    "facts/FW-07.json" = "3c31b42e27fecda6bd56a9d3cba740f765d0d1af0ba9a9a46cf68930aa16a76c"
    "facts/FW-08.json" = "44157f635487f5f6d96cfc6a640fe27db51250028329a9a98c3c2221cd234952"
    "facts/FW-10.json" = "732d8ebe4870ff9d3cc0a0d823d2495a149537cb00f3759d754877e2047cacd6"
    "facts/FW-14.json" = "6bb2d6a38cb9ba6b085c942883af1c12e6b7e95158b818d7d1dd0d5581733b4e"
    "facts/FW-15.json" = "5d3b306378c759ebb1c0c401a910546cfb83389ff0cbdc75c206160a53af0dfb"
    "facts/FW-16.json" = "2cf1126c7375603e33d05ddf0dbe0fa7b912a25aef4e43f1cc083222c613be23"
    "facts/FW-18.json" = "70fda85503b4038bac4b9326e110119c94446a26beeb027afa1761e0fd92b975"
    "manifest.json" = "35ec4573fa8706e8c71bec1b56eb57af37573d55db6998d5ad2c62bec804c68d"
    "manifest.md" = "a8130ed19f05673eb00fa8f8e6ede623513fa95c9210c964bd09d9b92f55ad87"
    "oracle/APP-01.json" = "4e514360640531bde203a04ea69a3cb1c9819b90317b69096037e851564206e6"
    "oracle/APP-02.json" = "b78c10ea86d0dc6a6a18ca43c40744166c6b044b14e254376e02bc87e085f3bd"
    "oracle/APP-03.json" = "b15a6c290ff081018df6f4b2e211f244776380518ff8dd30b3ae94d44309288f"
    "oracle/APP-11.json" = "28fdc231069e7ae4e1bd5a25b499e26ddf4994da08e8f4624b5b49035fc23fe4"
    "oracle/APP-13.json" = "bf82ce1197103908e8ec120b603da8f50bc5bd9a6100e0e45f3039a01a123465"
    "oracle/APP-14.json" = "938db15c8e8dbafcd16cf15baeb018b1191e49d2c56ecebc394345d0249731f7"
    "oracle/APP-15.json" = "64f70413ea3ff5f64acd1fb59afba421ab070b1840b6a33fbbbb127a3b08f0f8"
    "oracle/APP-16.json" = "72b94f4e3561679dc7436c75a6020adba034f456d9aefe0be37f843716ca5e49"
    "oracle/APP-17.json" = "fbaea606294318f0dc4635b0db720583c9316ea1ba5b39713e354d05609aaf50"
    "oracle/FW-02.json" = "6a21eb81786ecbc33b94d86cd848890d40857caa7bf2c370f95ce98ef53085d0"
    "oracle/FW-03.json" = "1bfa4104762767f48e15636d18ffc86be622acab1ca40b00e67d8127e0fe320a"
    "oracle/FW-07.json" = "ee4a9e9269a9f36e243f8312d612ee2e9dcf28105e94b0b46c3fb1808e7a74ef"
    "oracle/FW-08.json" = "8aa36216aa410db0f55381c3bf6f704f36dc67d412dbc20b8dbf5603074d9c6c"
    "oracle/FW-10.json" = "39c9579d7729ddc0ea8f63eee801877f45c5bebbf2577ccc70db1d04cd348bd5"
    "oracle/FW-14.json" = "15337a0c80034aa5a5e72829727ee8b6d62cfa4de31eb1d268657abe2197885c"
    "oracle/FW-15.json" = "99c17a8b219f8d0d642e8f4d2097f74f66c78d43aaa37ffa281e95fa4a7d0972"
    "oracle/FW-16.json" = "fce44396270a4ffd68e8b9179be151df06405eb978af1c52ab5d72c607d39477"
    "oracle/FW-18.json" = "2ee67a53fa306f11fac2938a2a45d0518716b32a04016e016d5ff8b31c58135a"
    "verification/README.md" = "40ac940090266ff289234accc8ef180c1623a4bff395355f6ad7aa1c490439e1"
    "verification/boundary.py" = "9b9888b7e33b26ef4b65033d982099c413540074408ff81df0f6cbd34a59f384"
    "verification/check_split.py" = "7a85129e20da6e5d52b07bf35ee244fd68305f9b122c9cb6478b07b1c37d1c8e"
    "verification/counting.py" = "01535dfe4097e289681ec0ab9f8d774cdfe11811c4d249c0050cbbee686ab9da"
    "verification/coverage.py" = "74876337d45bea4260ed60c94a00c6105464c05adff3e0df951d0d02a35a9392"
    "verification/evaluation_profile.py" = "8ab808d05a4106d913d127ff2e9f67210ff3d6d53acacd18f6aa33cc233b7ad5"
    "verification/examples/build_boundary_prototypes.py" = "5c802e00142f1815b67271210f51b3dc824e3598e84027667b64f02a81794394"
    "verification/rules.py" = "f0936ed0d1bb7400f4f44985abdb23c41330e5593fe7ea08643dfd652b334c4d"
    "verification/test_api_governance.py" = "b6dff09ba8cd6f0074e5faa9664f97604b78e8b8de90f1a2729288fa63f9c315"
    "verification/test_boundary_regression.py" = "a4237e27c9f627f2a5f807fe02e97149903e9db1c17c27a5992c84889cde83a2"
    "verification/test_cpp_counting.py" = "79c6f3d34c6a8d20904f3f1747b440e56f728cf54820d93b9df06680000370a5"
    "verification/test_evaluation_profile.py" = "b999aa7d419cf5e4738bb91de00ae14bb2d42f349f98f89c498810b2dd24a3b3"
    "verification/test_integration_execution.py" = "119e8df0701e4a110d4d13419ca864c90002deb238f843442aa1872f9257e492"
    "verification/test_lineage_split.py" = "a5ab7544a3bcfba9c80bef10238fa03713b07b9cf46d2845bd88db3ea3dedbb8"
    "verification/test_public_verification.py" = "5ef960a5004a3228aa73356ae67746737d14970f048ff02bc81e8d516f11c6f4"
    "verification/test_public_verification_consistency.py" = "8100627a20dd4d5b51724209069bf5b5f3cdb719e55536fe99938aa2ebde83a8"
    "verification/test_rule_boundaries.py" = "9d61d0c5ce9a5fc20e8e38c63c8998fe136084b8d72855383792814484b12517"
    "verification/verify.py" = "ee47327357e008a659750b7bc42a10796973650987a7e9989f1e29092f322d4c"
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
