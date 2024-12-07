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
