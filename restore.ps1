[CmdletBinding()]
# After a network interruption: ./restore.ps1 -Destination <same-directory> -Resume
param([Parameter(Mandatory=$true)][ValidateNotNullOrEmpty()][string]$Destination, [switch]$Resume, [switch]$IncludeSubmodules, [ValidateSet("app","fw","new-energy-matlab","architecture-center","ai-center","intelligent-driving-center","android-validation18","matlab-simulink","all")][string]$Suite = "all", [string]$SourceMap, [string[]]$RepositoryIds)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$expectedHashes = [ordered]@{
    ".gitattributes" = "5550472b34249d85a794952825db528251956dd8bfff9dd17589ea767446f588"
    ".gitignore" = "5cd94eb8d8b18a6dae65d262d5a1b8f5eff0c3f9da4b6c0be88264e8b76a6b60"
    "ACTIVE_EIGHTEEN.md" = "f64d70be58fea89e65d152c839f8e47a386f5e5db8c43ec81cda6008ad35881b"
    "LICENSE" = "950f20ff178debfcf2526200837304a7512f39c022dc1f9105a6e0af62788df0"
    "NOTICE" = "ff71f002bf010747ebc6a65858605d93e07bdbf19e2514ea0bab67f6e8bb1420"
    "README.md" = "d0e218c352e01cc003676f5d73e7707c3735d2a5d112ef24197fca912b30d10f"
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
    "docs/CURRENT_EVALUATION.md" = "62b5af63edc86ae6806b8900d2258274e95def6bb37539b4fb60b42688a86c44"
    "docs/DISCRIMINATION_FIXES.md" = "8b2e528e8ab652140344513c690a7f15100b08abcfd34e31363e92ab40048cc1"
    "docs/EVALUATION_BATCH.md" = "97835bee70c140cb381707737f27ac4708c97a7a70a1562f3dcacdf6768bd107"
    "docs/EVIDENCE_AVAILABILITY.md" = "48661c71c76d3afa5c0c6e321e5993b244cb9fcba3423d1fa8b5804fae9cc5d2"
    "docs/EVIDENCE_PROTOCOL.md" = "55da0019130fc7c3603bdd67655aaff23c255b0fdd297f624ebb29bfff47f22b"
    "docs/EXECUTION_SPEC.md" = "b8659cfdf5bc699dd099a88b5bb3fd768f85395b56a6fea0fdea9296a2db365b"
    "docs/EXPANSION_20260909.md" = "4d8ef7252f78cfc7c5c2bd64e1ff9e740dd10f426e7dc5cbe198aaf3d50af2aa"
    "docs/EXTERNAL_GIT_INPUTS.md" = "0330d0a1eea6a37c0ed2a9ec95613974e9174d813dd97d26330595f819a1a6c9"
    "docs/FIDELITY_REPAIR_20260910.md" = "edf8c6601a431a78065d95305e4b6a2d1f7e2eb6859d19e579327eef817e9fd3"
    "docs/HORIZONTAL_ARBITRATION_V093.md" = "504dcaab3441221d831aab02113614cc4fd92b0a4798ad5b6aa9faf05e8ac17f"
    "docs/INTEGRATION_EXECUTION.md" = "2b5b369751f52ee224d040fb2845df0451c31b6d1ef5f1c4269a89233f818e9d"
    "docs/MAP_OCP_ARBITRATION_V094.md" = "37aa04ae1b10ecbba7b40a6b21c3566cee1e2110ffab42581067a83d35a9ae1d"
    "docs/NE_REALITY_REBUILD_20260910.md" = "c4036c478478a725d03277ee27027b2b17afae6ee86d849c3c306695f9999c3b"
    "docs/REAL_REPOSITORY_GUIDANCE.md" = "862ad8541dccc85dd6c752aeb1c1645f5a4dfc6389c38158985945ef8a1b3051"
    "docs/REVIEW_FIXES.md" = "601899e42f1da145fb60929efffdc4e70c0a9d1205a9cf9aac99a9b7dd535cb2"
    "docs/REVIEW_FOLLOWUP.md" = "4dc3d8ed714a189e1c396ee3da179235dbd9e7394dbce160169b3fc0ba925a9f"
    "docs/REVIEW_V0101.md" = "efbcfae3f1f6c20c381452dddba6912be275ae69717b14a888332482b7399ccd"
    "docs/REVIEW_V0102.md" = "86a59568937fb3589acdce9a5ae374463ef83b5b830baa5c8c85412f11dced7f"
    "docs/REVIEW_V0103.md" = "cd6587d05c34a881df6a908b4095910f0f7a743fd4d069c7fb301668520b4619"
    "docs/REVIEW_V0111.md" = "f9607c430811b1a09572d99d1f6249cd7bea636a57ec9422c87dfc0f7156a02f"
    "docs/RULE_FIXES.md" = "2eac51b7ddc3877d9cf309e948af300a089e3ed416ba41a1919818fbb4abc154"
    "docs/SIX_GROUPS_20260912.md" = "92ec8fdbe60c855c018a173ce1f09e00ee3f4b651aeb70c9c2f75b4a3ef584e8"
    "docs/SOLID_CALIBRATION.md" = "c7523cdfc750052f12eb970f0db0b3f7286107727ecc5bf5d31be05e3382ec64"
    "docs/SOLID_CALIBRATION_V092.md" = "da7fd301095cd10dcbc5acc2263272f3811902599bbeef2b24938feda8b4aa6e"
    "docs/VERIFICATION_INPUTS.md" = "fde1e48faa97f29733d9d2260fb870eec53fb616128ab467cd9ce04bb4b3949c"
    "docs/WEB_REVIEW.md" = "d6f07e22a0bf46497276d77c04465727db9e5b8fa481e35be9aa06aaf12e5e2c"
    "docs/boundary-candidates.json" = "373a07b7fe67e5f76e023b088399f3dddb83c4e701aeae1661b31e40121ae228"
    "docs/boundary-reference.json" = "ec56264242213590a570f0e42d5bca470dd6c377c86fd6176ad066bcb883b088"
    "docs/compilation-calibration-v092.json" = "1edd4098b31321ae15dfed98ee08cc040ff3aaf223730876138c9baa339ba765"
    "docs/contract-sensitivity.json" = "6fa28378d96fe470869c569be64951d77ab91920fc21563426d9898099caea55"
    "docs/current-distribution.json" = "2cc75abb320ff07ca35d16582d6f36c00361f3d212cda65f26a3c4ec5b9cfcba"
    "docs/current-evaluation-summary.json" = "8a1b32fd703d3e45cb2c1c00913a29b39be19f26daa7ec4fdcb017d6688f94cc"
    "docs/current-evaluation.json" = "adfe7f13f11540123d5b6126828e16cb0ed9dbeb5c814aa4d695a4e503eb6d4d"
    "docs/evaluation-context.json" = "d31b289210347f996ad0744c3cef08c49a362494c482e6808eb5ad0cfc49e1ee"
    "docs/evidence-availability.json" = "5cdca5b0f3e0bcee18120a25c09f67ba34bb945ba305d5b9c31ebb1a0dbd4478"
    "docs/horizontal-arbitration-v093.json" = "e97da2b11fe4045af768e7ffe73d51a061a5e9513c2d20d13be1322c980ab899"
    "docs/map-ocp-arbitration-v094.json" = "ed69b0f08dd73eb0d14b54d6ad1106d0cdece6218400a54612be08ece73e1f9d"
    "docs/population-diagnostics.json" = "211cd0f13655aad27aee71aca5e559f1cb8baec66d4605fef093078b2a69868c"
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
    "suites.json" = "ce0dc6e38f8acd6ef6aaad6407be9ac9b9ec9d70140de30d0a2634085306e1be"
    "suites/ai-center/STANDARD_SCORES.json" = "59d9ca22878db28f152fbd96467ede16e01dd352bc8a169474df33d09b7819c6"
    "suites/ai-center/contract-index.json" = "a23c17970bdf0f5dfe18b58090c7d5d4021d77fc4f6b6adf64dc508f069cc395"
    "suites/ai-center/evidence/AIC-01.json" = "527bc934c1050b9f43b5ef528b805ced9cb8b851e62a763a04f756048167b3bc"
    "suites/ai-center/evidence/AIC-02.json" = "ca2b942c62395c570f03d9046a2af4db45ffce033b0b253031899155fd6a3bca"
    "suites/ai-center/evidence/AIC-03.json" = "012307d499e33d4bda67ffad8eba1ca9234074bedb12ba8e538314d249d41e4f"
    "suites/ai-center/evidence/AIC-04.json" = "6f72333c7b8d579694658e9c9ab63e7d674302630d3849249ef9cec50c48ceaa"
    "suites/ai-center/evidence/AIC-05.json" = "21b0415c17efe335732f3e6e41369b53e5c9704435d3d799d742c747acdf3bd2"
    "suites/ai-center/evidence/AIC-06.json" = "02b385e00f12da1469334cc56cbec2150ea2b4f9938830c19d453dddbe4b5665"
    "suites/ai-center/evidence/AIC-07.json" = "e23e6965bc064d1cd8090d03cf7818fb45716a0da52f9f1a8680b71cdaf9fbe2"
    "suites/ai-center/evidence/AIC-08.json" = "4e65f77eca13daaa3316dd0d4f1db18591e581a8960aa9b4a338309523d05734"
    "suites/ai-center/evidence/AIC-09.json" = "3e611f85716832a5f61967201bafde21bdeb456cf278ac0704c0a11ea69135f6"
    "suites/ai-center/evidence/AIC-10.json" = "ea7b042cd18b1b93d1fa18815f1c90c860d874561d9eebd37327459149d6474e"
    "suites/ai-center/evidence/AIC-11.json" = "dadf9a6878cd6da2a0fca6c758ed151f7afb269f5f7a27874026c5db9399842d"
    "suites/ai-center/execution/AIC-01.json" = "3f728b0265b12fab92336167e4b7e15f73881093142cada91832f9d0b65ae649"
    "suites/ai-center/execution/AIC-02.json" = "30bb25d1805ea3548151088ab7d0693174e5ed37711265afd2c1a831a759e945"
    "suites/ai-center/execution/AIC-03.json" = "de3b852120cdcb2beb955f5524f4641da16cca50e6b45daf4eff2da7735f3edd"
    "suites/ai-center/execution/AIC-04.json" = "3380b9d06d78bec9cac1a117f616562efabfc5edbe5e436f7691dc370f4f8e79"
    "suites/ai-center/execution/AIC-05.json" = "32dbaeaed7b73c65a62ef9bd6a5ea22bd7fb9e6502538dc01b2eb2bb5fa4e8ec"
    "suites/ai-center/execution/AIC-06.json" = "ab4cf0a94db5047222813a3afd39fc2cada3a01be5133f3ec3a5f09b3fa42a5b"
    "suites/ai-center/execution/AIC-07.json" = "e13c330159bbb679ab6da05a659ce95a6ed2dde75d97afe71f63e09a374dd7f2"
    "suites/ai-center/execution/AIC-08.json" = "4227265963875f8b8a4abeb451e1ff176f8baf74ad564cc122ea65bd381d2bb1"
    "suites/ai-center/execution/AIC-09.json" = "7638948c92226c216861f6a85dab228a41b108858da68817d5d6db34805709b0"
    "suites/ai-center/execution/AIC-10.json" = "4c222cca3cbb879a80220223941cd068800f2d5b6f1dca9d3cf66c3687fb2924"
    "suites/ai-center/execution/AIC-11.json" = "368081e6b5b2a963778173d7f771dd76cc2114f15872bcfbda80bbaca110f2e1"
    "suites/ai-center/inventories/AIC-01.json" = "01245c57e95b47c741f26e567be8d7d871e69d2612af13a0b89fb372095cf4a1"
    "suites/ai-center/inventories/AIC-02.json" = "230eb06aa9607083602e7eca73f169729f075404ac3fc4fc6bea7172f7eb14bf"
    "suites/ai-center/inventories/AIC-03.json" = "80321dafb9b6bb939af1afa6ba7f97fc816a5cdb27c6ef10791351f0bd03435b"
    "suites/ai-center/inventories/AIC-04.json" = "8ca5f30f42d0a3952d651ad9e8d234d0f3813ec45cbe5926f295ea694ce04d1f"
    "suites/ai-center/inventories/AIC-05.json" = "848f97dfa0ca39726263c23ce9c95880f6fe7c8d5bccff70c6855a6884a8ff55"
    "suites/ai-center/inventories/AIC-06.json" = "0a186689c99b4e131343e5dc26afa237408fe838e204503cbae3c668b1d05d3a"
    "suites/ai-center/inventories/AIC-07.json" = "5907bb323ed461907b4c97b0a6fafb91c93ba06c1eaf30ecfe67071c269aa81e"
    "suites/ai-center/inventories/AIC-08.json" = "e61439d40847a650a76d15e57587de22c0a1490eb95ae7e66ab493f2c3f0e0aa"
    "suites/ai-center/inventories/AIC-09.json" = "ba5b3f6ca5e9f1fa0d88ae03e5f44363790d4d23479c213abf429b91f59acfba"
    "suites/ai-center/inventories/AIC-10.json" = "8575d16bdd51811076df5a1e92e517ca31ab2ee6479d10516fe2338c73732ae9"
    "suites/ai-center/inventories/AIC-11.json" = "5d47a65d427af02f02980f208836e8de741b6791fc1c421b3a186fa9617f2005"
    "suites/ai-center/manifest.json" = "83604316bab9778315cd1774cb45e592c2b49baadfa6fc71d573e10bf981a5c7"
    "suites/ai-center/profiles/AIC-01.json" = "a6dec079cbc2789c58cc89f358f8bae6cd0fb1f3f1ffc128bd0fdd989f094fc5"
    "suites/ai-center/profiles/AIC-02.json" = "fa7b75e29f50694ea5eda08e234facbd47f7de92b16d9d4205697b20a2b9edce"
    "suites/ai-center/profiles/AIC-03.json" = "d545722577b1c53c1c290fbfc2e76d463bbd78de14fd366336671bbdab6ab1ca"
    "suites/ai-center/profiles/AIC-04.json" = "795f1ebbcf86affce9c56e20e290d907fd4a557c1b0b4c76be9d6aed58f2d456"
    "suites/ai-center/profiles/AIC-05.json" = "bb60ebf2b29a7f3d5f7321262cd74f9aec9a46832c07e60ef271724c312e8241"
    "suites/ai-center/profiles/AIC-06.json" = "53764a1059654aa1ac5cecb5c8ea6124ec79b02251f6edfbf978a609fb42b190"
    "suites/ai-center/profiles/AIC-07.json" = "e753aff62125ae8c3202a535ed38aac51af28e550b3adb8334b1ee14b0fe6ba1"
    "suites/ai-center/profiles/AIC-08.json" = "d92524c2c014cf580311e4264d676bea3e4581d24ca7a23d3202badceb9d13ab"
    "suites/ai-center/profiles/AIC-09.json" = "ca2ec4e14a0605fbb75fd2f84396bfdb479373be6fa6d6d7365068a0c1b27b65"
    "suites/ai-center/profiles/AIC-10.json" = "054cfb20ea816f1acbb31bc00b6a291ef36f4122039c7b97a854550e7e8e64dd"
    "suites/ai-center/profiles/AIC-11.json" = "c37267d1d1569631493dd9efe0f62b34718854d750778d5bab739b9769cb1c2d"
    "suites/app/SCORECARD.md" = "43dcf1b0cd9bf93cc4d7f165dfb16df3d766d5ca54667fe52ee99f82af2682c9"
    "suites/app/STANDARD_SCORES.json" = "f9ef83d2e95632ad1ae3c7eef369b93a152fe1bd55fe6daef854e80d49e0cbe3"
    "suites/app/additions.json" = "d164fb7243b3131362e3cd4fd781d45ed901884d0c848b460c5c470cc6c60a78"
    "suites/app/evidence/APP-21-source.json" = "bc896a055575968a5859fa95cdfc319468518dc6f34c58c95b9a96173091cc94"
    "suites/app/evidence/APP-21.json" = "721b6866a0f2994a911597b347a4a76aaff714cc11aad91bd0480b72f6f3ee70"
    "suites/app/evidence/APP-22-source.json" = "4a6b232e039df62dd9c71b7b9af03aa4ee5cee332599005d441ce00e7d8692f8"
    "suites/app/evidence/APP-22.json" = "285f231fef12b085233ddb0ba0c5faecdc1b70b6b54f2781c8e384f791589268"
    "suites/app/manifest.json" = "bac5e0da66faf6207aee44179ebab41f6a0bc7279e517f5acb6ecfc5f86cf361"
    "suites/app/revisions/APP-13-v0102.json" = "c71de127db42c0c09e8ca9c598929aad530f7c9fc8688fcb075750b68b3dae8a"
    "suites/architecture-center/STANDARD_SCORES.json" = "ded7f12f747fb12b2303575f15e8974fb78b9b535d80342290fe9f8516e1999e"
    "suites/architecture-center/contract-index.json" = "a23c17970bdf0f5dfe18b58090c7d5d4021d77fc4f6b6adf64dc508f069cc395"
    "suites/architecture-center/evidence/ARC-01.json" = "eb4976cb10be49d869624c1220b2f1c52450eccd6161d81b9c32628326f1926a"
    "suites/architecture-center/evidence/ARC-02.json" = "f22a2c22130c6152d8902583a7c0a4f6f73bed030bd4b5d2a0a81ef4016cb9fd"
    "suites/architecture-center/evidence/ARC-03.json" = "30b4f480d0e3e8a22d4b6d0ec8a03a08ee3e2e5dcde2316478defb35554fb827"
    "suites/architecture-center/evidence/ARC-04.json" = "689f042b687974031650bb9ec73ad2daff088d26b60db8c3fc98cc6c4120744a"
    "suites/architecture-center/evidence/ARC-05.json" = "0f917fb68a39744fb4d96d3d47046e26e21e49aa70ceb5d4a87afca1e630b068"
    "suites/architecture-center/evidence/ARC-06.json" = "61a141336c4145cb39068cd94293350c67fe0b0564005de1889b813459172a23"
    "suites/architecture-center/evidence/ARC-07.json" = "9f12e90ade7cc72988e7e29be261166026f5170597974b82d772fccceda3cbb2"
    "suites/architecture-center/evidence/ARC-08.json" = "ac91c880d83223905235467c7a53013049ae716f88a66dda0830760580ee35de"
    "suites/architecture-center/evidence/ARC-09.json" = "74dcf3c2eeb66547ca23fb99d3ca1da4fef8646bea804403fd4a98e0fa5e33a3"
    "suites/architecture-center/evidence/ARC-10.json" = "2a474b279da621864117deffc356fa996cf6c8f318ace4308f2b5875b7990749"
    "suites/architecture-center/evidence/ARC-11.json" = "844c32cdd08d8168006ac73ab6538f7b3e9435bd8d6118246f3f05a4b75ab208"
    "suites/architecture-center/execution/ARC-01.json" = "9d9b562e1e90dacdf6007555738203c2cbd9ea31d70ee366b8d37c998e17a858"
    "suites/architecture-center/execution/ARC-02.json" = "7cfa476d865652db1a585f02cb975f422a4fc2b201ed2a2e00ec51b25eb6e52d"
    "suites/architecture-center/execution/ARC-03.json" = "bbff996000c2b183d176d98062bdd4eb68e2c6c4037acabf41791b86f3a528a2"
    "suites/architecture-center/execution/ARC-04.json" = "c3cfa5f20943419c0823e76171be1e470435009613e170a5488fc44c8e4bdcad"
    "suites/architecture-center/execution/ARC-05.json" = "78e531fc20cce7d67dcfc2eebaebb6c3ba5eadbb49be70b4cda37414a905f27a"
    "suites/architecture-center/execution/ARC-06.json" = "a73250c28ae54a447b68f807052a3e8ae7b8989981ada9e6f33e3ffe85f7a9c3"
    "suites/architecture-center/execution/ARC-07.json" = "2bff45866162c387fa9c651694535f8fce2995a369564b88235891b493544a15"
    "suites/architecture-center/execution/ARC-08.json" = "771b81c334192744b4039adbf637d2f71708da56689b5fa468e0380220c5fd3d"
    "suites/architecture-center/execution/ARC-09.json" = "c552ce2b9df8df2ab753543608f172fdba5fb8834de2488448b473cdfe5afbc0"
    "suites/architecture-center/execution/ARC-10.json" = "020be22e98fd245d8c257adeb873f6c65352fb592e0c6c8a406480bbf611e5de"
    "suites/architecture-center/execution/ARC-11.json" = "58502e528a93b8a788b6244060d55bec64b44f8ccfe368848175fab1882bf1b6"
    "suites/architecture-center/inventories/ARC-01.json" = "9228408ac0ec68b3e14728aab79bba9481959c07b832b877c1f2ccec8ee6b1ea"
    "suites/architecture-center/inventories/ARC-02.json" = "6c9b5212bc1e7419b9cdacf25edfc59f3a3fb77c8673a22c23f0c54fe379e0e8"
    "suites/architecture-center/inventories/ARC-03.json" = "e3262886c815cd6a0353d7d03f047ab74d735326909102053a0d4653f6f3197e"
    "suites/architecture-center/inventories/ARC-04.json" = "c3cb518a0be7e59ea2d88958a125f8eacf50b8ff8a5a76bc7bcfe366b4842c0d"
    "suites/architecture-center/inventories/ARC-05.json" = "9dbe43026472e02d7a313c5b4b51efb69d1b9948d51eb4fa8e0ffd5cc8b39370"
    "suites/architecture-center/inventories/ARC-06.json" = "d6726a132e0ee518b54e801ee15c890d99c4deb38212f0e448a7546892617526"
    "suites/architecture-center/inventories/ARC-07.json" = "4d688872fb4e8baef052ade9b6d0cf25ea8b72179b65ed8059ba892db956c627"
    "suites/architecture-center/inventories/ARC-08.json" = "723db3f3b71496f9a0c55e48561518532427b02dbbe2f42bd19deeb64808fcc6"
    "suites/architecture-center/inventories/ARC-09.json" = "688869b431639104c9f753a8c78fcebac7449304ead245d386799f6a814e8e09"
    "suites/architecture-center/inventories/ARC-10.json" = "6bc8bfba86f428cd86b45208c0ef4f8fd617e6616501f4a39a385924a5da3b5a"
    "suites/architecture-center/inventories/ARC-11.json" = "d15748f0f5eb89c6918e490a27a03c627658b5c6ee7c04a642e276072a6bb69d"
    "suites/architecture-center/manifest.json" = "16e9574918c23dd8ba9def42a11cf75a1e22ef4effeafb48798d9136dd405947"
    "suites/architecture-center/profiles/ARC-01.json" = "3cce5b01e6b1f6a899c0b762a07e705e64afc53b24e63495c3121164f8ce91e6"
    "suites/architecture-center/profiles/ARC-02.json" = "1385cf79ffec6933e054fc81765886f061da14e58aa5ffdeed4c71b7c5495a9a"
    "suites/architecture-center/profiles/ARC-03.json" = "a400badaad2b5c86e60ee6c90bfd65e798d04ed4aa103969ddf74a5623e11fc1"
    "suites/architecture-center/profiles/ARC-04.json" = "c5bc55a1345e5a1ec0563ba8d72447edfd0f2a41223081029ca0a15a58c367bc"
    "suites/architecture-center/profiles/ARC-05.json" = "0f084af9b81b4bc95877a5213a79e4ae485a5e9e83c55acc9acb8912aa2e998c"
    "suites/architecture-center/profiles/ARC-06.json" = "bad9f563a7c8c7beaad1fb8be5fae49c0fb3e15e2a0e82227f088a17627d070c"
    "suites/architecture-center/profiles/ARC-07.json" = "f43b4a930381cb2148cc734791183b93cd01f12262e624b4a17aa12b265eeef4"
    "suites/architecture-center/profiles/ARC-08.json" = "3978f85f2406eccd4998b88bbb8f7d8ec95d736a8765fb40bf9c659bbc89b0f0"
    "suites/architecture-center/profiles/ARC-09.json" = "85601c78059e60aa853b546d4c85fe51f111d8b81a4d27b026f69115010e05bd"
    "suites/architecture-center/profiles/ARC-10.json" = "a5b2dbbceacb4d8077ef6bce27228a1b4bac4249ba0e9300622ec43b33d7bdae"
    "suites/architecture-center/profiles/ARC-11.json" = "2029926f64c7687e08ca2f07739d8f0f7ba5f5a37bc36d9a0a63e07149aae36e"
    "suites/center-contracts/README.md" = "cb9ad41fab93b98c81b1e9f6db4117c8d4e5ae681d8abca90e2542dbf8c55041"
    "suites/center-contracts/matlab.json" = "340ec05b3ae44e27bc82aca6ed9cd694f30fac96aa6b58073da313c1e6cbce71"
    "suites/center-contracts/software.json" = "29ff2679ff5beb8d16b77238f6803e1979d7ccae0c148f7eacfdacfa09213012"
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
    "suites/intelligent-driving-center/STANDARD_SCORES.json" = "75b2c3b76e221d00bf567b22f4037b7cec0dc8e72ef0394f9ac2779157496e28"
    "suites/intelligent-driving-center/contract-index.json" = "a23c17970bdf0f5dfe18b58090c7d5d4021d77fc4f6b6adf64dc508f069cc395"
    "suites/intelligent-driving-center/evidence/IDC-01.json" = "3ad60626a96c12f34446625635a26402400a12d19089db9b0565f2c3e98b3da6"
    "suites/intelligent-driving-center/evidence/IDC-02.json" = "7b877645e6f3df390e91c5b250bcd6727aa868828e50584371d10c42bea87f9b"
    "suites/intelligent-driving-center/evidence/IDC-03.json" = "a0916c1cc792776c064f135ebac6a573eb0c420a46ef767432723699242c183c"
    "suites/intelligent-driving-center/evidence/IDC-04.json" = "f1a14740a8cb0dc102c80b7ab57500a552b9f854aa87e69da2bcfbdbef0957ae"
    "suites/intelligent-driving-center/evidence/IDC-05.json" = "eb4a63092159ea7ea42cc1f7e1245b97f6bcc50ce81f976b69657359347fb6ed"
    "suites/intelligent-driving-center/evidence/IDC-06.json" = "c3421c85392e33d6a46dd451594ceb97addabd17c70574e884e76656610a55b2"
    "suites/intelligent-driving-center/evidence/IDC-07.json" = "0c0c47ee1ae2092b529c78a900adde62235e2a93eb766bf661d7fc3ba94aee26"
    "suites/intelligent-driving-center/evidence/IDC-08.json" = "eb40fe1a5e096e31b052cb645609803f01d343555b2178035fcd9093dfa79b3b"
    "suites/intelligent-driving-center/evidence/IDC-09.json" = "fd75de3c45f277d3872884821d3cc0a69512696924954420a96a2851536089d4"
    "suites/intelligent-driving-center/evidence/IDC-10.json" = "32c788bc6f257565b3793297f6661f9cde5c6217b2e7ee4c6a8bfc6318311665"
    "suites/intelligent-driving-center/evidence/IDC-11.json" = "f1110bd5857534943f91881df6161c8b14a2d61fbad6c53e820e7e25cd0b4562"
    "suites/intelligent-driving-center/execution/IDC-01.json" = "cecb543c4ca930bf2426b770dd9a44f2eff2732e8bd144a56ef9f7b4719ce248"
    "suites/intelligent-driving-center/execution/IDC-02.json" = "5381e1dd3367581a07e32a4ed846cb59941964e2d481eff4a636f2ea5246d491"
    "suites/intelligent-driving-center/execution/IDC-03.json" = "855672760720a8a240ecc203c1f5178958c4c51c609d17465b6a12b004267b63"
    "suites/intelligent-driving-center/execution/IDC-04.json" = "7baa1e451c374e759a6daf2adc06a41c00e4a687ea73e8215fb3bdcae2f9a83b"
    "suites/intelligent-driving-center/execution/IDC-05.json" = "0a99638616ca53eb09e6749affab54f2522b1c781ed6c1eeda52e51cfa837e40"
    "suites/intelligent-driving-center/execution/IDC-06.json" = "ef1345383075e13c6a67df543661ffe9c5bf5af289bb45d8a7db1bc39dc731af"
    "suites/intelligent-driving-center/execution/IDC-07.json" = "54196752a33cb50c2d99828dc801adb55172b3e5ba248eabd5d6271660e7b816"
    "suites/intelligent-driving-center/execution/IDC-08.json" = "35de1801c1f91566175aa9fb052087f028186f272f7574a06da2730007511a88"
    "suites/intelligent-driving-center/execution/IDC-09.json" = "cffa6ac922039e55ebaf12152a507b40987bd4087d028c3aa0d853992d405d0c"
    "suites/intelligent-driving-center/execution/IDC-10.json" = "1bfa05b43636287114ffe2bea2fe53ed075ab2b481dfc15c08a8ec98d5285c24"
    "suites/intelligent-driving-center/execution/IDC-11.json" = "9296fbe35510f0f68eff2ecd90cf615d5200bdc37f736a3f5b1c54339804c40d"
    "suites/intelligent-driving-center/inventories/IDC-01.json" = "4b449b7c2da1c51033cb4905a4bba1a8753c3a80d2cc4104f51441464166e7be"
    "suites/intelligent-driving-center/inventories/IDC-02.json" = "cb5b6abc496e72b4b84035509b17c3a69a6767c71ad946523436b07c32f07d24"
    "suites/intelligent-driving-center/inventories/IDC-03.json" = "256fcbc7964180dd6d06c73485f7c9bc545cab755156836ed18d31dc725f1339"
    "suites/intelligent-driving-center/inventories/IDC-04.json" = "39a81d24ff21cd8556ca466906020e5ed37e743dd3e85f3fb6289100d6de8df7"
    "suites/intelligent-driving-center/inventories/IDC-05.json" = "7b1c94de24efb38f87624015642ab41e034005e0963c8b90b9a633bf8f8b8dd2"
    "suites/intelligent-driving-center/inventories/IDC-06.json" = "aa7eed12d9dd2659eddce6e7d0c09f35447aac466b34c63019b49c284a1efdb9"
    "suites/intelligent-driving-center/inventories/IDC-07.json" = "bcda97e2c6766c60bcfaedbf0221d8720dec6128e55d3f0b893826179eabb134"
    "suites/intelligent-driving-center/inventories/IDC-08.json" = "2588b7f8035eb2d5f98ebd4856b6f20a818c55e8d10ebcb753ae13a39407bff0"
    "suites/intelligent-driving-center/inventories/IDC-09.json" = "12e917f793f693d1ed082f7f7e6e06dfdf80b1c02c83296ee112a3bc3e0db0dc"
    "suites/intelligent-driving-center/inventories/IDC-10.json" = "12d462ee6675d7d9b97c1f1f53c64402b99273d61b9989df84b97a1c1b9dfe84"
    "suites/intelligent-driving-center/inventories/IDC-11.json" = "58eeebc26bdb85854e6a70ba607d6ee5def089005091ac690bd89bce2a312fd3"
    "suites/intelligent-driving-center/manifest.json" = "fad2d37114add0b703716a8716abcf12e08de857307fe79ac88d67c32ab59fa3"
    "suites/intelligent-driving-center/profiles/IDC-01.json" = "205e1b8e8f0fa6df02b3853df1217a315c2be58e31ddd4450202d6e812cdc793"
    "suites/intelligent-driving-center/profiles/IDC-02.json" = "b317653e02e77b1f052edc6e118704de01c5f277b855c88587c056475a05ae7a"
    "suites/intelligent-driving-center/profiles/IDC-03.json" = "4e80272c9f30b37db60de0625c6719378eff918c16f804829e642ae0b4883a47"
    "suites/intelligent-driving-center/profiles/IDC-04.json" = "03a12e5e6e340b574d8814f3025fdbd4eaea1266f1ac401a7a29789638c8079c"
    "suites/intelligent-driving-center/profiles/IDC-05.json" = "019db0a49a5f28ecb6c44c14d4c185bade732dac9bc422daea16e94535781c26"
    "suites/intelligent-driving-center/profiles/IDC-06.json" = "670601be5f9577df0447e0853777da73bac0c68d659c14456ebce6c7d699b45a"
    "suites/intelligent-driving-center/profiles/IDC-07.json" = "adec0f29465ab60f63b6eec08c31d57c17b620a729bc9c04235080aa092e0a3f"
    "suites/intelligent-driving-center/profiles/IDC-08.json" = "b35ec964e7aba5bf8595fca63800a2c807cdccad98b1f4d368e8e308698187c3"
    "suites/intelligent-driving-center/profiles/IDC-09.json" = "9c3152dd1e550c7314bbc55654340188707451d68a13d4caeb57c7a78032bbc3"
    "suites/intelligent-driving-center/profiles/IDC-10.json" = "a35973a91f5dafee93aeea9c9b8b7d1607705f5418d69ec8f7e20818ae2bdcb5"
    "suites/intelligent-driving-center/profiles/IDC-11.json" = "94c4475e9cd4278d3956bd3330853ec33e33ffde5a62a205f52e44cfa6086c72"
    "suites/legacy-v094.json" = "a1944ba5d6d8a5a5d58d1f3d7b270b26150cda56a165d12c3c9737df754cae5b"
    "suites/new-energy-matlab/cohorts.json" = "4371e0021ed3e7d522bd8a61ef35a9ca648ed82288075d101063c0b11bc7e6ff"
    "suites/new-energy-matlab/cohorts/reality-proxy-20260910/APPROVED_BUILD_CLARIFICATION.md" = "9519b6a56ba9834f8f2059ebfd4e7e16c612133a2002cf827888c63603ca150c"
    "suites/new-energy-matlab/cohorts/reality-proxy-20260910/EXECUTION.json" = "aa9c342a9b4a74647f23bc7efcff913e0ab1494c8a642f1c16caf0fe5189d28a"
    "suites/new-energy-matlab/cohorts/reality-proxy-20260910/LINEAGE.json" = "fec0da157bce79694e8f4c1ceb1de4debfc08406f0738872540e266e29336f67"
    "suites/new-energy-matlab/cohorts/reality-proxy-20260910/OBSERVATIONS.json" = "d7e4b9a33c763c49d53e32ebe190fbbdea905bf987a1e257f7dc835565228ec6"
    "suites/new-energy-matlab/cohorts/reality-proxy-20260910/PROFILE_COMPARISON.json" = "18ee922f110ff989527862d32178a3ad0e734c5d7f39fa6f90f8aca0695e019e"
    "suites/new-energy-matlab/cohorts/reality-proxy-20260910/README.md" = "1b96e9b27b61d0bd42cb32636b78162588d422f57a59318c4ebe6f5380333447"
    "suites/new-energy-matlab/cohorts/reality-proxy-20260910/SCORECARD.csv" = "0c13df69dc81bbc98c0a56360f84cc3a315f7206dbf1981384677d5a71f9b151"
    "suites/new-energy-matlab/cohorts/reality-proxy-20260910/SCORING_CONTRACT_PART7.md" = "2bc31dcbbb9c3cc2ea11686a9d3e3cde0225c6213107b92f771303efd059559b"
    "suites/new-energy-matlab/cohorts/reality-proxy-20260910/STANDARD_SCORES.json" = "66a4b83ea43afa962ce7cf3a28451440ab8b391cdbfefe0010094fe1600c3a2c"
    "suites/new-energy-matlab/cohorts/reality-proxy-20260910/contract-index.json" = "0e520a2a41904649c545164fdc8d37abff0588b6c5aa943e9f863c22525b389d"
    "suites/new-energy-matlab/cohorts/reality-proxy-20260910/manifest.json" = "a411922a2a0402164ca4037c4e7c495ca48bbf3abd6cdb49417d17f9e288d374"
    "verification/README.md" = "12ff137a9e25cbb11ecf87b2a99bf3d6217956bb51b6692c1ca7052c0f070bd5"
    "verification/boundary.py" = "9b9888b7e33b26ef4b65033d982099c413540074408ff81df0f6cbd34a59f384"
    "verification/calibration_census.py" = "0e53528399d8ff5448610e4f2492df00121a4ba71c49914b991b565c31d23e30"
    "verification/centers.py" = "ced5ab0e8e5c246a73358447c536c4175a2e0efa55bc7c8deffc9f5aae7e10cc"
    "verification/check_split.py" = "7a85129e20da6e5d52b07bf35ee244fd68305f9b122c9cb6478b07b1c37d1c8e"
    "verification/counting.py" = "01535dfe4097e289681ec0ab9f8d774cdfe11811c4d249c0050cbbee686ab9da"
    "verification/coverage.py" = "74876337d45bea4260ed60c94a00c6105464c05adff3e0df951d0d02a35a9392"
    "verification/evaluation_batch.py" = "2b1f826f034fd09032c7c4109a39f98a5da574929fc5e5d1278c91c9a699f5a9"
    "verification/evaluation_current.py" = "25e4c4ccbae6926c705abbf42ae5aad6d0fb36d353c390cb5e2079a321832687"
    "verification/evaluation_profile.py" = "bb7ee5bc285526adbebf22afaee3357e1ce0e7df6eba96f5ff6d0b208ff9797c"
    "verification/examples/build_boundary_prototypes.py" = "5c802e00142f1815b67271210f51b3dc824e3598e84027667b64f02a81794394"
    "verification/examples/current-assignments.json" = "3d245bd5adac1a8dbbfa70dc7545a4a5969490c1d1715ce662fd83997c115774"
    "verification/expansion.py" = "0dd4a109a8d77a0615313ac55ecd11ec8f68ca980ab560681b746661e5c210ff"
    "verification/external_inputs.py" = "54882587f5cad6dd75be0b5b1feca9ac3c4dbe252667bc3b17dffd654b232b5d"
    "verification/ne_reality.py" = "3c449793c0065ae13d04fb3c4247702e77ba14e09c86330cefc5ffd0ae44c47c"
    "verification/ne_reality_census.py" = "eefea52b506a17bc96aae73a9ffa4f856cb032757448f5fd5986f14e121ef7fe"
    "verification/ne_reality_restore.py" = "2d02474749ff9ceeaaf2294b88679582762133e071b1461c82922dfebf325a63"
    "verification/population_diagnostics.py" = "160548e91c2a9eb59dd7ca514d015f1d9bb43bb1682ada5b0cc236079cf15a90"
    "verification/reference_revisions.py" = "b300b9ba0c8daf3c672775f0934f11d182a9e8ce58208ec8ee6211d36cebcb9c"
    "verification/repository_types.py" = "f56ce1a0183eb7326b0f0910a3fca2a5726d888cad6f801298c4784d2d8db4f0"
    "verification/rules.py" = "f0936ed0d1bb7400f4f44985abdb23c41330e5593fe7ea08643dfd652b334c4d"
    "verification/semantic_audits.py" = "2a2ca58d25c77e583d61f832b72f666799564f290c90657daf4d4846521ca3b9"
    "verification/suites-v1.schema.json" = "e293769beb9b82de969bc8ede7cde568f5fd8c3c499375253af0d19840c67244"
    "verification/suites.py" = "5fee6daadc83bdaf5a88a49ec39cc55e37941940a9652658bc05c296e0ddd342"
    "verification/suites.schema.json" = "1fe2fd41cfa276344ab11e7cf9a6449649387e97d7a7ec2935124a5e1f1850d8"
    "verification/test_api_governance.py" = "b6dff09ba8cd6f0074e5faa9664f97604b78e8b8de90f1a2729288fa63f9c315"
    "verification/test_boundary_regression.py" = "a4237e27c9f627f2a5f807fe02e97149903e9db1c17c27a5992c84889cde83a2"
    "verification/test_calibration_census.py" = "9334b11434542bc99d00fa0d4e34df426e0f6e003695482f53411aacca570057"
    "verification/test_centers.py" = "a47e87b86d45fa8fe4f2742d02f10d1ac2955d2d6ea430a63d50d275e6aaad25"
    "verification/test_cpp_counting.py" = "79c6f3d34c6a8d20904f3f1747b440e56f728cf54820d93b9df06680000370a5"
    "verification/test_evaluation_batch.py" = "2e948b6d4517a931514423ece625cab27cfb92e4ea52a21a7b1871bb7896eea0"
    "verification/test_evaluation_current.py" = "65e6f1631f240b6c2d6ca501f89339646079445e64c3f29d690e9091a62d369d"
    "verification/test_evaluation_profile.py" = "b999aa7d419cf5e4738bb91de00ae14bb2d42f349f98f89c498810b2dd24a3b3"
    "verification/test_external_inputs.py" = "9c364f6e1d1a524681020430c8712ea392556015c81e4e02847f17435857a774"
    "verification/test_integration_execution.py" = "119e8df0701e4a110d4d13419ca864c90002deb238f843442aa1872f9257e492"
    "verification/test_lineage_split.py" = "a5ab7544a3bcfba9c80bef10238fa03713b07b9cf46d2845bd88db3ea3dedbb8"
    "verification/test_ne_reality.py" = "bb7bd9f9c6217d93cf7d12c8f046d95192ee4031ba761e5cb8ff2b1f2726d8d7"
    "verification/test_population_diagnostics.py" = "99b42825aebba750d5539411c9d02c35613e9fbfd4efc1d199274deb3dba14cc"
    "verification/test_public_verification.py" = "5ef960a5004a3228aa73356ae67746737d14970f048ff02bc81e8d516f11c6f4"
    "verification/test_public_verification_consistency.py" = "8100627a20dd4d5b51724209069bf5b5f3cdb719e55536fe99938aa2ebde83a8"
    "verification/test_reference_revisions.py" = "9c39b471dd82e9b17b6626c5688698c5f6fac5c65f2b3251251673853a92b0ed"
    "verification/test_repository_types.py" = "79e4a5f96161534b948dc6b3e60e03eeaa550fbe538471f9b9e3b70a10df1ece"
    "verification/test_rule_boundaries.py" = "9d61d0c5ce9a5fc20e8e38c63c8998fe136084b8d72855383792814484b12517"
    "verification/test_suites.py" = "5ec3a7c57ad717745012725acd46069008d6cc05772f9b419b55f7611c6fb3e8"
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
if ($registry.schema_version -in @('benchmark-repository-types-2','benchmark-reporting-groups-3') -or $Suite -ne 'android-validation18') {
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
