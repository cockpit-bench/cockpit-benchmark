[CmdletBinding()]
# After a network interruption: ./restore.ps1 -Destination <same-directory> -Resume
param([Parameter(Mandatory=$true)][ValidateNotNullOrEmpty()][string]$Destination, [switch]$Resume, [switch]$IncludeSubmodules, [ValidateSet("app","fw","new-energy-matlab","android-validation18","matlab-simulink","all")][string]$Suite = "all", [string]$SourceMap, [string[]]$RepositoryIds)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$expectedHashes = [ordered]@{
    ".gitattributes" = "5550472b34249d85a794952825db528251956dd8bfff9dd17589ea767446f588"
    ".gitignore" = "5cd94eb8d8b18a6dae65d262d5a1b8f5eff0c3f9da4b6c0be88264e8b76a6b60"
    "ACTIVE_EIGHTEEN.md" = "f64d70be58fea89e65d152c839f8e47a386f5e5db8c43ec81cda6008ad35881b"
    "LICENSE" = "950f20ff178debfcf2526200837304a7512f39c022dc1f9105a6e0af62788df0"
    "NOTICE" = "ff71f002bf010747ebc6a65858605d93e07bdbf19e2514ea0bab67f6e8bb1420"
    "README.md" = "42b9831902d8e20377a588fa0839fbed1efb6aaecf8037fd562ae6f4b8ba923e"
    "SCORECARD.csv" = "49aaa5df1f3d561d56f6d3870ca27df2dffda6bb428cac122e597cd710e4e730"
    "SCORECARD.md" = "c0d86db5ebbb779a086d18d49bfeff354fb4da2c2b90f5e062a232819507ccb8"
    "SCORE_RULES.md" = "2bb21ed67c9e47c3cf7691bc2a526fa3e2c41b410017fa4faa41a02132da7b91"
    "STANDARD_SCORES.json" = "901fa4c74245967a5d91379de0a9b0d7330c057aeb464537151366501c403540"
    "delivery-scope.json" = "a2e672700421863ec5fc5932b92b7f57dd21673e489392d761901e45690f7126"
    "docs/API_GOVERNANCE.md" = "5df876b326a2bc66c06972485dfa3a9c41826eecab8e0224bfae120fc1231620"
    "docs/BOUNDARY_CANDIDATES.md" = "833cb1786bdba58e3586d92805c4a7f0494d5d846002b8e1ce7a6f36ddbdc265"
    "docs/BOUNDARY_REGRESSION.md" = "4895a639ed08bc349888b7a5394e1fc7a03aa943a7a8dfb73021dd0e77c93f2c"
    "docs/CONTRACT_DECISION.md" = "d3352916f9ec02b48ae7ea4903e1a09ed65911e944da205aab4b7d3f8f851f79"
    "docs/COVERAGE.json" = "27dd09488e68cc71630a9223f2d5a0ac9cb9bb52d5a5a6390bd39708b53b8f79"
    "docs/COVERAGE.md" = "694fc888f1f4b915ced2b72edac7f49d92b03030ce97ce3faf5d6e14e4073b1e"
    "docs/CURRENT_EVALUATION.md" = "9ca2df4b4e66ff91d28718df646c0d7a916d36775f2787eec9d053fcd0d4c896"
    "docs/DISCRIMINATION_FIXES.md" = "8b2e528e8ab652140344513c690a7f15100b08abcfd34e31363e92ab40048cc1"
    "docs/EVALUATION_BATCH.md" = "97835bee70c140cb381707737f27ac4708c97a7a70a1562f3dcacdf6768bd107"
    "docs/EVIDENCE_AVAILABILITY.md" = "48661c71c76d3afa5c0c6e321e5993b244cb9fcba3423d1fa8b5804fae9cc5d2"
    "docs/EVIDENCE_PROTOCOL.md" = "55da0019130fc7c3603bdd67655aaff23c255b0fdd297f624ebb29bfff47f22b"
    "docs/EXECUTION_SPEC.md" = "b8659cfdf5bc699dd099a88b5bb3fd768f85395b56a6fea0fdea9296a2db365b"
    "docs/EXPANSION_20260909.md" = "4d8ef7252f78cfc7c5c2bd64e1ff9e740dd10f426e7dc5cbe198aaf3d50af2aa"
    "docs/EXTERNAL_GIT_INPUTS.md" = "0330d0a1eea6a37c0ed2a9ec95613974e9174d813dd97d26330595f819a1a6c9"
    "docs/HORIZONTAL_ARBITRATION_V093.md" = "504dcaab3441221d831aab02113614cc4fd92b0a4798ad5b6aa9faf05e8ac17f"
    "docs/INTEGRATION_EXECUTION.md" = "2b5b369751f52ee224d040fb2845df0451c31b6d1ef5f1c4269a89233f818e9d"
    "docs/MAP_OCP_ARBITRATION_V094.md" = "37aa04ae1b10ecbba7b40a6b21c3566cee1e2110ffab42581067a83d35a9ae1d"
    "docs/NE_REALITY_REBUILD_20260910.md" = "b363a88dfa11bea1a658501ee6fc862560b2f5f0bf9c71da186763fdd255c281"
    "docs/REAL_REPOSITORY_GUIDANCE.md" = "862ad8541dccc85dd6c752aeb1c1645f5a4dfc6389c38158985945ef8a1b3051"
    "docs/REVIEW_FIXES.md" = "601899e42f1da145fb60929efffdc4e70c0a9d1205a9cf9aac99a9b7dd535cb2"
    "docs/REVIEW_FOLLOWUP.md" = "4dc3d8ed714a189e1c396ee3da179235dbd9e7394dbce160169b3fc0ba925a9f"
    "docs/REVIEW_V0101.md" = "efbcfae3f1f6c20c381452dddba6912be275ae69717b14a888332482b7399ccd"
    "docs/REVIEW_V0102.md" = "86a59568937fb3589acdce9a5ae374463ef83b5b830baa5c8c85412f11dced7f"
    "docs/REVIEW_V0103.md" = "cd6587d05c34a881df6a908b4095910f0f7a743fd4d069c7fb301668520b4619"
    "docs/REVIEW_V0111.md" = "362d3a2fae19a9ac894af523dd352a9e7f2c4fdd2008e0eb12e14441bfe96f04"
    "docs/RULE_FIXES.md" = "2eac51b7ddc3877d9cf309e948af300a089e3ed416ba41a1919818fbb4abc154"
    "docs/SOLID_CALIBRATION.md" = "c7523cdfc750052f12eb970f0db0b3f7286107727ecc5bf5d31be05e3382ec64"
    "docs/SOLID_CALIBRATION_V092.md" = "da7fd301095cd10dcbc5acc2263272f3811902599bbeef2b24938feda8b4aa6e"
    "docs/VERIFICATION_INPUTS.md" = "fde1e48faa97f29733d9d2260fb870eec53fb616128ab467cd9ce04bb4b3949c"
    "docs/WEB_REVIEW.md" = "d6f07e22a0bf46497276d77c04465727db9e5b8fa481e35be9aa06aaf12e5e2c"
    "docs/boundary-candidates.json" = "373a07b7fe67e5f76e023b088399f3dddb83c4e701aeae1661b31e40121ae228"
    "docs/boundary-reference.json" = "ec56264242213590a570f0e42d5bca470dd6c377c86fd6176ad066bcb883b088"
    "docs/compilation-calibration-v092.json" = "1edd4098b31321ae15dfed98ee08cc040ff3aaf223730876138c9baa339ba765"
    "docs/contract-sensitivity.json" = "6fa28378d96fe470869c569be64951d77ab91920fc21563426d9898099caea55"
    "docs/current-distribution.json" = "d18c82fb286ecd37674159d95bed7807e1a9a894185b53cf348e031ef5f7234e"
    "docs/current-evaluation-summary.json" = "7aa5403efbf9ac17c3ef695c000c5c6c1ddb396fc346161eae8c188e5496af68"
    "docs/current-evaluation.json" = "80eed2abb3903edf0b0b4575c4e0ec5ab6d9875f2872d3f38ffb4fff16b26949"
    "docs/evaluation-context.json" = "d31b289210347f996ad0744c3cef08c49a362494c482e6808eb5ad0cfc49e1ee"
    "docs/evidence-availability.json" = "5cdca5b0f3e0bcee18120a25c09f67ba34bb945ba305d5b9c31ebb1a0dbd4478"
    "docs/horizontal-arbitration-v093.json" = "e97da2b11fe4045af768e7ffe73d51a061a5e9513c2d20d13be1322c980ab899"
    "docs/map-ocp-arbitration-v094.json" = "ed69b0f08dd73eb0d14b54d6ad1106d0cdece6218400a54612be08ece73e1f9d"
    "docs/population-diagnostics.json" = "350806913f50c6f69509ec9926cf53c661a953092845f1d12bb86508d933cae7"
    "docs/solid-calibration-v092.json" = "da29557a92e5a4661966669b928a2d4fe9bf439a089fd9603f448b334a8444b2"
    "docs/solid-calibration.json" = "da273627b2b3ff3dcba58ba8131f321121683ef8c429e29ba216126c3879e8ea"
    "facts/APP-01.json" = "0f65cbca530a6d8046e3007df4778df9272f817807bea43847a963fd2011196d"
    "facts/APP-02.json" = "35e7b0e157fbcf34d93d412a5f4bb83ad54d26abff9549803cd6403be9a31861"
    "facts/APP-03.json" = "6a300cb5d8ab648b2ff108f6ca11a9c9d46080b22f80383576890a8aa47b686c"
    "facts/APP-11.json" = "abba1db9af12db5d97db53d6652e4ae8ab4a9cd0ba30d50384584307c364fb7d"
    "facts/APP-13.json" = "12975789a7a9311f9c30c19bd761048916fb05cee9c0bd45c73b68223d53441f"
    "facts/APP-14.json" = "6ebe1f4b81dd8f614230aae77b18edd22073a1dcf90d2db7417c993b6c5857a2"
    "facts/APP-15.json" = "3995842436d7e1026d121f2538a295f7bec42cd6ce5345a5b579cd3eb030959c"
    "facts/APP-16.json" = "de9dfb6c96bfabfe375c45d1270859018e2f7199a0bb04f31585364211a3e2c1"
    "facts/APP-17.json" = "12f33a7fe36c7026f9dabb966fee27d2f0b8e9eb12ca077408be4ce815ae1eb9"
    "facts/FW-02.json" = "d1f6c2158e9793c6ae656507213be40043a7cc89a28797d6409348f7c9a9a51b"
    "facts/FW-03.json" = "abbcfcef0dc83f09ca30bcc845b2e1e90b752e82046da97d02b99143143240cb"
    "facts/FW-07.json" = "689d704c04ac1cb1b5af598e129170ab49d50cf809ee68d2ac68a07d2076001e"
    "facts/FW-08.json" = "9bf87026c696ef96082e74bb120b068d3b68233ca5b27a6a8dc3fe6d5f587728"
    "facts/FW-10.json" = "a12f60e028f4a1448e1656a83b32c51477d25fccb9105eabd175924f123706cb"
    "facts/FW-14.json" = "591cd656cbfb888680b6f2764df1694035c2e4769b08d583eb11e1e696b517dd"
    "facts/FW-15.json" = "72e61fa37f717d4f9812e8bbf2cc6c3ec6fc204a8f193693a5bcd701ce96c60f"
    "facts/FW-16.json" = "6c6648736f65ace697982c6af6cb228d93b33e4ce27f552cb120a524c7048461"
    "facts/FW-18.json" = "d83fda97e329cc372f78c3a1c852bb4ee1fcdf70798684b0d4f749a44c6b9498"
    "manifest.json" = "e1256ec573ed1746b2f239cb552d44cf51f7b935ee88f11003013de56d52981d"
    "manifest.md" = "a8130ed19f05673eb00fa8f8e6ede623513fa95c9210c964bd09d9b92f55ad87"
    "oracle/APP-01.json" = "10d10fa3e0a4a101c872e4673eea20dd66021b27388be3381098bc2caa5e77a8"
    "oracle/APP-02.json" = "306d81c657bfd3fa33b9f4cc0808fbd2d724c9bbbb3b22e4a8962d8b86ea6fb0"
    "oracle/APP-03.json" = "6d973774bb23f7df254eac8340da7d44be7382c4ec80c2d041fe919181ff1b25"
    "oracle/APP-11.json" = "750b131b4e588e149ffa7aa70e81a292472078a579722e24e0002ef03721215c"
    "oracle/APP-13.json" = "8f7c62a7a3eb5813011a75c90ae0ad4b11f25f99bf8e1785b1e7eb7dce16ab49"
    "oracle/APP-14.json" = "995e18a0287d666bddcd0bac3a53b357be43034e18ca38a4a899628cc5368aec"
    "oracle/APP-15.json" = "76a4ac876633c2bc3f1122af5c6d5e961eafbfe854fa61bdd3d6367f0d27e718"
    "oracle/APP-16.json" = "50e995127468769e2322c8d074be684f29726dd78bfe5c4a609628c9062ba3c1"
    "oracle/APP-17.json" = "976f64d3d690b7a15642ae062982d3c969ae1e21b0e701d7854bd4e4b09fb62b"
    "oracle/FW-02.json" = "b75315959bfe17f3340f5a0a42c4ae5dda5511829913029f75435dff80d325ac"
    "oracle/FW-03.json" = "639c02b517309d9ae0a5fe6878e13c2d0adb8b3c54f045abf6bf25fb8b1f695c"
    "oracle/FW-07.json" = "2e34792af028a0b9afffcd704048f7ca11e249f5dbe1fc4beac2c000067520a5"
    "oracle/FW-08.json" = "3f60fe4563540a576b5891edae8f4319f7b5b71a0178a5b37b06aac3cf0da054"
    "oracle/FW-10.json" = "9a481ffef562b9e651e9bbb9afb738c13e9c6fb57ad9b37b78cc22f99b9e6df1"
    "oracle/FW-14.json" = "bb85e95243286a7f32c882120973f61a1c00097efba086d4250dce35ec8a911d"
    "oracle/FW-15.json" = "79a7c638cb4d735f02712ee5160659281b89f0191b1c7281254d68ba9b33443d"
    "oracle/FW-16.json" = "dceb43bea031c520526328a73e71e80e157da6c11b56a74a6bc2f921831368d2"
    "oracle/FW-18.json" = "4a4830eb68ede260e6a6ca4b0ee45c3dd0122fef5128ddb085f7371e0748b4bb"
    "suites.json" = "e91317256d5f28959b24cf2a006141c4a29ab652a95af387ca325cae249db446"
    "suites/app/SCORECARD.md" = "43dcf1b0cd9bf93cc4d7f165dfb16df3d766d5ca54667fe52ee99f82af2682c9"
    "suites/app/STANDARD_SCORES.json" = "f9ef83d2e95632ad1ae3c7eef369b93a152fe1bd55fe6daef854e80d49e0cbe3"
    "suites/app/additions.json" = "d164fb7243b3131362e3cd4fd781d45ed901884d0c848b460c5c470cc6c60a78"
    "suites/app/evidence/APP-21-source.json" = "bc896a055575968a5859fa95cdfc319468518dc6f34c58c95b9a96173091cc94"
    "suites/app/evidence/APP-21.json" = "721b6866a0f2994a911597b347a4a76aaff714cc11aad91bd0480b72f6f3ee70"
    "suites/app/evidence/APP-22-source.json" = "4a6b232e039df62dd9c71b7b9af03aa4ee5cee332599005d441ce00e7d8692f8"
    "suites/app/evidence/APP-22.json" = "285f231fef12b085233ddb0ba0c5faecdc1b70b6b54f2781c8e384f791589268"
    "suites/app/manifest.json" = "bac5e0da66faf6207aee44179ebab41f6a0bc7279e517f5acb6ecfc5f86cf361"
    "suites/app/revisions/APP-13-v0102.json" = "c71de127db42c0c09e8ca9c598929aad530f7c9fc8688fcb075750b68b3dae8a"
    "suites/fw/SCORECARD.md" = "c21eaa80af378fb5bc94112f0753694566db3024eab4f16474636be19204aded"
    "suites/fw/STANDARD_SCORES.json" = "4c5a7a6cf7ebcbcc93c901caf3709cddc14571c08ae14f4aa4c929321a48624b"
    "suites/fw/additions.json" = "733831ed61796fba710420710718f00f8a2c980c17c60f69743143dfb959a703"
    "suites/fw/evidence/FW-21-source.json" = "afaca551de9c3320fbbe42be876cb6b5bff7a1cd12d0489af611fb1d06ca5a31"
    "suites/fw/evidence/FW-21.json" = "7bb41566ce88642140a0e6956fd0edd1e7a238e588b4ca7e98e2a083c1bcb0e1"
    "suites/fw/evidence/FW-22-source.json" = "82dffb1691142d29491a597611651b2b6148892e0059a78268d71b5e4b5267b5"
    "suites/fw/evidence/FW-22.json" = "1c41d2c1b9745d0caa7166b8a28a101cfee05ad435846c5c05dcb833d2f9e401"
    "suites/fw/manifest.json" = "f36682b7f2ae29d45677ed95b2c529c54993dd87aadf27c530a6cf433709fb2c"
    "suites/fw/revisions/FW-14-execution-rebinding.json" = "b2176c751973866e3be5689469d5b5134121019b5861bbcc3d4bbcb4e6e34788"
    "suites/fw/revisions/FW-14-v0102.json" = "1e096c78e17dd8f924cfdaaa68f42b5124491d8cbb4bf71290f081ff3606d887"
    "suites/legacy-v094.json" = "a1944ba5d6d8a5a5d58d1f3d7b270b26150cda56a165d12c3c9737df754cae5b"
    "suites/new-energy-matlab/cohorts.json" = "1bd4f810a006a09fba201ff4948f9377c03f940b47fe42c0a474b1fc6b868ad6"
    "suites/new-energy-matlab/cohorts/reality-proxy-20260910/APPROVED_BUILD_CLARIFICATION.md" = "9519b6a56ba9834f8f2059ebfd4e7e16c612133a2002cf827888c63603ca150c"
    "suites/new-energy-matlab/cohorts/reality-proxy-20260910/EXECUTION.json" = "c8a68890ef7ebac767155ce059b8e86d34971c973050f70e24661db1be7d71fb"
    "suites/new-energy-matlab/cohorts/reality-proxy-20260910/LINEAGE.json" = "fec0da157bce79694e8f4c1ceb1de4debfc08406f0738872540e266e29336f67"
    "suites/new-energy-matlab/cohorts/reality-proxy-20260910/OBSERVATIONS.json" = "2b985adb1aa8a39c7c96b09e75ea7289bc98a87eddd19cf8d4b67aa3e8f634c8"
    "suites/new-energy-matlab/cohorts/reality-proxy-20260910/PROFILE_COMPARISON.json" = "512a0aaf4d9febc8390498a9c1c4f433071d2bbb633345b9b333a7a78af9d108"
    "suites/new-energy-matlab/cohorts/reality-proxy-20260910/README.md" = "b363a88dfa11bea1a658501ee6fc862560b2f5f0bf9c71da186763fdd255c281"
    "suites/new-energy-matlab/cohorts/reality-proxy-20260910/SCORECARD.csv" = "0c13df69dc81bbc98c0a56360f84cc3a315f7206dbf1981384677d5a71f9b151"
    "suites/new-energy-matlab/cohorts/reality-proxy-20260910/SCORING_CONTRACT_PART7.md" = "2bc31dcbbb9c3cc2ea11686a9d3e3cde0225c6213107b92f771303efd059559b"
    "suites/new-energy-matlab/cohorts/reality-proxy-20260910/STANDARD_SCORES.json" = "538c95b3bd1e4e6627ed398c2a450a2f0b332a956e3a8b1e75ed2e4d3142545f"
    "suites/new-energy-matlab/cohorts/reality-proxy-20260910/contract-index.json" = "0e520a2a41904649c545164fdc8d37abff0588b6c5aa943e9f863c22525b389d"
    "suites/new-energy-matlab/cohorts/reality-proxy-20260910/manifest.json" = "501802f32c9b94c47564e41ce018e4421bfe3660a751552199ce8f22b53f49ee"
    "verification/README.md" = "12ff137a9e25cbb11ecf87b2a99bf3d6217956bb51b6692c1ca7052c0f070bd5"
    "verification/boundary.py" = "9b9888b7e33b26ef4b65033d982099c413540074408ff81df0f6cbd34a59f384"
    "verification/calibration_census.py" = "0e53528399d8ff5448610e4f2492df00121a4ba71c49914b991b565c31d23e30"
    "verification/check_split.py" = "7a85129e20da6e5d52b07bf35ee244fd68305f9b122c9cb6478b07b1c37d1c8e"
    "verification/counting.py" = "01535dfe4097e289681ec0ab9f8d774cdfe11811c4d249c0050cbbee686ab9da"
    "verification/coverage.py" = "74876337d45bea4260ed60c94a00c6105464c05adff3e0df951d0d02a35a9392"
    "verification/evaluation_batch.py" = "2b1f826f034fd09032c7c4109a39f98a5da574929fc5e5d1278c91c9a699f5a9"
    "verification/evaluation_current.py" = "29a2a82febf4ef1f38311acd7f0e5e5229caa3fd5d619314585c7b57aca2edc9"
    "verification/evaluation_profile.py" = "bb7ee5bc285526adbebf22afaee3357e1ce0e7df6eba96f5ff6d0b208ff9797c"
    "verification/examples/build_boundary_prototypes.py" = "5c802e00142f1815b67271210f51b3dc824e3598e84027667b64f02a81794394"
    "verification/examples/current-assignments.json" = "fbd504cd7284bbc0f54dbe0948fbba61aac0568cd107a0cf48a256efd3156e02"
    "verification/expansion.py" = "0dd4a109a8d77a0615313ac55ecd11ec8f68ca980ab560681b746661e5c210ff"
    "verification/external_inputs.py" = "54882587f5cad6dd75be0b5b1feca9ac3c4dbe252667bc3b17dffd654b232b5d"
    "verification/ne_reality.py" = "3c449793c0065ae13d04fb3c4247702e77ba14e09c86330cefc5ffd0ae44c47c"
    "verification/ne_reality_census.py" = "d88ffdbb547c3b74aa9fe7ed3a576dd502533c7ae0a564c0a3be0ada2ea1b017"
    "verification/ne_reality_restore.py" = "2d02474749ff9ceeaaf2294b88679582762133e071b1461c82922dfebf325a63"
    "verification/population_diagnostics.py" = "33aef774ad1ab1c58b8a01e659c6d78dc26c3860da77cd0412169a667ca0d383"
    "verification/reference_revisions.py" = "b300b9ba0c8daf3c672775f0934f11d182a9e8ce58208ec8ee6211d36cebcb9c"
    "verification/repository_types.py" = "74e0c7a6a481727c9c951c25af16ba964115ad80c5e89321cd23e56efcaadd41"
    "verification/rules.py" = "f0936ed0d1bb7400f4f44985abdb23c41330e5593fe7ea08643dfd652b334c4d"
    "verification/semantic_audits.py" = "2a2ca58d25c77e583d61f832b72f666799564f290c90657daf4d4846521ca3b9"
    "verification/suites-v1.schema.json" = "e293769beb9b82de969bc8ede7cde568f5fd8c3c499375253af0d19840c67244"
    "verification/suites.py" = "9b71365ea8c352fdc57a889166032a504e658ac0474ed8b34fcdc2436325db0f"
    "verification/suites.schema.json" = "b5fd10ccead50341591d53950154dbab4a98764764d04f7c3c40dfb2e5e0d4c6"
    "verification/test_api_governance.py" = "b6dff09ba8cd6f0074e5faa9664f97604b78e8b8de90f1a2729288fa63f9c315"
    "verification/test_boundary_regression.py" = "a4237e27c9f627f2a5f807fe02e97149903e9db1c17c27a5992c84889cde83a2"
    "verification/test_calibration_census.py" = "9334b11434542bc99d00fa0d4e34df426e0f6e003695482f53411aacca570057"
    "verification/test_cpp_counting.py" = "79c6f3d34c6a8d20904f3f1747b440e56f728cf54820d93b9df06680000370a5"
    "verification/test_evaluation_batch.py" = "2e948b6d4517a931514423ece625cab27cfb92e4ea52a21a7b1871bb7896eea0"
    "verification/test_evaluation_current.py" = "65e6f1631f240b6c2d6ca501f89339646079445e64c3f29d690e9091a62d369d"
    "verification/test_evaluation_profile.py" = "b999aa7d419cf5e4738bb91de00ae14bb2d42f349f98f89c498810b2dd24a3b3"
    "verification/test_external_inputs.py" = "9c364f6e1d1a524681020430c8712ea392556015c81e4e02847f17435857a774"
    "verification/test_integration_execution.py" = "119e8df0701e4a110d4d13419ca864c90002deb238f843442aa1872f9257e492"
    "verification/test_lineage_split.py" = "a5ab7544a3bcfba9c80bef10238fa03713b07b9cf46d2845bd88db3ea3dedbb8"
    "verification/test_ne_reality.py" = "cc3f284c6c1e8a53d1d0f41d4faaf0bde734b2efd39ac54576062f2aa16ecb27"
    "verification/test_population_diagnostics.py" = "99b42825aebba750d5539411c9d02c35613e9fbfd4efc1d199274deb3dba14cc"
    "verification/test_public_verification.py" = "5ef960a5004a3228aa73356ae67746737d14970f048ff02bc81e8d516f11c6f4"
    "verification/test_public_verification_consistency.py" = "8100627a20dd4d5b51724209069bf5b5f3cdb719e55536fe99938aa2ebde83a8"
    "verification/test_reference_revisions.py" = "9c39b471dd82e9b17b6626c5688698c5f6fac5c65f2b3251251673853a92b0ed"
    "verification/test_repository_types.py" = "b96c97a2883ab61514f4b8a1ea603c878b0a9ce47f3ab9ef82411d1259c1cd92"
    "verification/test_rule_boundaries.py" = "9d61d0c5ce9a5fc20e8e38c63c8998fe136084b8d72855383792814484b12517"
    "verification/test_suites.py" = "b882138f798cd25224d64467f5d7c9e12e5b33beeea1170ed702f028f2eb1d49"
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
$registry = Get-Content -LiteralPath (Join-Path $PSScriptRoot 'suites.json') -Raw | ConvertFrom-Json
if ($registry.schema_version -eq 'benchmark-repository-types-2' -or $Suite -ne 'android-validation18') {
    $python = Get-Command python -ErrorAction SilentlyContinue
    if (-not $python) { throw 'Python 3.11+ is required for the additional suite dispatcher.' }
    $arguments = @((Join-Path $PSScriptRoot 'verification/suites.py'), 'restore', '--wrapper', $PSScriptRoot, '--suite', $Suite, '--destination', $Destination)
    if ($Resume) { $arguments += '--resume' }
    if ($IncludeSubmodules) { $arguments += '--include-submodules' }
    if ($SourceMap) { $arguments += @('--source-map', $SourceMap) }
    if ($RepositoryIds) { $arguments += '--ids'; $arguments += $RepositoryIds }
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
