import re

class Token:
    def __init__(self, token_type, value):
        self.type = token_type
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {repr(self.value)})"


class Lexer:
    def __init__(self, source_code):
        self.source_code = source_code
        self.tokens = []
        self.current_pos = 0

    def advance(self):
        """Move to the next character in the source code."""
        self.current_pos += 1

    def current_char(self):
        """Return the current character."""
        if self.current_pos < len(self.source_code):
            return self.source_code[self.current_pos]
        return None

    def add_token(self, token_type, value):
        """Add a token to the list of tokens."""
        self.tokens.append(Token(token_type, value))

    def tokenize(self):
        """Tokenize the source code."""
        while self.current_pos < len(self.source_code):
            char = self.current_char()

            # Skip whitespace
            if char in ' \t\n\r':
                self.advance()

            # Handle keywords, identifiers, and data types
            elif char.isalpha():
                start_pos = self.current_pos
                while self.current_char() and self.current_char().isalnum():
                    self.advance()
                value = self.source_code[start_pos:self.current_pos]
                if value in ['fn', 'let', 'return', 'println']:  # Keywords
                    self.add_token('KEYWORD', value)
                elif value in ['int', 'float', 'double', 'bool','void']:  # Data types
                    self.add_token('DATATYPE', value)
                else:  # Identifiers
                    self.add_token('IDENTIFIER', value)

            # Handle numbers (integers)
            elif char.isdigit():
                start_pos = self.current_pos
                while self.current_char() and self.current_char().isdigit():
                    self.advance()
                value = self.source_code[start_pos:self.current_pos]
                self.add_token('INTEGER', value)

            # Handle delimiters (like ':', ',', ';', '(', ')')
            elif char in ':,();':
                self.add_token('DELIMITER', char)
                self.advance()

            # Handle operators (+, -, *, /, >, <-, =, ->)
            elif char in '+-*/':
                self.add_token('OPERATOR', char)
                self.advance()

            # Handle assignment operator '='
            elif char == '=':
                self.add_token('OPERATOR', '=')
                self.advance()

            # Handle function return type arrow (->)
            elif char == '-' and self.current_char() == '>':
                self.add_token('OPERATOR', '->')
                self.advance()  # Skip the '>' character
                self.advance()  # Skip the '-' character

            # Handle '>' as a standalone operator
            elif char == '>':
                self.add_token('OPERATOR', '>')
                self.advance()

            else:
                raise ValueError(f"Unknown character: {char}")

        return self.tokens
