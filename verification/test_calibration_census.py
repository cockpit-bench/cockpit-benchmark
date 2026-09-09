import unittest
from calibration_census import xml_expressions


class CalibrationCensusTests(unittest.TestCase):
    def test_guard_changes_are_visible_even_when_stateflow_counts_do_not_change(self):
        source = '<chart><transition SSID="48"><P Name="labelString">[Vbus &gt;= 0.95*Vpack]</P><P Name="position">1 2 3 4</P></transition></chart>'
        before = xml_expressions(source, 'simulink/stateflow/chart_119.xml')
        changed = xml_expressions(source.replace('0.95', '0.90'), 'simulink/stateflow/chart_119.xml')
        self.assertNotEqual(before, changed)
        self.assertEqual(before[0]['id'], '48')
        self.assertEqual(before[0]['expression'], '[Vbus >= 0.95*Vpack]')
        self.assertEqual(before, xml_expressions(source.replace('1 2 3 4', '5 6 7 8'), 'simulink/stateflow/chart_119.xml'))

    def test_block_initial_values_and_configured_timing_are_not_omitted(self):
        source = '<root><Block SID="39" Name="Charge"><P Name="InitialValue">48*0.985</P></Block><Object ObjectID="2"><P Name="FixedStep">0.1</P></Object></root>'
        rows = xml_expressions(source, 'simulink/configSet0.xml')
        self.assertEqual([r['field'] for r in rows], ['InitialValue', 'FixedStep'])
        self.assertEqual([r['expression'] for r in rows], ['48*0.985', '0.1'])

    def test_embedded_matlab_function_is_part_of_parameter_review(self):
        source='<chart><state SSID="1"><eml><P Name="script">function x=f(speed)\nx=speed&lt;1;\nend</P><P Name="editorLayout">123</P></eml></state></chart>'
        rows=xml_expressions(source,'simulink/stateflow/chart_13.xml')
        self.assertEqual(len(rows),1)
        self.assertEqual((rows[0]['id'],rows[0]['field']),('1','script'))
        self.assertIn('speed<1',rows[0]['expression'])


if __name__ == '__main__': unittest.main()
