"""Recompute 135 contract leaves from facts, never from adopted scores/reasons.

Optional reviewed inputs: staging/validation18-realism-20260907/rule-inputs/NAME.json
{ "name": NAME, "head": SHA, "leaf_facts": { LEAF: { FACT: VALUE } },
  "evidence": { LEAF: [repository evidence objects] } }
Every supplied leaf override requires exact-HEAD repository evidence. Unknown
facts remain unresolved. Count objects may use {"minimum": N} only in >= gates;
absence/zero cannot be proved from a lower bound.
"""
import argparse
import configparser
import hashlib
import json
import math
import re
import subprocess
from pathlib import Path

APP=['camera-inspector','owner-handbook','climate-panel','market-distribution','podcast-player','launcher-workspace','navigation-map','system-settings','system-ui-shell']
FW=['network-stack-service','telecom-service','cell-broadcast-service','connectivity-service','telephony-service','bluetooth-service','wifi-service','car-services','platform-framework']
COMMON=['compilation.ci_independence','compilation.compilation_independence','compilation.api_version_management','platform_reuse.platform_upgrade','platform_reuse.release_branch_strategy']
ARCH=['architecture.componentization','architecture.decoupling','architecture.modularization']
MAX={'architecture.componentization':5,'architecture.decoupling':3,'architecture.modularization':3,'compilation.ci_independence':3,'compilation.compilation_independence':3,'compilation.api_version_management':3,'platform_reuse.platform_upgrade':10,'platform_reuse.release_branch_strategy':10,'quality.integration_test':3,'solid_principle.liskov_substitution':4}

class Missing(Exception):
    def __init__(self,keys): self.keys=keys

def need(f,*keys):
    missing=[k for k in keys if k not in f or f[k] is None]
    if missing:raise Missing(missing)
    return [f[k] for k in keys]

def atleast(value,n):
    if isinstance(value,dict):return True if value.get('minimum',-1)>=n else None
    if value is None:return None
    return isinstance(value,(int,float)) and value>=n

def gate(*items, operator='and'):
    """Three-valued AND/OR. Decisive false/true avoids invented unknown facts."""
    values=[v for _,v in items]
    decisive=False if operator=='and' else True
    if any(v is decisive for v in values):return decisive
    unknown=[key for key,value in items if value is None]
    if unknown:raise Missing(unknown)
    return True if operator=='and' else False

def positive(f,key):return (key,f.get(key))

def negative(f,key):
    value=f.get(key);return (key,None if value is None else not value)

def componentization(f):
    modules,=need(f,'module_count')
    if modules==1:
        return 1 if gate(*(positive(f,k) for k in ['has_layered_directory','has_business_packages','code_not_in_root_package']),operator='or') else 0
    if gate(('independently_buildable_cohesive_component_count',atleast(f.get('independently_buildable_cohesive_component_count'),2)),
            positive(f,'component_responsibilities_clear'),positive(f,'shared_capability_downshift_or_explicit_contract_reuse')):return 5
    packages,=need(f,'has_business_packages')
    if modules>=2 and packages:return 3
    layered,notroot=need(f,'has_layered_directory','code_not_in_root_package')
    return 1 if layered or notroot else 0

def decoupling(f):
    cycle,=need(f,'has_circular_dependency')
    if cycle:return 0
    unstable,=need(f,'core_mutually_coupled_without_stable_direction')
    if unstable:return 0
    many,boundaries=need(f,'multiple_direct_cross_boundary_or_propagation_violations','has_identifiable_boundaries')
    if many:return 1
    if gate(*(negative(f,k) for k in ['has_cross_module_source_intrusion','has_reverse_dependency','has_hardcoded_implementation_dependency']),
            *(positive(f,k) for k in ['shared_capability_downshift_or_injection','stable_dependency_direction','implementation_changes_do_not_require_unrelated_module_changes'])):return 3
    if boundaries and gate(*(positive(f,k) for k in ['has_cross_module_source_intrusion','has_reverse_dependency','has_hardcoded_implementation_dependency']),
                           negative(f,'shared_capability_downshift_or_injection'),operator='or'):return 2
    raise Missing(['explicit_boundary_adjudication_for_remaining_case'])

def modularization(f):
    cycle,modules=need(f,'has_circular_dependency','real_build_module_count')
    if cycle:return 0
    if modules==1:
        layered,packages=need(f,'has_layered_directory','has_business_packages')
        return 1 if layered or packages else 0
    named=f.get('standard_named_module_count')
    if gate(('standard_named_module_count',atleast(named,2)),('cohesive_module_count',atleast(f.get('cohesive_module_count'),3)),
            positive(f,'module_build_test_entry_or_clear_api_implementation_boundary')):return 3
    identifiable,=need(f,'module_responsibilities_identifiable')
    if modules>=2 and identifiable:return 2
    return 1

def ci(f):
    independent,platform=need(f,'valid_independent_ci_exists','valid_platform_ci_exists')
    if not independent:return 1 if platform else 0
    return 3 if gate(*(positive(f,k) for k in ['ci_has_real_build','ci_has_real_test','ci_has_quality_or_report','ci_steps_executable'])) else 2

def compilation(f):
    unclosed,local=need(f,'requires_platform_tree_or_undeclared_external_source','meaningful_independent_production_unit_exists')
    if unclosed and not local:return 0
    unversioned,=need(f,'full_build_requires_unversioned_platform_injection')
    if unversioned:return 1
    closed,declared,entry=need(f,'repository_source_module_closure_complete','external_dependencies_declared_interfaces','repeatable_module_build_entry')
    if not (closed and declared and entry):raise Missing(['external_build_closure_adjudication'])
    return 3 if gate(*(positive(f,k) for k in ['critical_cross_repo_api_versions_locked','real_compatibility_check_or_commitment','repeatable_or_hermetic_environment'])) else 2

def api(f):
    boundaries = api_governance_boundaries(f)
    critical = [b for b in boundaries if b['critical']]
    if critical and all(b['covered'] for b in critical):return 3
    semver,=need(f,'semantic_api_versioning')
    if type(semver) is not bool:raise Missing(['semantic_api_versioning must be boolean'])
    if semver or any(b['real_compatibility_check'] or b['fixed_external_responsibility_verified'] for b in critical):return 2
    version,=need(f,'manual_api_version_exists')
    if type(version) is not bool:raise Missing(['manual_api_version_exists must be boolean'])
    return 1 if version else 0


def api_governance_boundaries(f):
    """Validate reviewed scope and responsibility; never infer completeness.

    Source evidence is separately checked by verify.py. A valid record describes
    a mechanism, not a successful execution or independently proved semantics.
    """
    def require(value,message):
        if not value:raise Missing(['API governance: '+message])
    def string(value):return isinstance(value,str) and bool(value.strip())
    revision,governance=need(f,'evaluation_revision','api_governance')
    require(isinstance(revision,str) and re.fullmatch('[0-9a-f]{40}',revision),'invalid revision')
    require(isinstance(governance,dict),'inventory required')
    require(governance.get('revision')==revision,'stale inventory')
    require(governance.get('inventory_complete') is True and governance.get('unresolved')==[], 'scope or responsibility unresolved')
    require(string(governance.get('scope_basis')),'scope basis absent')
    boundaries=governance.get('boundaries')
    require(isinstance(boundaries,list) and bool(boundaries),'nonempty reviewed inventory required')
    ids=[]
    for b in boundaries:
        require(isinstance(b,dict),'invalid boundary')
        for key in ['id','type','owner','consumer','scope_basis','version_baseline','mechanism','coverage_reason']:
            require(string(b.get(key)),'empty '+key)
        ids.append(b['id'])
        require(b.get('role') in {'provided','consumed','internal'},'invalid role')
        for key in ['critical','owns_contract','covered','version_controlled','real_compatibility_check','fixed_external_responsibility_verified']:
            require(type(b.get(key)) is bool,'invalid '+key)
        require(isinstance(b.get('evidence'),list) and len(b['evidence'])>=2,'two source anchors required')
        if not b['critical']:
            require(not b['covered'] and not b['real_compatibility_check'] and not b['fixed_external_responsibility_verified'], 'excluded boundary claims coverage')
        if b['real_compatibility_check']:
            require(b['critical'] and b['version_controlled'],'compatibility check lacks version/criticality')
            require(string(b.get('current_binding')) and string(b.get('released_binding')),'current/released binding absent')
        if b['fixed_external_responsibility_verified']:
            require(not b['owns_contract'] and b['critical'] and b['version_controlled'],'invalid external responsibility')
            require(string(b.get('current_binding')) and string(b.get('released_binding')),'external version/commitment binding absent')
        if b['covered']:
            require(b['critical'] and b['version_controlled'] and
                    (b['real_compatibility_check'] or b['fixed_external_responsibility_verified']), 'unsupported full coverage')
            if b['owns_contract']:require(b['real_compatibility_check'],'owned contract needs actual extraction/diff')
    require(len(ids)==len(set(ids)),'duplicate boundaries')
    return boundaries

def integration(f):
    metrics = integration_execution_metrics(f)
    valid,=need(f,'valid_integration_assertions_and_interface_behavior')
    if type(valid) is not bool:raise Missing(['valid_integration_assertions_and_interface_behavior must be boolean'])
    if not valid:return 0
    if metrics is None:return 1
    rate, coverage = metrics
    if rate <= 0.5 or coverage < 0.5:return 1
    return 3 if rate==1 else 2


def integration_execution_metrics(f):
    """Validate declared execution and recompute ratios; report bytes checked by verify.

    Values describe retained evidence, not an execution performed by this rule.
    Host execution can validate real cross-component behavior under contract 3.5,
    but is never evidence of Android device/emulator execution.
    """
    def require(value, message):
        if not value:raise Missing(['integration execution: ' + message])
    def string(value):return isinstance(value,str) and bool(value.strip())
    def integer(value):return type(value) is int and value >= 0
    def digest(value, length):return isinstance(value,str) and re.fullmatch('[0-9a-f]{'+str(length)+'}',value) is not None
    def ratio(value, expected):
        return type(value) in (int,float) and math.isfinite(value) and math.isclose(value,expected,rel_tol=0,abs_tol=1e-12)
    # The Android-named flag is retained as a historical schema alias only.
    declared=f.get('final_head_integration_execution_exists',
                   f.get('final_head_android_integration_execution_exists'))
    execution=f.get('integration_execution')
    require(declared is None or type(declared) is bool,'execution flag must be boolean')
    if declared is not True:
        require(execution is None or execution == {} or execution == {'status':'not_run'},'execution record contradicts absent declaration')
        return None
    require(isinstance(execution,dict),'positive declaration needs a bound report')
    need(execution,'revision','mode','runtime','runtime_environment','runner','command',
         'status','objectives','expected_outcomes','tests_passed','tests_failed','tests_skipped','tests_total',
         'pass_ratio','coverage','artifacts','report_path','report_sha256')
    revision,=need(f,'evaluation_revision')
    require(digest(revision,40) and execution['revision']==revision,'evaluated revision differs')
    require(execution['mode'] in {'local','remote_ci'},'unknown execution mode')
    require(execution['runtime'] in {'android_device','android_emulator','host_jvm','host_native'},'unknown execution runtime')
    if execution['runtime'] in {'android_device','android_emulator'}:
        need(execution,'target_id','android_api','build_fingerprint')
        require(type(execution['android_api']) is int and execution['android_api']>0,'Android API is invalid')
        for key in ['target_id','build_fingerprint']:require(string(execution[key]),'empty '+key)
    for key in ['runtime_environment','runner','command','objectives','expected_outcomes','report_path']:
        require(string(execution[key]),'empty '+key)
    require(execution['status']=='completed','run must be complete')
    require(digest(execution['report_sha256'],64),'invalid report hash')
    counts=[execution[k] for k in ['tests_passed','tests_failed','tests_skipped','tests_total']]
    require(all(integer(v) for v in counts),'test counts must be nonnegative integers')
    passed,failed,skipped,total=counts
    require(total>0 and passed+failed+skipped==total,'test count denominator differs')
    pass_ratio=passed/total
    require(ratio(execution['pass_ratio'],pass_ratio),'test pass ratio differs')
    coverage=execution['coverage']
    require(isinstance(coverage,dict),'coverage object required')
    need(coverage,'name','definition','scope','all_edges','covered_edges','numerator','denominator','ratio','threshold')
    for key in ['name','definition','scope']:require(string(coverage[key]),'empty coverage '+key)
    def edge_set(edges):
        require(isinstance(edges,list),'interaction edges must be a list')
        require(all(isinstance(e,list) and len(e)==2 and all(string(x) for x in e) and e[0]!=e[1] for e in edges),'invalid cross-component edge')
        pairs={tuple(e) for e in edges}
        require(len(pairs)==len(edges),'duplicate interaction edges')
        return pairs
    all_edges=edge_set(coverage['all_edges']);covered=edge_set(coverage['covered_edges'])
    require(bool(all_edges) and covered <= all_edges,'covered edges not in nonempty complete scope')
    require(integer(coverage['numerator']) and integer(coverage['denominator'])
            and coverage['numerator']==len(covered) and coverage['denominator']==len(all_edges),'coverage numerator/denominator differs')
    coverage_ratio=len(covered)/len(all_edges)
    require(ratio(coverage['ratio'],coverage_ratio) and ratio(coverage['threshold'],0.5),'coverage ratio/contract threshold differs')
    require(isinstance(execution['artifacts'],list),'artifacts must be explicitly listed')
    paths=[]
    for artifact in execution['artifacts']:
        require(isinstance(artifact,dict),'invalid artifact')
        need(artifact,'path','sha256','kind','summary')
        require(all(string(artifact[k]) for k in ['path','kind','summary']) and digest(artifact['sha256'],64),'invalid artifact digest/summary')
        paths.append(artifact['path'])
    require(len(paths)==len(set(paths)) and execution['report_path'] not in paths,'duplicate/self-referential artifacts')
    if execution['mode']=='remote_ci':
        ci=execution.get('ci');require(isinstance(ci,dict),'remote CI binding required')
        need(ci,'provider','run_id','run_url','revision','workflow_path','workflow_blob','workflow_sha256','job_id','job_conclusion')
        for key in ['provider','run_id','run_url','workflow_path','job_id']:require(string(ci[key]),'empty CI '+key)
        require(ci['run_url'].startswith('https://') and ci['revision']==revision,'CI run/revision differs')
        require(digest(ci['workflow_blob'],40) and digest(ci['workflow_sha256'],64),'invalid workflow binding')
        require(ci['job_conclusion'] in {'success','failure'},'CI job is not complete')
    else:require(execution.get('ci') in (None,{}),'local run must not claim remote CI')
    for key,value in [('executed_test_pass_ratio',pass_ratio),('defined_key_interaction_coverage_ratio',coverage_ratio)]:
        if key in f:require(ratio(f[key],value),'legacy '+key+' disagrees with counts')
    if 'majority_tests_pass' in f:
        require(type(f['majority_tests_pass']) is bool and f['majority_tests_pass']==(pass_ratio>0.5),'legacy majority flag disagrees with counts')
    return pass_ratio,coverage_ratio

def passed_substitution_implementations(f):
    """Count executed passes, never test declarations. Missing proof cannot upgrade."""
    execution = f.get('substitution_execution')
    if not execution or execution.get('status') in {'not_run', 'failed'}:
        return 0, False
    required = ['revision', 'parent_symbol', 'command', 'tests_passed', 'tests_failed',
                'tested_implementations', 'passed_implementations', 'coverage', 'report_path', 'report_sha256']
    need(execution, *required)
    revision, children = need(f, 'evaluation_revision', 'child_symbols')
    if (execution.get('status') != 'passed' or execution['revision'] != revision
            or execution['parent_symbol'] != f['parent_symbol'] or not execution['command']
            or not isinstance(execution['tests_passed'], int) or execution['tests_passed'] <= 0
            or execution['tests_failed'] != 0):
        raise Missing(['valid final-revision substitution execution'])
    tested, passed = execution['tested_implementations'], execution['passed_implementations']
    if (not isinstance(tested, list) or not isinstance(passed, list) or not passed
            or len(set(passed)) != len(passed) or not set(passed) <= set(tested) <= set(children)
            or not execution['report_path'] or len(execution['report_sha256']) != 64):
        raise Missing(['bound production implementations and execution report'])
    systematic = all(execution['coverage'].get(k) is True for k in
                     ['exception', 'boundary', 'precondition', 'postcondition'])
    return len(passed), systematic

def lsp(f):
    parent,=need(f,'parent_symbol')
    if parent=='':return 'failed'
    if gate(*((k,atleast(f.get(k),1)) for k in ['empty_override_violation_count','unconditional_throw_violation_count','precondition_risk_count','postcondition_risk_count']),operator='or'):return 0
    unexplained,=need(f,'multiple_unexplained_override_or_exception_risks')
    if unexplained:return 1
    implementations,=need(f,'production_implementation_count')
    passed,systematic=passed_substitution_implementations(f)
    if isinstance(implementations,int) and implementations>=2 and passed==implementations and systematic:return 4
    if atleast(implementations,2) is True:return 3
    if atleast(implementations,1) is True and passed>=1:return 3
    if implementations==1:return 2
    return 'failed'

def platform(f):
    version=f.get('version_bound_status');arch=f.get('arch_bound_status')
    total=None if version is None or arch is None else version+arch
    if gate(positive(f,'single_abi_closed_dependency_without_fallback'),('version_bound_status+arch_bound_status',None if total is None else total>=5),
            positive(f,'multiple_unstable_core_paths_without_isolation'),positive(f,'permission_or_platform_hardcoding_blocks_core_migration'),operator='or'):return 0
    version,arch=need(f,'version_bound_status','arch_bound_status')
    noncompat=f.get('has_non_compatible_api');covered=f.get('non_compatible_api_all_covered')
    uncovered=False if noncompat is False or covered is True else True if noncompat is True and covered is False else None
    if gate(('has_non_compatible_api+non_compatible_api_all_covered',uncovered),positive(f,'has_complex_permission_adaptation'),
            ('version_bound_status',version>=2),('arch_bound_status',arch>=2),operator='or'):return 3
    noncompat,=need(f,'has_non_compatible_api')
    archspecific,=need(f,'has_arch_specific_deps')
    if not noncompat and not archspecific and version+arch<=1:
        if gate(positive(f,'has_interface_abstraction'),positive(f,'automated_compatibility_validation_at_least_two_android_versions'),operator='or'):return 10
    if not noncompat and not archspecific and version+arch<=3:return 8
    if gate(positive(f,'risks_all_localized_in_compat_layer'),positive(f,'risk_fallback_available'),('version_bound_status+arch_bound_status',version+arch<=3)):return 8
    return 3

def release(f):
    # Evidence may be same-version configurations/artifacts/tags on a single trunk.
    # Explicit False means reviewed absence; missing/None remains unresolved.
    # New records name the actual gate without implying that different trees
    # are mandatory. The legacy key is retained for frozen published inputs.
    key = ('release_policy_evidence_verified' if 'release_policy_evidence_verified' in f
           else 'ref_tree_differences_verify_release_policy')
    verified,=need(f,key)
    if type(verified) is not bool:raise Missing([key+' must be boolean'])
    if not verified:return 0
    vehicle,=need(f,'vehicle_specific_sop_channel')
    if vehicle:return 3
    platform_shared,=need(f,'platform_shared_release_channel')
    if platform_shared:return 8
    unified,=need(f,'cross_platform_unified_release_policy')
    if unified:return 10
    return 0

RULES=dict(zip(ARCH,[componentization,decoupling,modularization]))
RULES.update(dict(zip(COMMON,[ci,compilation,api,platform,release])))
RULES.update({'quality.integration_test':integration,'solid_principle.liskov_substitution':lsp})

# Reference inventory for reviewers supplying missing facts. This is not a set of
# required fields for every branch: each rule requests only its decisive gates.
INPUT_KEYS={
 'architecture.componentization':['module_count','has_layered_directory','has_business_packages','code_not_in_root_package','independently_buildable_cohesive_component_count','component_responsibilities_clear','shared_capability_downshift_or_explicit_contract_reuse'],
 'architecture.decoupling':['has_circular_dependency','core_mutually_coupled_without_stable_direction','multiple_direct_cross_boundary_or_propagation_violations','has_identifiable_boundaries','has_cross_module_source_intrusion','has_reverse_dependency','has_hardcoded_implementation_dependency','shared_capability_downshift_or_injection','stable_dependency_direction','implementation_changes_do_not_require_unrelated_module_changes'],
 'architecture.modularization':['has_circular_dependency','real_build_module_count','standard_named_module_count','cohesive_module_count','module_build_test_entry_or_clear_api_implementation_boundary','module_responsibilities_identifiable','has_layered_directory','has_business_packages'],
 'compilation.ci_independence':['valid_independent_ci_exists','valid_platform_ci_exists','ci_has_real_build','ci_has_real_test','ci_has_quality_or_report','ci_steps_executable'],
 'compilation.compilation_independence':['requires_platform_tree_or_undeclared_external_source','meaningful_independent_production_unit_exists','full_build_requires_unversioned_platform_injection','repository_source_module_closure_complete','external_dependencies_declared_interfaces','repeatable_module_build_entry','critical_cross_repo_api_versions_locked','real_compatibility_check_or_commitment','repeatable_or_hermetic_environment'],
 'compilation.api_version_management':['evaluation_revision','api_governance','semantic_api_versioning','manual_api_version_exists'],
 'quality.integration_test':['valid_integration_assertions_and_interface_behavior','final_head_integration_execution_exists','final_head_android_integration_execution_exists','evaluation_revision','integration_execution','majority_tests_pass','defined_key_interaction_coverage_ratio','executed_test_pass_ratio'],
 'solid_principle.liskov_substitution':['parent_symbol','child_symbols','overridden_methods','empty_override_violation_count','unconditional_throw_violation_count','precondition_risk_count','postcondition_risk_count','multiple_unexplained_override_or_exception_risks','production_implementation_count','substitution_test_count','systematic_contract_tests_cover_exception_boundary_pre_post','evaluation_revision','substitution_execution'],
 'platform_reuse.platform_upgrade':['version_bound_status','arch_bound_status','single_abi_closed_dependency_without_fallback','multiple_unstable_core_paths_without_isolation','permission_or_platform_hardcoding_blocks_core_migration','has_non_compatible_api','non_compatible_api_all_covered','has_complex_permission_adaptation','has_arch_specific_deps','has_interface_abstraction','automated_compatibility_validation_at_least_two_android_versions','risks_all_localized_in_compat_layer','risk_fallback_available'],
 'platform_reuse.release_branch_strategy':['current_head_refs','vehicle_specific_sop_channel','platform_shared_release_channel','cross_platform_unified_release_policy','ref_tree_differences_verify_release_policy']}


def semantic_rule(facts):
    if not facts.get('scope_sufficient'):
        return None,['scope_sufficient: '+facts['observation']]
    extent=facts.get('violation_extent')
    if extent=='severe':return 0,[]
    if extent=='multiple':return 1,[]
    if extent=='localized' and facts.get('positive_conformance_observed'):return 2,[]
    if extent=='none_observed' and facts.get('positive_conformance_observed'):
        if facts.get('exceptional_automotive_practice_demonstrated') is True:return 4,[]
        if facts.get('exceptional_automotive_practice_demonstrated') is False:return 3,[]
    return None,['violation_extent/positive_conformance_observed/exceptional_automotive_practice_demonstrated']
