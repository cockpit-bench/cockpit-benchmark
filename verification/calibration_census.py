"""Deterministic calibration expression census, including Stateflow guards.

This records expressions, not whether a number is a business calibration.
Reviewers still distinguish thresholds, enumerations and algorithm constants.
No model, script, callback or target code is executed.
"""
import re
import zipfile
import io
import xml.etree.ElementTree as ET
from suites import git, sha

FIELDS = {'Value', 'Gain', 'Threshold', 'InitialValue', 'InitialCondition',
          'FixedStep', 'SampleTime', 'DelayLength', 'UpperLimit', 'LowerLimit',
          'UpperSaturationLimit', 'LowerSaturationLimit', 'Numerator', 'Denominator',
          'BreakpointsForDimension1', 'Table', 'maxIndex', 'minIndex'}


def xml_expressions(body, member):
    tree = ET.fromstring(body)
    rows = []
    for node in tree.iter():
        if node.tag not in {'Block', 'state', 'transition', 'Object'}:
            continue
        for prop in node.findall('P'):
            key = prop.get('Name')
            if key in FIELDS or (node.tag in {'state', 'transition'} and key == 'labelString'):
                expression = prop.text or ''
                if expression.strip():
                    rows.append({'member': member, 'node_type': node.tag,
                                 'id': node.get('SID', node.get('SSID', node.get('ObjectID'))),
                                 'name': node.get('Name'), 'field': key,
                                 'expression': expression})
        if node.tag == 'state':
            for prop in node.findall('eml/P'):
                if prop.get('Name') == 'script' and prop.text:
                    rows.append({'member': member, 'node_type': 'state', 'id': node.get('SSID'),
                                 'name': node.get('Name'), 'field': 'script', 'expression': prop.text})
    return rows


def census(repo, scope):
    result = {'schema': 'calibration-expression-census-v1',
              'head': git('-C', repo, 'rev-parse', 'HEAD'), 'scope': scope,
              'models': [], 'scripts': [],
              'limits': 'Expression inventory only; business meaning, active configuration and parameter completeness require semantic review.'}
    for name in scope['models']:
        body = git('-C', repo, 'show', 'HEAD:' + name, binary=True)
        expressions = []
        with zipfile.ZipFile(io.BytesIO(body)) as z:
            for member in sorted(z.namelist()):
                if member.endswith('.xml') and member.startswith('simulink/'):
                    expressions.extend(xml_expressions(z.read(member), member))
        result['models'].append({'path': name, 'sha256': sha(body), 'expressions': expressions})
    for name in scope['scripts']:
        body = git('-C', repo, 'show', 'HEAD:' + name, binary=True)
        assignments = []
        for line, text in enumerate(body.decode('utf-8-sig').splitlines(), 1):
            if re.match(r'\s*[A-Za-z]\w*(?:\.\w+)*\s*=', text):
                assignments.append({'line': line, 'text': text.strip()})
        result['scripts'].append({'path': name, 'sha256': sha(body), 'assignments': assignments})
    return result
