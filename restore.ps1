[CmdletBinding()]
# After a network interruption: ./restore.ps1 -Destination <same-directory> -Resume
param([Parameter(Mandatory=$true)][ValidateNotNullOrEmpty()][string]$Destination, [switch]$Resume, [switch]$IncludeSubmodules, [ValidateSet("android-validation18","matlab-simulink","all")][string]$Suite = "android-validation18")
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$expectedHashes = [ordered]@{
    ".gitattributes" = "5550472b34249d85a794952825db528251956dd8bfff9dd17589ea767446f588"
    ".gitignore" = "6feaded4e28ea86e001a6751b4e3d960e8b7c31b9616ff9936b79297086e809b"
    "ACTIVE_EIGHTEEN.md" = "f64d70be58fea89e65d152c839f8e47a386f5e5db8c43ec81cda6008ad35881b"
    "LICENSE" = "950f20ff178debfcf2526200837304a7512f39c022dc1f9105a6e0af62788df0"
    "NOTICE" = "ff71f002bf010747ebc6a65858605d93e07bdbf19e2514ea0bab67f6e8bb1420"
    "README.md" = "29bdb546f65e2a227d320509a9f6fdaa8ccfd00d32a935ad7f415a35fa345fc3"
    "SCORECARD.csv" = "80fee7fa8fd14be03e3fbd2034f3048750ddad5a59f730e49d6edeaf3adda52e"
    "SCORECARD.md" = "418cec97647f74b6c7e9a04b018902e196a947411ac8454ed44aacb1c0e58d7c"
    "SCORE_RULES.md" = "bcbbe577dd3b62862d48efb18bfcd17a86d749631ac6c282b73a1f2215b5689a"
    "STANDARD_SCORES.json" = "6ca863e0021abeea946dede4f7f142cfb09864931c5ba9ea732741d5a411a174"
    "delivery-scope.json" = "8a0df42bdc04163a043a399e3ae3de2ac646cbf0315edc9cfe24ea11292b871c"
    "docs/API_GOVERNANCE.md" = "8a2cfb4e20b12d116944d881fd80f37c2edf2cbaccd2222644998d477e256792"
    "docs/BOUNDARY_CANDIDATES.md" = "833cb1786bdba58e3586d92805c4a7f0494d5d846002b8e1ce7a6f36ddbdc265"
    "docs/BOUNDARY_REGRESSION.md" = "4895a639ed08bc349888b7a5394e1fc7a03aa943a7a8dfb73021dd0e77c93f2c"
    "docs/CONTRACT_DECISION.md" = "7c106c46658612cf02a7c701df2acfe2c59e02d0c70cb9bd898cc97e705e7052"
    "docs/COVERAGE.json" = "05ca07ca79a9d8d84b2fecbcb043b0c680208f0ad4a1ce88cc9604036c679a7d"
    "docs/COVERAGE.md" = "11cecd6b8a379e5b3da8547923561a16feb6989681eadb1cb346c17e552b4961"
    "docs/DISCRIMINATION_FIXES.md" = "8b2e528e8ab652140344513c690a7f15100b08abcfd34e31363e92ab40048cc1"
    "docs/EVALUATION_BATCH.md" = "9e2081bfb80811b845fbbbbbbc3c4679d5c4b034b0ee34774ccdbac57254bb65"
    "docs/EVIDENCE_AVAILABILITY.md" = "62bd750696e60b8599f65efb2be9ae00dca6879d6c28238aad8cdda4bddca91a"
    "docs/EVIDENCE_PROTOCOL.md" = "55da0019130fc7c3603bdd67655aaff23c255b0fdd297f624ebb29bfff47f22b"
    "docs/EXECUTION_SPEC.md" = "c7789760897d82e07ce3dba5c385319acc6f9866ad7f6fa9bc945d4bfbcf3095"
    "docs/EXTERNAL_GIT_INPUTS.md" = "0330d0a1eea6a37c0ed2a9ec95613974e9174d813dd97d26330595f819a1a6c9"
    "docs/INTEGRATION_EXECUTION.md" = "2b5b369751f52ee224d040fb2845df0451c31b6d1ef5f1c4269a89233f818e9d"
    "docs/REAL_REPOSITORY_GUIDANCE.md" = "862ad8541dccc85dd6c752aeb1c1645f5a4dfc6389c38158985945ef8a1b3051"
    "docs/REVIEW_FIXES.md" = "601899e42f1da145fb60929efffdc4e70c0a9d1205a9cf9aac99a9b7dd535cb2"
    "docs/REVIEW_FOLLOWUP.md" = "4de94d213b49c6fca8265a9f6f1350a9f4aea8a6759c259bc24a81739addcfb4"
    "docs/RULE_FIXES.md" = "2eac51b7ddc3877d9cf309e948af300a089e3ed416ba41a1919818fbb4abc154"
    "docs/SOLID_CALIBRATION.md" = "c7523cdfc750052f12eb970f0db0b3f7286107727ecc5bf5d31be05e3382ec64"
    "docs/VERIFICATION_INPUTS.md" = "e82c5b5e4d331a65eabf85dbabdf59637a992259111fae331fce4767ee7231e7"
    "docs/WEB_REVIEW.md" = "d6f07e22a0bf46497276d77c04465727db9e5b8fa481e35be9aa06aaf12e5e2c"
    "docs/boundary-candidates.json" = "373a07b7fe67e5f76e023b088399f3dddb83c4e701aeae1661b31e40121ae228"
    "docs/boundary-reference.json" = "599559ca960174566fc54995c44f268077008a1b43f1773b78f589c69ff99947"
    "docs/contract-sensitivity.json" = "6fa28378d96fe470869c569be64951d77ab91920fc21563426d9898099caea55"
    "docs/evaluation-context.json" = "a7b9252e3d5ab9722ac6e3821a3de7eebddd9e4bdaafa4db2bf5558004fc98df"
    "docs/evidence-availability.json" = "acb9fbd7213fb50c17ab7700f8edf657616254e694a3d3f7863aead8208961d8"
    "docs/solid-calibration.json" = "da273627b2b3ff3dcba58ba8131f321121683ef8c429e29ba216126c3879e8ea"
    "facts/APP-01.json" = "29bdfc40e8d9ff1df4b6a4a5d01d46784b3c98099523a254e4760323bb113e50"
    "facts/APP-02.json" = "0cc080be10d7bc9d875346a7c02c5fdb36c4473f3043251d3f40b7bff49b3177"
    "facts/APP-03.json" = "3c0c9336ea961c000234e310aacad9993aedd9b14fcfc31c12c486a8dd44f4b1"
    "facts/APP-11.json" = "0998484e04ce6f94dfbb7bdd558289d30eaacd40fe5420142c9baa91807f0093"
    "facts/APP-13.json" = "3501446ed3cba6bf6bb3b5a7e9421f8c542c1b099c30cb8c2ac91b23be4ceedd"
    "facts/APP-14.json" = "3b88c6184dd5dbb7af6d142bee5d1fba775a3ef11ca62ebd3da0ac8663ebe2ee"
    "facts/APP-15.json" = "bb0853c77cc6447786e33db1a71f5a384d643b62ab7338694036273e22fae8ba"
    "facts/APP-16.json" = "d0711b9e197a319806ed4c96d24150b59807cfc06734a1af8749fac6b9ac3e1f"
    "facts/APP-17.json" = "ab916ed82ae801aa0715f162bb132d8e28f408646fab7d64630cc9b80708bdf9"
    "facts/FW-02.json" = "8c56e32b057f617038d8f89baa4b5ee42c0b7448dbff1b8bbe45b03fd0edfb0d"
    "facts/FW-03.json" = "b994ff486f911a25b819fe93c05b80f700ec8723ede510378ffb18aca37408ca"
    "facts/FW-07.json" = "3c3a34689ac25e71718d4be7bfb106c01b8d0b3beeace48518cf7beeaaa431d9"
    "facts/FW-08.json" = "ad9301ba9d638f75f82dd67457e4fa5c88a2239881a366ffab2131f280268fbd"
    "facts/FW-10.json" = "e09a9486576a65c00f2c4baffa16838b678d97b75bb10837836139013fa8a2c6"
    "facts/FW-14.json" = "3b26b4d27cb9359f2c072289c4164924f1c80ae51fafff61d80bc8d1b59bbe0f"
    "facts/FW-15.json" = "dbeeaefc4bfc076966b32eb75d16daaaab0fa52d6d4d8f521c97d7fef8197637"
    "facts/FW-16.json" = "0fa237b014402abfee32b11c3caace0e7f69ee4ca811e211d54f605437099c66"
    "facts/FW-18.json" = "e59fb1ff76ea89c4232add502a2b74048a060f5c326154e288df9cec2b9cbf05"
    "manifest.json" = "68877d7b0b8638246306833686d373f2dee9df36335e14a34bbfd57295d7578f"
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
    "oracle/FW-02.json" = "9eaa1e1d7ee24c18972e96a6ed1e0845c918c9c8f6ed433b10649c74954fee03"
    "oracle/FW-03.json" = "1bfa4104762767f48e15636d18ffc86be622acab1ca40b00e67d8127e0fe320a"
    "oracle/FW-07.json" = "241338587b386b3b057342bfa9b47efe91d4ddc8676116fce82c3bd2ceeb1f5e"
    "oracle/FW-08.json" = "8aa36216aa410db0f55381c3bf6f704f36dc67d412dbc20b8dbf5603074d9c6c"
    "oracle/FW-10.json" = "2b4c7ac060a4326ef686c964518d2e5048598e92740121e38c1bff3a350d4f87"
    "oracle/FW-14.json" = "15337a0c80034aa5a5e72829727ee8b6d62cfa4de31eb1d268657abe2197885c"
    "oracle/FW-15.json" = "99c17a8b219f8d0d642e8f4d2097f74f66c78d43aaa37ffa281e95fa4a7d0972"
    "oracle/FW-16.json" = "8d3b233a8c40dd8497cbac0aea984202ddcbeb3ae55bd8f0c3c00679b006c0cd"
    "oracle/FW-18.json" = "2ee67a53fa306f11fac2938a2a45d0518716b32a04016e016d5ff8b31c58135a"
    "suites.json" = "3f681e15f1a8ac1dff1995dac9536e1dbc846bd23a9c3c4bf5ac03de26c6696b"
    "suites/matlab-simulink/DATASET_LIMITS.json" = "12b2a775b1c2563b298b620fb422f0ba69b7091f99ef3a02e909b7806b3aad4f"
    "suites/matlab-simulink/DATASET_LIMITS.md" = "f3de5bd55e52d1852b52488ede2b204ad2c124d48de360d22199939bf5e64605"
    "suites/matlab-simulink/EFFECTIVE_CONTRACT.md" = "36f75b2b79416d227c0f0538573774067e6ef4fa096e3272df88bb3439495665"
    "suites/matlab-simulink/EVIDENCE_INDEX.json" = "9f3815129808034b9eb7905bba7fde443b23805cbc4559331066711fead036f6"
    "suites/matlab-simulink/PUBLIC_RESTORE.json" = "d8b62c284e5147e200ef555249d7e855c52d3a1113f43a3848dc55c09690d9b9"
    "suites/matlab-simulink/README.md" = "44607fcc44e5e5204065db8ea8dfac9af4bb6b83af7620b6d8e6cd140b2f695a"
    "suites/matlab-simulink/SCORECARD.csv" = "b1debd47876d2106128b7f7e794293852879cfe6f483fa95d240508a81cd3d04"
    "suites/matlab-simulink/SCORECARD.md" = "fe3497932d3ddcf45eabb4f0b6b265a083bb86bb9c376533445887f96da5647b"
    "suites/matlab-simulink/SCORING_CONTRACT.md" = "5c3783521aae11d8d00c45c81abb9029aa0d863f61a89660bab29b28ae231845"
    "suites/matlab-simulink/SCORING_OVERRIDES.md" = "690436ce76d3d352c6f44394b923b3be2e0c09ed5c62b875904e412aa7fac4c2"
    "suites/matlab-simulink/STANDARD_SCORES.json" = "aed0534cf42f06ed15d9e4ae1863547cc5f9bcc8af9c72081c4dda432e104848"
    "suites/matlab-simulink/VALIDATION_STATUS.json" = "7fc37135fee2963fdac5a126ebe4634404ce1ae543ac1017fb7c2192b4e4a1c0"
    "suites/matlab-simulink/contract-index.json" = "d63e2da4840178571af2ced5ce89f53c42fcf48ddc4c38a37d78aec93ef1ce1f"
    "suites/matlab-simulink/effective-contract-binding.json" = "f7a01c7243cdc9757de850e11bb1748a25a596e6a473ed8f02c96fc40e02386b"
    "suites/matlab-simulink/manifest.json" = "f1695c0a3544071d9319ad4e06e2e0fabf3ce4aacca788dbfff41895754de71a"
    "suites/matlab-simulink/oracle/ML-01.json" = "48159bad543d640c896cf1b4753066629010bb81def7990cf8ba8ee3ad30782d"
    "suites/matlab-simulink/oracle/ML-02.json" = "ace700204b4ac8fac1ebbb4f9437c7313c690b082fa1600948f78e8146d555f5"
    "suites/matlab-simulink/oracle/ML-03.json" = "b956e9115055a01b3d7da4ad50f5e3c96dda25d9107a7e9a7c9b401f28a4927f"
    "suites/matlab-simulink/oracle/ML-04.json" = "73250406ab2bef69b5e93d04d943536e6c300e96dd5d5ebbbc98584c68f684e1"
    "suites/matlab-simulink/oracle/ML-05.json" = "808aa72e174e5a8b21f110ae3c738e8ad1caa3ffe57a183a5982b450caad88d4"
    "suites/matlab-simulink/oracle/ML-06.json" = "d6868c77d1c21bf0acec978ae0a7e3f433ead6711b3cf90c850f8b07954d255d"
    "suites/matlab-simulink/oracle/ML-07.json" = "5d63c8e249e8d1472ea041f9e00f57ef0e31d3d9b17cf4f290c4bef6ab362584"
    "suites/matlab-simulink/oracle/ML-08.json" = "57b0b777b2ffb031add5189c92953dae99fa761c60778331c160ec0b226195b2"
    "suites/matlab-simulink/oracle/ML-09.json" = "c50522bcca822faa4b6ddadb62a0272a7278fb00df2a218ceba42a2c9481e697"
    "verification/README.md" = "6c2d135a31b5e41708d5866e86e51fae63465d26ef3c96a713b6eebb0213b0ff"
    "verification/boundary.py" = "9b9888b7e33b26ef4b65033d982099c413540074408ff81df0f6cbd34a59f384"
    "verification/check_split.py" = "7a85129e20da6e5d52b07bf35ee244fd68305f9b122c9cb6478b07b1c37d1c8e"
    "verification/counting.py" = "01535dfe4097e289681ec0ab9f8d774cdfe11811c4d249c0050cbbee686ab9da"
    "verification/coverage.py" = "74876337d45bea4260ed60c94a00c6105464c05adff3e0df951d0d02a35a9392"
    "verification/effective_contract.py" = "1c25ad2920ad49fca83b968f76036f3df70461a57a5b1520fde9ec3693b3afa5"
    "verification/evaluation_batch.py" = "2b1f826f034fd09032c7c4109a39f98a5da574929fc5e5d1278c91c9a699f5a9"
    "verification/evaluation_profile.py" = "8ab808d05a4106d913d127ff2e9f67210ff3d6d53acacd18f6aa33cc233b7ad5"
    "verification/examples/build_boundary_prototypes.py" = "5c802e00142f1815b67271210f51b3dc824e3598e84027667b64f02a81794394"
    "verification/external_inputs.py" = "54882587f5cad6dd75be0b5b1feca9ac3c4dbe252667bc3b17dffd654b232b5d"
    "verification/matlab_evidence.py" = "f5f1f7749ff08b979a3e433d941db91292006f86a2b2065453af8a2132239630"
    "verification/matlab_properties.py" = "066d12dc74dfaf6ede617a32d6bcc9903f1c371e45198ce4a83a848101802c5f"
    "verification/matlab_recompute.py" = "bcc05daf3b8f8a19fb064926e0cd0d6ba9930fd085427a169103d0516000178f"
    "verification/matlab_validators.py" = "99fabdd335fc4d873f1b269979710dc9faaff316ccdcc2bb2fe0a921dc7c7ef8"
    "verification/rules.py" = "f0936ed0d1bb7400f4f44985abdb23c41330e5593fe7ea08643dfd652b334c4d"
    "verification/suites.py" = "0de336069f39a380772e59708459dd4922f2da33ad1d051a616cd74104d3f93b"
    "verification/suites.schema.json" = "9cbe5d9ba378ec35c4d6f27131158259dd636addc1df0643885da9d4f1dea217"
    "verification/test_api_governance.py" = "b6dff09ba8cd6f0074e5faa9664f97604b78e8b8de90f1a2729288fa63f9c315"
    "verification/test_boundary_regression.py" = "a4237e27c9f627f2a5f807fe02e97149903e9db1c17c27a5992c84889cde83a2"
    "verification/test_cpp_counting.py" = "79c6f3d34c6a8d20904f3f1747b440e56f728cf54820d93b9df06680000370a5"
    "verification/test_effective_contract.py" = "6e4b6dda8be6e2bc13a1d05b12b0e3f7baf16877ef282572464574096f2486c0"
    "verification/test_evaluation_batch.py" = "27251ac369331cb85b3f0e0bed2a3098be9d1abe2002062f72be0fecc95af65e"
    "verification/test_evaluation_profile.py" = "b999aa7d419cf5e4738bb91de00ae14bb2d42f349f98f89c498810b2dd24a3b3"
    "verification/test_external_inputs.py" = "9c364f6e1d1a524681020430c8712ea392556015c81e4e02847f17435857a774"
    "verification/test_integration_execution.py" = "119e8df0701e4a110d4d13419ca864c90002deb238f843442aa1872f9257e492"
    "verification/test_lineage_split.py" = "a5ab7544a3bcfba9c80bef10238fa03713b07b9cf46d2845bd88db3ea3dedbb8"
    "verification/test_matlab_evidence.py" = "c17da7b4e6df1d2bf8c8bdeba7616d28081a53fa4a36fd86d202f6bc719c65a1"
    "verification/test_public_verification.py" = "5ef960a5004a3228aa73356ae67746737d14970f048ff02bc81e8d516f11c6f4"
    "verification/test_public_verification_consistency.py" = "8100627a20dd4d5b51724209069bf5b5f3cdb719e55536fe99938aa2ebde83a8"
    "verification/test_rule_boundaries.py" = "9d61d0c5ce9a5fc20e8e38c63c8998fe136084b8d72855383792814484b12517"
    "verification/test_suites.py" = "e32ba60cf5cafbf2264fdd9a9899eae0ee5f6bc467165fc909521342c0270411"
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
if ($Suite -ne 'android-validation18') {
    $python = Get-Command python -ErrorAction SilentlyContinue
    if (-not $python) { throw 'Python 3.11+ is required for the additional suite dispatcher.' }
    $arguments = @((Join-Path $PSScriptRoot 'verification/suites.py'), 'restore', '--wrapper', $PSScriptRoot, '--suite', $Suite, '--destination', $Destination)
    if ($Resume) { $arguments += '--resume' }
    if ($IncludeSubmodules) { $arguments += '--include-submodules' }
    & $python.Source @arguments
    if ($LASTEXITCODE -ne 0) { throw "Suite restoration rejected or failed ($LASTEXITCODE)." }
    return
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
