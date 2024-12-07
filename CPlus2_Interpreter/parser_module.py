class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_pos = 0
        self.current_token = self.tokens[self.current_pos] if self.tokens else None

    def advance(self):
        """Advance to the next token."""
        self.current_pos += 1
        self.current_token = self.tokens[self.current_pos] if self.current_pos < len(self.tokens) else None

    def consume(self, token_type):
        """Consume a token of the expected type."""
        if self.current_token and self.current_token.type == token_type:
            token = self.current_token
            self.advance()
            return token
        else:
            raise ValueError(f"Expected token type {token_type}, but got {self.current_token}")

    def parse_program(self):
        """Parse the entire program."""
        statements = []

        while self.current_token:
            # Parse function definitions (fn)
            if self.current_token.type == 'KEYWORD' and self.current_token.value == 'fn':
                statements.append(self.parse_function())
            else:
                self.advance()  # Move to the next token if not a function

        return statements

    def parse_function(self):
        """Parse a function definition."""
        self.consume('KEYWORD')  # 'fn'
        function_name_token = self.consume('IDENTIFIER')  # Function name
        function_name = function_name_token.value

        self.consume('DELIMITER')  # '('
        parameters = self.parse_parameters()  # Function parameters
        self.consume('DELIMITER')  # ')'

        self.consume('OPERATOR')  # '-'
        self.consume('OPERATOR')  # '>'
        return_type_token = self.consume('DATATYPE')  # Return type
        return_type = return_type_token.value

        self.consume('DELIMITER')  # ':'
        statements = self.parse_statements()  # Function body

        return {
            'name': function_name,
            'parameters': parameters,
            'return_type': return_type,
            'body': statements
        }

    def parse_parameters(self):
        """Parse function parameters."""
        parameters = []

        # Loop until we encounter the closing parenthesis ')'
        while self.current_token and (self.current_token.type != 'DELIMITER' or self.current_token.value != ')'):
            # First, we expect an IDENTIFIER (parameter name)
            if self.current_token.type == 'IDENTIFIER':
                param_name_token = self.consume('IDENTIFIER')  # Expecting the parameter name
                param_name = param_name_token.value

                # Next, we expect a colon ':' delimiter
                self.consume('DELIMITER')  # ':'

                # Then, we expect a DATATYPE (e.g., 'int', 'float')
                param_type_token = self.consume('DATATYPE')  # Expecting 'int', 'float', etc.
                param_type = param_type_token.value

                parameters.append((param_name, param_type))

                # If we encounter a comma, skip it to continue to the next parameter
                if self.current_token and self.current_token.type == 'DELIMITER' and self.current_token.value == ',':
                    self.advance()  # Skip over the comma
            else:
                raise ValueError(f"Unexpected token in parameter list: {self.current_token}")

        return parameters

    def parse_statements(self):
        """Parse statements inside the function body."""
        statements = []

        while self.current_token and self.current_token.type != 'KEYWORD' and self.current_token.value != 'fn':
            if self.current_token.type == 'KEYWORD' and self.current_token.value == 'return':
                statements.append(self.parse_return_statement())
            elif self.current_token.type == 'KEYWORD' and self.current_token.value == 'let':
                statements.append(self.parse_declaration())
            else:
                self.advance()  # Skip over unknown tokens for now

        return statements

    def parse_return_statement(self):
        """Parse return statement."""
        self.consume('KEYWORD')  # 'return'
        expression = self.parse_expression()
        self.consume('DELIMITER')  # ';'
        return {'type': 'return', 'expression': expression}

    def parse_declaration(self):
        """Parse variable declarations."""
        self.consume('KEYWORD')  # 'let'
        var_name_token = self.consume('IDENTIFIER')
        var_name = var_name_token.value

        self.consume('DELIMITER')  # ':'
        var_type_token = self.consume('DATATYPE')
        var_type = var_type_token.value

        self.consume('OPERATOR')  # '='
        value = self.parse_expression()

        self.consume('DELIMITER')  # ';'
        return {'type': 'declaration', 'name': var_name, 'data_type': var_type, 'value': value}

    def parse_expression(self):
        """Parse expressions (simple for now, could be expanded)."""
        if self.current_token.type == 'IDENTIFIER':
            return self.consume('IDENTIFIER').value
        elif self.current_token.type == 'INTEGER':
            return int(self.consume('INTEGER').value)
        else:
            raise ValueError(f"Unexpected token in expression: {self.current_token}")
