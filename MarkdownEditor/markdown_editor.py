import markdown
import bleach
import re

class MarkdownEditor:
    def __init__(self):
        self.md = markdown.Markdown(extensions=[
            'markdown.extensions.fenced_code',
            'markdown.extensions.tables',
            'markdown.extensions.nl2br',
            'markdown.extensions.sane_lists',
            'markdown.extensions.codehilite',
            'markdown.extensions.meta',
            'markdown.extensions.toc'
        ])
        
        # Cấu hình cho bleach (HTML sanitizer)
        self.allowed_tags = [
            'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
            'strong', 'em', 'del', 'ul', 'ol', 'li',
            'code', 'pre', 'blockquote', 'a', 'img',
            'table', 'thead', 'tbody', 'tr', 'th', 'td',
            'br', 'hr', 'div', 'span'
        ]
        
        self.allowed_attributes = {
            'a': ['href', 'title'],
            'img': ['src', 'alt', 'title'],
            'code': ['class'],
            'pre': ['class'],
            '*': ['class']
        }

    def convert_to_html(self, markdown_text):
        """Convert markdown text to safe HTML"""
        try:
            # Convert markdown to HTML
            html = self.md.convert(markdown_text)
            
            # Sanitize HTML
            clean_html = bleach.clean(
                html,
                tags=self.allowed_tags,
                attributes=self.allowed_attributes,
                strip=True
            )
            
            return clean_html
        except Exception as e:
            raise Exception(f"Error converting markdown: {str(e)}")

    def get_toc(self, markdown_text):
        """Generate table of contents"""
        try:
            self.md.convert(markdown_text)
            if hasattr(self.md, 'toc'):
                return self.md.toc
            return ""
        except Exception as e:
            raise Exception(f"Error generating TOC: {str(e)}")

    def validate_markdown(self, markdown_text):
        """Validate markdown syntax"""
        try:
            # Basic validation rules
            errors = []
            
            # Check unclosed code blocks
            code_blocks = re.findall(r'```.*?```', markdown_text, re.DOTALL)
            if markdown_text.count('```') % 2 != 0:
                errors.append("Unclosed code block detected")
            
            # Check unmatched brackets
            if markdown_text.count('[') != markdown_text.count(']'):
                errors.append("Unmatched square brackets")
            
            # Check unmatched parentheses in links
            if markdown_text.count('(') != markdown_text.count(')'):
                errors.append("Unmatched parentheses")
            
            return len(errors) == 0, errors
            
        except Exception as e:
            raise Exception(f"Error validating markdown: {str(e)}") 