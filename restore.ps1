[CmdletBinding()]
# After a network interruption: ./restore.ps1 -Destination <same-directory> -Resume
param([Parameter(Mandatory=$true)][ValidateNotNullOrEmpty()][string]$Destination, [switch]$Resume, [switch]$IncludeSubmodules)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$expectedHashes = [ordered]@{
    ".gitattributes" = "5550472b34249d85a794952825db528251956dd8bfff9dd17589ea767446f588"
    ".gitignore" = "6feaded4e28ea86e001a6751b4e3d960e8b7c31b9616ff9936b79297086e809b"
    "ACTIVE_EIGHTEEN.md" = "f64d70be58fea89e65d152c839f8e47a386f5e5db8c43ec81cda6008ad35881b"
    "delivery-scope.json" = "f27dcdf676900d99202753e7bdc147778a32c4ac859b2b6137eb92fd60af865a"
    "docs/boundary-candidates.json" = "75a473e3ed461e2ab732e8db9dee9fcb2cab5fb16edc91994843efce3272c94f"
    "docs/BOUNDARY_CANDIDATES.md" = "b36c1913545682c23f7dce0c31ca10cd07e9ff8b7909c32d3a437808bc703fdd"
    "docs/COVERAGE.json" = "2abaf3433cb039bcc29fd11ecc40417b8dfb5afbc7b9184d5a500512fe9404b3"
    "docs/COVERAGE.md" = "024c9a7b20f1a00e5dc68c5f3425646f2a49f4374300a724992f3c0e41c46acd"
    "docs/EXECUTION_SPEC.md" = "4f2facff28ae746949c2facc991cd7749f356019709c064219afb12499808dee"
    "docs/REAL_REPOSITORY_GUIDANCE.md" = "862ad8541dccc85dd6c752aeb1c1645f5a4dfc6389c38158985945ef8a1b3051"
    "docs/RULE_FIXES.md" = "2eac51b7ddc3877d9cf309e948af300a089e3ed416ba41a1919818fbb4abc154"
    "docs/VERIFICATION_INPUTS.md" = "edc383c7c90a2f06347be9a2510e147bc523a3f37038f31455f1ddf3fe55bf46"
    "docs/WEB_REVIEW.md" = "cc95ca4ffc5842a72807f82269cd6ab25d9fbcf9422fcbe28e6a2f581498453e"
    "facts/APP-01.json" = "f75075594328ad2f351b4c297de04b4f7c2f0d8db3d3fe28eec40b189f7882bb"
    "facts/APP-02.json" = "5053c2c9898b462fbb03002f078ebcdb2e370d2fe70cd9c0a85065bc98f11d99"
    "facts/APP-03.json" = "ec568b74402a04ecae492d47b528272e55c73fc4033f1661076da0049eb4d4f7"
    "facts/APP-11.json" = "740856d8d80664a7134415218c9d7c1ca074d2d1525f6d6fcfd13b657ffd6f1e"
    "facts/APP-13.json" = "dd57c0f795879a187565403b23ca804ba31ea45e574d0be68944732d6c66b0c5"
    "facts/APP-14.json" = "df88b656eefc27effb5a2ec611f8347b1ad4406c5dab464daa31c90da4479553"
    "facts/APP-15.json" = "3fa77c438245eb72ac70c46bb9069fc1b0cdb5f9c44cbb28da5c3f6574b52bb1"
    "facts/APP-16.json" = "2db6490baf17e806c0379fbbc54b812fe09d3645f9ebcd4cdb2d6a9d7b3123b0"
    "facts/APP-17.json" = "3daf6839a22855a687995cb2a312f02a69f112c53457b9d55c3df24022817017"
    "facts/FW-02.json" = "0c98292aff6b61557af6b34cec7ddd443772bcbf517711188fa080ccd9abb676"
    "facts/FW-03.json" = "3344e3dd71220394e14e49206711bd0f6c497260e4ff456ed6a8fa8baac80bb1"
    "facts/FW-07.json" = "f4362b5e939d3062b16460da0e48d39b930afb1888c10f29bbb68278b97c3a28"
    "facts/FW-08.json" = "61b8d0505871b96652ed602087aba41910e0ae0afe0cae123bf3a8f3c4f2c3ee"
    "facts/FW-10.json" = "f6c03c79dee954052e65e1611d3d6cf16d33789b366d7ca70e04b72136521954"
    "facts/FW-14.json" = "0db7f3f069b95016a0ce0b43c4ad5102fb1d9afa6535f1129ead83b8693ff882"
    "facts/FW-15.json" = "bcb2ebd828e549d8c49b3388d6394ad549d23840c4a28ece8d7fcb9a45bd80d8"
    "facts/FW-16.json" = "34ba511b87ce4d8c96f8defa36312192b58083e001ba0aac49fdd4cf09b6856f"
    "facts/FW-18.json" = "5995843e7677f4a0755f2e0bed9d52833df9a7ee85e73f23d0cfc2b04bfce738"
    "LICENSE" = "950f20ff178debfcf2526200837304a7512f39c022dc1f9105a6e0af62788df0"
    "manifest.json" = "be5284a4aff407a875a121543d1a3697e65d64ee8afd8c6a191ea20e7d0f396b"
    "manifest.md" = "a8130ed19f05673eb00fa8f8e6ede623513fa95c9210c964bd09d9b92f55ad87"
    "NOTICE" = "ff71f002bf010747ebc6a65858605d93e07bdbf19e2514ea0bab67f6e8bb1420"
    "oracle/APP-01.json" = "d7dae977ecbc1b317f929fb2892718a8e75dd89c539db26b08e760ab7f47b0d8"
    "oracle/APP-02.json" = "11ffd6e2e4703b320a7d95744ff9dc4344386f51664a779cdd595fb87e0259f6"
    "oracle/APP-03.json" = "eee2552644f9b3d545869f05d66f6d43ce08f3df7ff7faa028595e242e13492f"
    "oracle/APP-11.json" = "db3b2c9d97ff7795bb8ba24304479459effec384be26520b57dd51da6fdd2bf8"
    "oracle/APP-13.json" = "8de2a200be919a0cd87eca27a68267a25fa4599420a8eb4326ef8b545bd767d1"
    "oracle/APP-14.json" = "3979ed71ca9b421e1d573d0badc10140f14d4d6e848de97203077da0a96f610e"
    "oracle/APP-15.json" = "0ad685393e26e758e63635dcbe51d233e0b29b7c8f886ee0204565b428bc36a5"
    "oracle/APP-16.json" = "0b6088f67507bbc71659626a856a11e43646ddfe6c13fe8f48c79f4d320ae3dd"
    "oracle/APP-17.json" = "f883cfe3b61bc052881f454355626b19c8a94ed161ec10328e1cf854dd52cb69"
    "oracle/FW-02.json" = "501b4dfec02e9f75bcdda7309512320c8720cc90209ae7f39fe834f4be48b333"
    "oracle/FW-03.json" = "bb2adb2cec5b3566ffd76fe0d6472e551441dbe946130e7af46948817d78727c"
    "oracle/FW-07.json" = "5867e3d9524120d39d852f13e699bf921f0da93474537b6881bdeb596e0f7e87"
    "oracle/FW-08.json" = "8dcccec227b5a6bc8143e4e039a4ac2df83a90d219705df9db78d4beea8eb13d"
    "oracle/FW-10.json" = "c44f7d2687ec970fc212fcca80260d90cd2153de7fa384028a50dfd694362b64"
    "oracle/FW-14.json" = "236fe3f70d416f8eb4830630472d5b5e94711237f30d451d606c5b9ea7455cab"
    "oracle/FW-15.json" = "bc927a5561cee5a1fdee3c51a22f9145b969db1251017bec189c56a47180012d"
    "oracle/FW-16.json" = "8b71fdd370388b4e7233bc27f85a9ffb019a36efabdbb2e6236c337dfc24bd40"
    "oracle/FW-18.json" = "9ce4d16ef7f4e61cb8ab26188bb92be0814ca96b876a10b07c98c69884843b65"
    "README.md" = "c0ed973f6c6cd5a8614c8323a82edc05ba930c1b44951d7ab3bb8e38269593df"
    "SCORE_RULES.md" = "fc488cf70619a1f72e7e9ca808c228a0a45e0a9dd8cda5a540438cb0602212d4"
    "SCORECARD.csv" = "d3e52f7445f3ca0a454f9c705a270603544da594746c0af6286d2894a20e227e"
    "SCORECARD.md" = "9f255de781c04f95c865b7da528929e94b595f2d4ea377012d035cc6da04feeb"
    "STANDARD_SCORES.json" = "c120b223f43d3f8919446bb7f5d70ef78177a72f77d982905a3c56576f0589eb"
    "verification/counting.py" = "15af0d94e9af89c15fdc6531baaf764fae62d44d0879bce51050e1430aab2ba7"
    "verification/coverage.py" = "d3c1063a5f89503c02a216517c5a958d7a5aa772f8d06e49f640b6405d1cf5c1"
    "verification/examples/build_boundary_prototypes.py" = "27362d1e7c61330f65de0f60ef80030b4dd8758a8acabf93140f249b6e1875f0"
    "verification/README.md" = "1685f4e2fe7a19d3065a4d488fed91572c867d4ef3386a0111dfaf11f12adfa1"
    "verification/rules.py" = "f8b0bb9299d68ac15eebbab06acf1971e0c0b0224ba04874b125e46c771a784e"
    "verification/test_rule_boundaries.py" = "d28371efd0f11c968c2948a701a4f4503a2756adc7a2e8d3cf47445733d1749e"
    "verification/verify.py" = "f673467297a008ec6200d7387811d87e50827618463174528aa417fa4d12b0e2"
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
