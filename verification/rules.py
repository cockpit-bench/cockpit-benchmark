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
    if gate(positive(f,'api_version_controlled'),positive(f,'real_public_api_or_abi_compatibility_diff')):return 3
    semver,=need(f,'semantic_api_versioning')
    if semver:return 2
    version,=need(f,'manual_api_version_exists')
    return 1 if version else 0

def integration(f):
    valid,=need(f,'valid_integration_assertions_and_interface_behavior')
    if not valid:return 0
    executed,=need(f,'final_head_android_integration_execution_exists')
    if not executed:return 1
    if not gate(positive(f,'majority_tests_pass'),('defined_key_interaction_coverage_ratio',atleast(f.get('defined_key_interaction_coverage_ratio'),0.5))):return 1
    rate,=need(f,'executed_test_pass_ratio')
    return 3 if rate==1 else 2

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
    verified,=need(f,'ref_tree_differences_verify_release_policy')
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
 'compilation.api_version_management':['api_version_controlled','real_public_api_or_abi_compatibility_diff','semantic_api_versioning','manual_api_version_exists'],
 'quality.integration_test':['valid_integration_assertions_and_interface_behavior','final_head_android_integration_execution_exists','majority_tests_pass','defined_key_interaction_coverage_ratio','executed_test_pass_ratio'],
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
