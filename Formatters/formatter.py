import json
from bs4 import BeautifulSoup
import jsbeautifier
import cssbeautifier
from yapf.yapflib.yapf_api import FormatCode

class CodeFormatter:
    def __init__(self):
        # Cấu hình cho các formatter
        self.js_options = {
            'indent_size': 2,
            'indent_char': ' ',
            'max_preserve_newlines': 2,
            'preserve_newlines': True,
            'keep_array_indentation': False,
            'break_chained_methods': False,
            'indent_scripts': 'normal',
            'space_before_conditional': True,
            'unescape_strings': False,
            'jslint_happy': False,
            'end_with_newline': True,
            'wrap_line_length': 80,
            'indent_inner_html': False,
            'comma_first': False,
            'e4x': False
        }
        
        self.css_options = {
            'indent': '  ',
            'openbrace': 'end-of-line',
            'autosemicolon': True
        }

    def format_json(self, content):
        try:
            parsed = json.loads(content)
            return json.dumps(parsed, indent=2)
        except Exception as e:
            raise Exception(f"Invalid JSON: {str(e)}")

    def format_html(self, content):
        try:
            soup = BeautifulSoup(content, 'html.parser')
            return soup.prettify()
        except Exception as e:
            raise Exception(f"Invalid HTML: {str(e)}")

    def format_javascript(self, content):
        try:
            return jsbeautifier.beautify(content, self.js_options)
        except Exception as e:
            raise Exception(f"Invalid JavaScript: {str(e)}")

    def format_css(self, content):
        try:
            return cssbeautifier.beautify(content, self.css_options)
        except Exception as e:
            raise Exception(f"Invalid CSS: {str(e)}")

    def format_python(self, content):
        try:
            formatted_code, _ = FormatCode(content)
            return formatted_code
        except Exception as e:
            raise Exception(f"Invalid Python code: {str(e)}") 