[CmdletBinding()]
# After a network interruption: ./restore.ps1 -Destination <same-directory> -Resume
param([Parameter(Mandatory=$true)][ValidateNotNullOrEmpty()][string]$Destination, [switch]$Resume, [switch]$IncludeSubmodules, [ValidateSet("app","fw","new-energy-matlab","android-validation18","matlab-simulink","all")][string]$Suite = "all", [string]$SourceMap, [string[]]$RepositoryIds)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$expectedHashes = [ordered]@{
    ".gitattributes" = "5550472b34249d85a794952825db528251956dd8bfff9dd17589ea767446f588"
    ".gitignore" = "6feaded4e28ea86e001a6751b4e3d960e8b7c31b9616ff9936b79297086e809b"
    "ACTIVE_EIGHTEEN.md" = "f64d70be58fea89e65d152c839f8e47a386f5e5db8c43ec81cda6008ad35881b"
    "LICENSE" = "950f20ff178debfcf2526200837304a7512f39c022dc1f9105a6e0af62788df0"
    "NOTICE" = "ff71f002bf010747ebc6a65858605d93e07bdbf19e2514ea0bab67f6e8bb1420"
    "README.md" = "54186589c915a5eb7b1155a0fac9ffc324a6db05f40784c7282677325f82745e"
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
    "docs/CURRENT_EVALUATION.md" = "ff651526ca969addb52498a970b021f9e749e32ba5f088633d1a561a9b55dd66"
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
    "docs/REAL_REPOSITORY_GUIDANCE.md" = "862ad8541dccc85dd6c752aeb1c1645f5a4dfc6389c38158985945ef8a1b3051"
    "docs/REVIEW_FIXES.md" = "601899e42f1da145fb60929efffdc4e70c0a9d1205a9cf9aac99a9b7dd535cb2"
    "docs/REVIEW_FOLLOWUP.md" = "1d1469abacb96bb11e8431c4ab07341b316ad4a88fb854b1b1798774ea946cc5"
    "docs/REVIEW_V0101.md" = "a4721327e6e04cbd068fb26f798099db4c1550c75cf29a5bbf1548c3ed1f8e01"
    "docs/REVIEW_V0102.md" = "7303b50f20a88795aa03a4bc3b1edc6d9696bdd3c233856229c679dd0d389081"
    "docs/RULE_FIXES.md" = "2eac51b7ddc3877d9cf309e948af300a089e3ed416ba41a1919818fbb4abc154"
    "docs/SOLID_CALIBRATION.md" = "c7523cdfc750052f12eb970f0db0b3f7286107727ecc5bf5d31be05e3382ec64"
    "docs/SOLID_CALIBRATION_V092.md" = "da7fd301095cd10dcbc5acc2263272f3811902599bbeef2b24938feda8b4aa6e"
    "docs/VERIFICATION_INPUTS.md" = "fde1e48faa97f29733d9d2260fb870eec53fb616128ab467cd9ce04bb4b3949c"
    "docs/WEB_REVIEW.md" = "d6f07e22a0bf46497276d77c04465727db9e5b8fa481e35be9aa06aaf12e5e2c"
    "docs/boundary-candidates.json" = "373a07b7fe67e5f76e023b088399f3dddb83c4e701aeae1661b31e40121ae228"
    "docs/boundary-reference.json" = "ec56264242213590a570f0e42d5bca470dd6c377c86fd6176ad066bcb883b088"
    "docs/compilation-calibration-v092.json" = "1edd4098b31321ae15dfed98ee08cc040ff3aaf223730876138c9baa339ba765"
    "docs/contract-sensitivity.json" = "6fa28378d96fe470869c569be64951d77ab91920fc21563426d9898099caea55"
    "docs/current-distribution.json" = "a795955e5ad6227120c0415f8fe4c37d6aaadcf14618b666f47ffaad8ce7e996"
    "docs/current-evaluation-summary.json" = "ab883ea778db3f0099b5aa8bcefd120b341e1c133de04bc56ad7e47bf9b6f6f0"
    "docs/current-evaluation.json" = "9df2433ea4bb152dd0d0a23e373fae0aa02b3a3a702b4534f9bd21100e460940"
    "docs/evaluation-context.json" = "d31b289210347f996ad0744c3cef08c49a362494c482e6808eb5ad0cfc49e1ee"
    "docs/evidence-availability.json" = "5cdca5b0f3e0bcee18120a25c09f67ba34bb945ba305d5b9c31ebb1a0dbd4478"
    "docs/horizontal-arbitration-v093.json" = "e97da2b11fe4045af768e7ffe73d51a061a5e9513c2d20d13be1322c980ab899"
    "docs/map-ocp-arbitration-v094.json" = "ed69b0f08dd73eb0d14b54d6ad1106d0cdece6218400a54612be08ece73e1f9d"
    "docs/population-diagnostics.json" = "62b3584263325d057d4f579b6102d3076ae9caa4abf56b0b97446d75a0d5abb6"
    "docs/review-v0101/NEM-10-parameter-scope.json" = "e312fc9a00904bf3da4aa3722eb5d95443ab1ec9d650328b34e1160d23183c40"
    "docs/review-v0101/NEM-11-reuse-scope.json" = "b61e8a78d19fb402bd612708db0ccb0e1b016fecc77230db249efd101dbdff45"
    "docs/review-v0102/NEM-10-acquisition.json" = "0c25f7e99ec25abde52f78a602a5ae9d8e8125cebec172cfe52f1f014f246918"
    "docs/review-v0102/NEM-10-comparison.json" = "4f235c43259bcc3739047a033526decf4fe9594b3f80596a4a8fe1a0354a472d"
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
    "suites.json" = "ead8b71d3189da36eb0436649a692a54213f4d9a109fbf4d01e57801d0a916ac"
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
    "suites/legacy-v094.json" = "fadc09b820c9781b3eb1575737301f049d75dfe99375a6ad5c92062664cea911"
    "suites/matlab-simulink/DATASET_LIMITS.json" = "12b2a775b1c2563b298b620fb422f0ba69b7091f99ef3a02e909b7806b3aad4f"
    "suites/matlab-simulink/DATASET_LIMITS.md" = "f3de5bd55e52d1852b52488ede2b204ad2c124d48de360d22199939bf5e64605"
    "suites/matlab-simulink/EFFECTIVE_CONTRACT.md" = "36f75b2b79416d227c0f0538573774067e6ef4fa096e3272df88bb3439495665"
    "suites/matlab-simulink/EVIDENCE_INDEX.json" = "9f3815129808034b9eb7905bba7fde443b23805cbc4559331066711fead036f6"
    "suites/matlab-simulink/PUBLIC_RESTORE.json" = "d8b62c284e5147e200ef555249d7e855c52d3a1113f43a3848dc55c09690d9b9"
    "suites/matlab-simulink/README.md" = "01249a7e23ca096dfee76e5eaf6acac96c7e8124c20e1ca82c82cd63efdffd39"
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
    "suites/matlab-simulink/oracle/ML-09.json" = "85f720482680eb5748ed443dbadaa388c1c13ee6579c2268fd524c27ca47aca6"
    "suites/new-energy-matlab/SCORECARD.md" = "a6809c4f519d57c0bf459e89bc21ea24a862e7c3a2687db3e4cfbf9ea23a3183"
    "suites/new-energy-matlab/STANDARD_SCORES.json" = "572cd408913d24b8d174301b9697fa0583db35d8b4cbc9474ae54aae9899350e"
    "suites/new-energy-matlab/additions.json" = "6cb445b94581736ea9898a66eb9fc2b43d7b35cd3b46dc340910c40801cf04aa"
    "suites/new-energy-matlab/evidence/NEM-10-source.json" = "07f142e97185c0768392c3b627611ab43e49f42a02ea662cd66024f386643d20"
    "suites/new-energy-matlab/evidence/NEM-10.json" = "72456e7ed19edead8219e5830de257fed3b5535f02354f5e6969baae12fa8d96"
    "suites/new-energy-matlab/evidence/NEM-11-source.json" = "5d1de30a247c3759a3d5326f8bdd9be52f07ca8a3d3971310e21be96b1c133b5"
    "suites/new-energy-matlab/evidence/NEM-11.json" = "a7b66abaf61747b2a7428ea1960fdfaa8b87ecd9a347830ebe19d3048bbbb25a"
    "suites/new-energy-matlab/manifest.json" = "b35a07d754eaeb13797eeeaeac8a445663911b21360aa787152f27775d0604a6"
    "verification/README.md" = "12ff137a9e25cbb11ecf87b2a99bf3d6217956bb51b6692c1ca7052c0f070bd5"
    "verification/boundary.py" = "9b9888b7e33b26ef4b65033d982099c413540074408ff81df0f6cbd34a59f384"
    "verification/check_split.py" = "7a85129e20da6e5d52b07bf35ee244fd68305f9b122c9cb6478b07b1c37d1c8e"
    "verification/counting.py" = "01535dfe4097e289681ec0ab9f8d774cdfe11811c4d249c0050cbbee686ab9da"
    "verification/coverage.py" = "74876337d45bea4260ed60c94a00c6105464c05adff3e0df951d0d02a35a9392"
    "verification/effective_contract.py" = "1c25ad2920ad49fca83b968f76036f3df70461a57a5b1520fde9ec3693b3afa5"
    "verification/evaluation_batch.py" = "2b1f826f034fd09032c7c4109a39f98a5da574929fc5e5d1278c91c9a699f5a9"
    "verification/evaluation_current.py" = "d9edbcfbe74a77c544f249db6fbd0f5f8be298d7bb91350b1a497e3a6db73bd3"
    "verification/evaluation_profile.py" = "8ab808d05a4106d913d127ff2e9f67210ff3d6d53acacd18f6aa33cc233b7ad5"
    "verification/examples/build_boundary_prototypes.py" = "5c802e00142f1815b67271210f51b3dc824e3598e84027667b64f02a81794394"
    "verification/examples/current-assignments.json" = "fbd504cd7284bbc0f54dbe0948fbba61aac0568cd107a0cf48a256efd3156e02"
    "verification/expansion.py" = "420926c56d3e1a90c31d439b5fb6205a322e50b4a6ee8ca37caa5a050b471c42"
    "verification/external_inputs.py" = "54882587f5cad6dd75be0b5b1feca9ac3c4dbe252667bc3b17dffd654b232b5d"
    "verification/matlab_evidence.py" = "2488ab60fbff3505161c49ea1c54aa148c3493dd64f3089c95b16a89bc69f894"
    "verification/matlab_properties.py" = "066d12dc74dfaf6ede617a32d6bcc9903f1c371e45198ce4a83a848101802c5f"
    "verification/matlab_recompute.py" = "4c040c2b634e0ca10794c8aaedb908f581ec9a35462aa0517c39c5d3d65bc0df"
    "verification/matlab_validators.py" = "99fabdd335fc4d873f1b269979710dc9faaff316ccdcc2bb2fe0a921dc7c7ef8"
    "verification/population_diagnostics.py" = "84476a032787a799f70746adc92b83b2f3182d49849d315dd58e86bdb9693ccc"
    "verification/reference_revisions.py" = "b300b9ba0c8daf3c672775f0934f11d182a9e8ce58208ec8ee6211d36cebcb9c"
    "verification/repository_types.py" = "6e7b9a79344952ecc13a4a523ac58a9b9eb1e2b0af32b76ab3100bde5923fb22"
    "verification/rules.py" = "f0936ed0d1bb7400f4f44985abdb23c41330e5593fe7ea08643dfd652b334c4d"
    "verification/semantic_audits.py" = "2a2ca58d25c77e583d61f832b72f666799564f290c90657daf4d4846521ca3b9"
    "verification/suites-v1.schema.json" = "e293769beb9b82de969bc8ede7cde568f5fd8c3c499375253af0d19840c67244"
    "verification/suites.py" = "efe6a054e0cb5c6c0ca0a59ae1c7b11673521c205f37291c9bed41b389488fbb"
    "verification/suites.schema.json" = "0e7abd73038b2e17f94de2c51e5d0984ff23589a415f442ff9b1c2d806202cbf"
    "verification/test_api_governance.py" = "b6dff09ba8cd6f0074e5faa9664f97604b78e8b8de90f1a2729288fa63f9c315"
    "verification/test_boundary_regression.py" = "a4237e27c9f627f2a5f807fe02e97149903e9db1c17c27a5992c84889cde83a2"
    "verification/test_cpp_counting.py" = "79c6f3d34c6a8d20904f3f1747b440e56f728cf54820d93b9df06680000370a5"
    "verification/test_effective_contract.py" = "6e4b6dda8be6e2bc13a1d05b12b0e3f7baf16877ef282572464574096f2486c0"
    "verification/test_evaluation_batch.py" = "2e948b6d4517a931514423ece625cab27cfb92e4ea52a21a7b1871bb7896eea0"
    "verification/test_evaluation_current.py" = "7793ee7707cf4c7e9971d061ad6517fe1b397b90569557a223dfa3bbc11cfc02"
    "verification/test_evaluation_profile.py" = "b999aa7d419cf5e4738bb91de00ae14bb2d42f349f98f89c498810b2dd24a3b3"
    "verification/test_external_inputs.py" = "9c364f6e1d1a524681020430c8712ea392556015c81e4e02847f17435857a774"
    "verification/test_integration_execution.py" = "119e8df0701e4a110d4d13419ca864c90002deb238f843442aa1872f9257e492"
    "verification/test_lineage_split.py" = "a5ab7544a3bcfba9c80bef10238fa03713b07b9cf46d2845bd88db3ea3dedbb8"
    "verification/test_matlab_evidence.py" = "996f6168f4e27d1af9d52670f61fb3a3c6775891d0bf7f39d6405bb30cdb6aba"
    "verification/test_population_diagnostics.py" = "9df4a96ad82eb12b24fd4f871ec230db4607385fce9a88db95309f010530470c"
    "verification/test_public_verification.py" = "5ef960a5004a3228aa73356ae67746737d14970f048ff02bc81e8d516f11c6f4"
    "verification/test_public_verification_consistency.py" = "8100627a20dd4d5b51724209069bf5b5f3cdb719e55536fe99938aa2ebde83a8"
    "verification/test_reference_revisions.py" = "96a769122a8b5a85fe2a5ca99deda32ef40e4173dee13c248913739e96bf09a7"
    "verification/test_repository_types.py" = "6a5f3b295fb0a4ccd2d6dc0c4fe5aa886315d4abc51dcca2d85f621074576baa"
    "verification/test_rule_boundaries.py" = "9d61d0c5ce9a5fc20e8e38c63c8998fe136084b8d72855383792814484b12517"
    "verification/test_suites.py" = "77464d95e44e130ee7ccf3bb9dedf77a9b0cf36615f7245a614e5ff0b604c52d"
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
