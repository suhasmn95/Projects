from lexer import Lexer
from parser_module import Parser  # or from parser_module import Parser if you renamed parser.py

source_code = """
fn add(a: int, b: int) -> int:
    return a + b;

fn main() -> void:
    let result: int = add(10, 20);
    println(result);
"""

lexer = Lexer(source_code)

tokens = lexer.tokenize()
for token in tokens:
    print(token)
parser = Parser(tokens)
program = parser.parse_program()

print(program)
