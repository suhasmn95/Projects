# C+2 - A New Programming Language

Hi there,

Thank you for visiting my GitHub profile! If you're in this folder, it means you're seeing my latest work-in-progress for a new language that I call **C+2**. I am currently in the phase of developing the **lexer** and **parser** modules, and it's exciting to share this journey with you.

## About C+2

C+2 is a programming language designed with simplicity in mind, while retaining all the powerful features of C++. The goal is to create a language that is easy to read, write, and maintain, while resolving some of the complexities found in traditional C++.

## Current Features

As of now, the **lexer** and **parser** are working in the following ways:

- **Lexer (Tokenizer)**:
  - Identifies and tokenizes various components of the source code, including:
    - **Keywords** (e.g., `fn`, `let`, `return`, `println`)
    - **Identifiers** (e.g., function names, variable names)
    - **Data types** (e.g., `int`, `void`)
    - **Operators** (e.g., `+`, `-`, `->`)
    - **Delimiters** (e.g., `;`, `:`, `,`, `()`)
  - Converts the source code into a list of tokens that can be parsed further.

- **Parser**:
  - Supports basic function declaration and parsing, including:
    - Function name
    - Function parameters with types (e.g., `a: int`, `b: int`)
    - Return type (e.g., `-> int`, `-> void`)
    - Function body (currently parsing the function declaration structure, but empty body is parsed for now)
  - Example: 
    ```plaintext
    fn add(a: int, b: int) -> int:
        return a + b;
    ```

## Example Usage

Here's how you can run the lexer and parser:

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/cplus2.git
   cd cplus2
2. Run the lexer and parser on a sample source code:
   ```bash
   python CPlus2_Interpreter/Test.py
The output will tokenize the source code and parse the function definitions. Example output:
   ```bash
   Token(KEYWORD, 'fn')
   Token(IDENTIFIER, 'add')
   Token(DELIMITER, '(')
   Token(IDENTIFIER, 'a')
   Token(DELIMITER, ':')
   Token(DATATYPE, 'int')
   Token(DELIMITER, ',')
   Token(IDENTIFIER, 'b')
   Token(DELIMITER, ':')
   Token(DATATYPE, 'int')
   Token(DELIMITER, ')')
   Token(OPERATOR, '-')
   Token(OPERATOR, '>')
   Token(DATATYPE, 'int')
   Token(DELIMITER, ':')
   Token(KEYWORD, 'return')
   Token(IDENTIFIER, 'a')
   Token(OPERATOR, '+')
   Token(IDENTIFIER, 'b')
   Token(DELIMITER, ';')

After parsing, the result will be an abstract representation of the functions defined:
   ```bash
   [{'name': 'add', 'parameters': [('a', 'int'), ('b', 'int')], 'return_type': 'int', 'body': []}]

## Future Plans
  - Implement parsing for the **function body**, such as **return statements** and **expressions**.
  - Add **execution logic** to evaluate parsed expressions and function calls.
  - Improve **error handling** and edge cases for better robustness.
  - Expand the language features, including loops, conditionals, and more.

## Contributing
Feel free to contribute if you have suggestions, improvements, or bug fixes. Please fork the repository, make your changes, and submit a pull request.


