"""C++ lexical regressions, not a substitute for a compiler/preprocessor."""
from pathlib import Path
import sys
import unittest

root = Path(__file__).resolve().parents[1] / 'scripts/verification'
sys.path.insert(0, str(root if root.exists() else Path(__file__).resolve().parent))
from counting import count_production_lines, strip_c_like_comments


class CppCountingTests(unittest.TestCase):
    def check(self, source, expected):
        for language in ['C++', '.cpp', '.cc', 'C++ header', 'C/C++ header', '.hpp']:
            with self.subTest(language=language):
                masked = strip_c_like_comments(source, language=language)
                self.assertEqual(count_production_lines(source, language=language)[0], expected)
                self.assertEqual(len(masked), len(source))
                self.assertEqual([i for i,c in enumerate(masked) if c in '\r\n'],
                                 [i for i,c in enumerate(source) if c in '\r\n'])

    def test_numeric_separators_do_not_swallow_comments(self):
        for literal in ['30000', "30'000", "0xAB'CD", "0b1010'0011", "1.234'567e+10", ".123'456", "42'000ULL"]:
            self.check(f'constexpr auto value = {literal};\n// comment only\n/* comment only */\nconstexpr int answer = 7;\n', 2)

    def test_character_literals_are_not_numbers(self):
        self.check("char value = '3';\nchar slash = '/';\nchar quote = '\\'';\n// removed\nint value3 = 7;\n", 4)

    def test_raw_string_keeps_quotes_and_comment_text(self):
        self.check('constexpr auto text = R"tag(first\n" // literal content\n/* still literal */\n)tag";\nconstexpr int answer = 7;\n', 5)

    def test_raw_prefixes_and_exact_delimiters(self):
        for prefix in ['R','u8R','uR','UR','LR']:
            self.check(f'auto text = {prefix}"edge(\n)other" // literal\n\\" /* literal */\n)edge"; // comment\n// removed\nint result = 1;\n', 5)
        self.check('auto text = R"(quote " and /* literal */)";\n// removed\nint result = 1;\n', 2)

    def test_raw_markers_inside_comments_and_strings_are_ignored(self):
        self.check('// R"bad(unclosed\n/* u8R"bad(unclosed */\nconst char* a = "R\\\"bad(";\nint result = 1;\n', 2)

    def test_adjacent_literals_and_identifier_digits(self):
        self.check('const char* a = "" "// literal";\nint id30 = 1;\nchar c = \'0\';\n// removed\n', 3)

    def test_crlf_offsets_and_delimiter_length(self):
        self.check('auto value = R"abcdefghijklmnop(\r\n" // literal\r\n)abcdefghijklmnop";\r\n// removed\r\n', 3)

    def test_unclosed_raw_literal_fails_instead_of_guessing(self):
        with self.assertRaisesRegex(ValueError, 'Unterminated C\\+\\+'):
            strip_c_like_comments('auto text = R"x(unclosed', language='C++')


if __name__ == '__main__':
    unittest.main()
