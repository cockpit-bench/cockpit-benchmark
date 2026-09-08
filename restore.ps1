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
    "README.md" = "3d0612c7c64dd5c29e60bda422f3b1b66afd3366035e0bee109734570730c518"
    "SCORECARD.csv" = "4fffd52e4510c0187c9a304482ae8a5e394b4ee902cbb1912d47b2f69a87e1a8"
    "SCORECARD.md" = "c499db47a924e9c7f18f9fe640d5145915b034e9bd91ff326b57a29059995c7a"
    "SCORE_RULES.md" = "fc488cf70619a1f72e7e9ca808c228a0a45e0a9dd8cda5a540438cb0602212d4"
    "STANDARD_SCORES.json" = "601195cce7bd71476b854011f0782bf54a391cdb1dab8cad79c026c60e691d81"
    "delivery-scope.json" = "ebd96cf4cea5c3db8637b7f3dc001e33f0da54d922fda12eff6c6aa42c895d71"
    "docs/BOUNDARY_CANDIDATES.md" = "833cb1786bdba58e3586d92805c4a7f0494d5d846002b8e1ce7a6f36ddbdc265"
    "docs/BOUNDARY_REGRESSION.md" = "4895a639ed08bc349888b7a5394e1fc7a03aa943a7a8dfb73021dd0e77c93f2c"
    "docs/COVERAGE.json" = "56cd1d3b4a7268d2e043726e6f7ceec8cb79613de90a9fa3e563ef980e47c119"
    "docs/COVERAGE.md" = "756825539e17662ae513c35818bba30a82765160a9f8c18d67595c74875342b7"
    "docs/DISCRIMINATION_FIXES.md" = "8b2e528e8ab652140344513c690a7f15100b08abcfd34e31363e92ab40048cc1"
    "docs/EVIDENCE_AVAILABILITY.md" = "c0f9d40b2cf3ab8f5ddc5d3923cec2d004b3c8faec424067a01b28808b96e978"
    "docs/EVIDENCE_PROTOCOL.md" = "d16e11265a3af1a3fff29469121fb161cdaf7f93258f5010ea2d9bd66e7c526c"
    "docs/EXECUTION_SPEC.md" = "cc65b63cc366f8f614f26e9e4d77e60a794d8dc40d4a5c525e91c3026888cef0"
    "docs/INTEGRATION_EXECUTION.md" = "2b5b369751f52ee224d040fb2845df0451c31b6d1ef5f1c4269a89233f818e9d"
    "docs/REAL_REPOSITORY_GUIDANCE.md" = "862ad8541dccc85dd6c752aeb1c1645f5a4dfc6389c38158985945ef8a1b3051"
    "docs/REVIEW_FIXES.md" = "601899e42f1da145fb60929efffdc4e70c0a9d1205a9cf9aac99a9b7dd535cb2"
    "docs/RULE_FIXES.md" = "2eac51b7ddc3877d9cf309e948af300a089e3ed416ba41a1919818fbb4abc154"
    "docs/VERIFICATION_INPUTS.md" = "7b2d9fd079454bf75acf3cbc09ce8c39978a4da5951cf54da6c5bdd6cba0e0bd"
    "docs/WEB_REVIEW.md" = "9e8caea8b6e3305565a9824113f356d66f8f2a667e2648451e11daaa68eaad5d"
    "docs/boundary-candidates.json" = "373a07b7fe67e5f76e023b088399f3dddb83c4e701aeae1661b31e40121ae228"
    "docs/boundary-reference.json" = "6c66f835e07172653a03e38e09e3b91c95d44d34e2b5f2e693cd2b73ffbfa3fc"
    "docs/evaluation-context.json" = "e36c0ce3fd1d00e830301aa1e86cd0760ccce00ce31034945c0ce174f6be00f3"
    "docs/evidence-availability.json" = "12231e76f34b7751eb64bec86460860fdb5590ac2677184deae403f98ab1eb31"
    "facts/APP-01.json" = "58dfb31e45adfdd81e9497e392ce16622a4722b3eb118b3fcd084a66123649a3"
    "facts/APP-02.json" = "50066389def8928f8294aca07a0540db41c7b81aaab2c508ea8663f468d258f9"
    "facts/APP-03.json" = "ab9fabdb04d2718dda49bce21a1609cc5e0032c41d77cbce954c6e7a484156f8"
    "facts/APP-11.json" = "37479c59e09d1d4a112c5c02ac7c7599539e509c2384adb7df56c01b48a2d5c7"
    "facts/APP-13.json" = "c8ff340ae8790b1a8eb8df006285c6f86fe4b7713685654df508ac9dd52b97a0"
    "facts/APP-14.json" = "b833d8de72e3a5e5905bd52336d6c098ee9b72f1fb190c96891d138fafeb6b41"
    "facts/APP-15.json" = "43ea58e7f66f0103e7cb4ae92f9da64bff339be5a8e0cfa22010b05383a131a5"
    "facts/APP-16.json" = "77881ed5445f36c70dbee3c75a7b012a4fb0ec8e5bd75f0c4a62dd30f95a34e9"
    "facts/APP-17.json" = "f95c08653b5a45e00b469c341e424fada0c52b13ef71474652d2a273db3d1ad7"
    "facts/FW-02.json" = "ce486eddec5e668186050acb9aa98a9461acbfbb719d50c51461693ed8e589c1"
    "facts/FW-03.json" = "fc6ecc96f715dc8783ffc8e7d93376f04d57862de1e7c1664764db35d351f702"
    "facts/FW-07.json" = "5268c6f902f092f849a13f5c59851d61fc6b161b9cb048e248a03c31eb42e7fb"
    "facts/FW-08.json" = "3b3b171f247c1b4165a66ea670a59018256e04ca4fcb763e85ec555666452255"
    "facts/FW-10.json" = "fd113be19d2710fe93cf7125140018e16e07a0690cec38c24e098d3d53cc7d03"
    "facts/FW-14.json" = "f3f3fb799de4f65542756523e06b7c7232f5071544251135a67906471ebfc3b9"
    "facts/FW-15.json" = "30d02f53b0bbf49c19ed4c7a83ccf865e5c7440519b7cc9604db0c70f35960cd"
    "facts/FW-16.json" = "626965e5ae3bfa2aacb12f510a8f940c32811077459cc1f859939ba807f9dc66"
    "facts/FW-18.json" = "40b99b0ab66ba016ad4b9c2f7d82a472ea883c20265a82a58e99fc51da563b81"
    "manifest.json" = "ca00be789c879d78946ac6901a0c849ee4516f96011d7b85f294e38babdb9005"
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
    "verification/README.md" = "75c54094ad017cb5dec575abafad6a3e89bab330188087cf4e1fa78f111d79b0"
    "verification/boundary.py" = "9b9888b7e33b26ef4b65033d982099c413540074408ff81df0f6cbd34a59f384"
    "verification/check_split.py" = "7a85129e20da6e5d52b07bf35ee244fd68305f9b122c9cb6478b07b1c37d1c8e"
    "verification/counting.py" = "01535dfe4097e289681ec0ab9f8d774cdfe11811c4d249c0050cbbee686ab9da"
    "verification/coverage.py" = "74876337d45bea4260ed60c94a00c6105464c05adff3e0df951d0d02a35a9392"
    "verification/evaluation_profile.py" = "8ab808d05a4106d913d127ff2e9f67210ff3d6d53acacd18f6aa33cc233b7ad5"
    "verification/examples/build_boundary_prototypes.py" = "5c802e00142f1815b67271210f51b3dc824e3598e84027667b64f02a81794394"
    "verification/rules.py" = "8dbfc0622da69475e4f0b325009bbdc2e1865d3f99979235c6eb3e26d03e4266"
    "verification/test_boundary_regression.py" = "a4237e27c9f627f2a5f807fe02e97149903e9db1c17c27a5992c84889cde83a2"
    "verification/test_cpp_counting.py" = "79c6f3d34c6a8d20904f3f1747b440e56f728cf54820d93b9df06680000370a5"
    "verification/test_evaluation_profile.py" = "b999aa7d419cf5e4738bb91de00ae14bb2d42f349f98f89c498810b2dd24a3b3"
    "verification/test_integration_execution.py" = "119e8df0701e4a110d4d13419ca864c90002deb238f843442aa1872f9257e492"
    "verification/test_lineage_split.py" = "a5ab7544a3bcfba9c80bef10238fa03713b07b9cf46d2845bd88db3ea3dedbb8"
    "verification/test_public_verification.py" = "5ef960a5004a3228aa73356ae67746737d14970f048ff02bc81e8d516f11c6f4"
    "verification/test_public_verification_consistency.py" = "8100627a20dd4d5b51724209069bf5b5f3cdb719e55536fe99938aa2ebde83a8"
    "verification/test_rule_boundaries.py" = "9d61d0c5ce9a5fc20e8e38c63c8998fe136084b8d72855383792814484b12517"
    "verification/verify.py" = "4939942f3c13dfd2ef93ec8d4d4ecd85930818628fd0694c3ebb7d240486b559"
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
