[CmdletBinding()]
# After a network interruption: ./restore.ps1 -Destination <same-directory> -Resume
param([Parameter(Mandatory=$true)][ValidateNotNullOrEmpty()][string]$Destination, [switch]$Resume, [switch]$IncludeSubmodules)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$expectedHashes = [ordered]@{
    ".gitattributes" = "5550472b34249d85a794952825db528251956dd8bfff9dd17589ea767446f588"
    ".gitignore" = "6feaded4e28ea86e001a6751b4e3d960e8b7c31b9616ff9936b79297086e809b"
    "ACTIVE_EIGHTEEN.md" = "f64d70be58fea89e65d152c839f8e47a386f5e5db8c43ec81cda6008ad35881b"
    "delivery-scope.json" = "1acba621a5aab6df38fe44017edbf70a80c242c47559500169d19eef8ab3cb9d"
    "docs/COVERAGE.json" = "f806cced59928c322e5539c05fdfb01180d8364f59100f5d40efca1b15f57e2d"
    "docs/COVERAGE.md" = "eb36446f6564ce272ae1f8cd8194244a785820cc07af3b3bc5a46e9a9785ca8f"
    "docs/EXECUTION_SPEC.md" = "4f2facff28ae746949c2facc991cd7749f356019709c064219afb12499808dee"
    "docs/REAL_REPOSITORY_GUIDANCE.md" = "862ad8541dccc85dd6c752aeb1c1645f5a4dfc6389c38158985945ef8a1b3051"
    "docs/VERIFICATION_INPUTS.md" = "0396089a2fdb33ff3a14bdd50b41db8a98592414785faff8f4d094152b52e01c"
    "docs/WEB_REVIEW.md" = "3d6f62374a48b792febf70cc0295417e14517bd97ed42ce05ac27cb27bab952e"
    "facts/APP-01.json" = "5c6531ef3e1f62f078eeee7e35c10872abfb3c5c43568ba524e142a46bb1ef4f"
    "facts/APP-02.json" = "fcfdece20ebd666619c101fcbd66032fed767ef1d6d506e9bdc8719b7f55466f"
    "facts/APP-03.json" = "afea47fb4507dea64d2dfb165b211b694667d158d12c9f926e9c359e873479e7"
    "facts/APP-11.json" = "057a897d8ef5322771faa36001524342d5bf1802ac67b3854abd29dd64d1ba01"
    "facts/APP-13.json" = "54f7865761d0932e5b2245585087c75c41d22126e030e03557abaca5fbcc19b3"
    "facts/APP-14.json" = "22f524b273236e4b90611806607b90d68f04f1fa69ab26df85de2ee498f6520c"
    "facts/APP-15.json" = "c75f8174a7dffb5b58ca484aff4dc3d03718054f6e774ac93239c4f6cbefd8db"
    "facts/APP-16.json" = "60ef78f6a6559e5dfdacf16c01f6a5fbeb4e195bac78db240340e64a34b27dd9"
    "facts/APP-17.json" = "81f55c74e912b0e51cdae9e06783e765bb7997f623ebaa85028c692df1c09da7"
    "facts/FW-02.json" = "afaf8e60661b83203cf0ab765b9847f06a3dea5bb6057a781058187e0d1a80e7"
    "facts/FW-03.json" = "e0a1ddeb507431eb0ce8dab8e0a34c53be5d2bc5c5fe7e2530216d5dd1844d48"
    "facts/FW-07.json" = "7d54e2ff3fb73099ae8f8c93531fde95a73bd8cb02084a1b30add8517b0671a6"
    "facts/FW-08.json" = "c9b4fc088354fa34dd60712f8edb7e293665bcd6502dd0bf54c28ae587608594"
    "facts/FW-10.json" = "f1741fdf2d59b4655ac6bde372f8024af2d30af99e614e0f4083340938d45343"
    "facts/FW-14.json" = "7f515226438eb1bcba3fbe173fc2ab1c1d8c02e4c9faf3bbc33ce00a0d3b4877"
    "facts/FW-15.json" = "731cfff1cb00675aed7e262243e765608609b0267e9649b8b73e63486ed43a5f"
    "facts/FW-16.json" = "576067ef89dda60fc6409f1154051d37d1d3ff7fc19d9d856c07414aa965f6f0"
    "facts/FW-18.json" = "2276cf6de615670f8f88dde8f9289c4e07e87601c2b7e35350da9b75a3373fcc"
    "LICENSE" = "950f20ff178debfcf2526200837304a7512f39c022dc1f9105a6e0af62788df0"
    "manifest.json" = "6383e54cf99adb01e757bd385a5c560eab3084e013ef115e18ffad01ead8abf0"
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
    "oracle/FW-07.json" = "d1b23143b4a8a238bf3758e42577b0aa30ed2643de05beebf9a8ff17db2d75ae"
    "oracle/FW-08.json" = "8dcccec227b5a6bc8143e4e039a4ac2df83a90d219705df9db78d4beea8eb13d"
    "oracle/FW-10.json" = "c44f7d2687ec970fc212fcca80260d90cd2153de7fa384028a50dfd694362b64"
    "oracle/FW-14.json" = "236fe3f70d416f8eb4830630472d5b5e94711237f30d451d606c5b9ea7455cab"
    "oracle/FW-15.json" = "bc927a5561cee5a1fdee3c51a22f9145b969db1251017bec189c56a47180012d"
    "oracle/FW-16.json" = "8b71fdd370388b4e7233bc27f85a9ffb019a36efabdbb2e6236c337dfc24bd40"
    "oracle/FW-18.json" = "9ce4d16ef7f4e61cb8ab26188bb92be0814ca96b876a10b07c98c69884843b65"
    "README.md" = "247043cf4f4d8cdbd2df972967d2ca0bde1c3e4e76573fb614698cc56893977e"
    "SCORE_RULES.md" = "fc488cf70619a1f72e7e9ca808c228a0a45e0a9dd8cda5a540438cb0602212d4"
    "SCORECARD.csv" = "d3e52f7445f3ca0a454f9c705a270603544da594746c0af6286d2894a20e227e"
    "SCORECARD.md" = "f0b5adb8b64c9267ae2b0f16bf57fc413841a8e40c2f25378371995ccdfb1092"
    "STANDARD_SCORES.json" = "64eee92226fb49ca9cd07e72a63495b29b60390d822e780ae312e1dac7b52d67"
    "verification/counting.py" = "15af0d94e9af89c15fdc6531baaf764fae62d44d0879bce51050e1430aab2ba7"
    "verification/coverage.py" = "f9fb3277eaa516de345cb85068eb98eb3c83b49951603146ddcde1c71927142f"
    "verification/README.md" = "47cc593f435d5a9afaef983df52b4ad0a9f171ea2020f8f6c03178f47aafafed"
    "verification/rules.py" = "0c5563b70359eff64a02cec1b0e4262d02003fb976ed3e6110ca07278708a95a"
    "verification/verify.py" = "fe064996002e81340f0b918a44bbc3d21941db3302bef571efa54881be4669d5"
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
