import sys

from gen import gen_code
from ana_sin import parse_pascal
from ana_sem import SemanticAnalyzer


if __name__ == "__main__":
    texto = sys.stdin.read()
    ast_root = parse_pascal(texto)
    SemanticAnalyzer().analyze(ast_root)
    # print(f"\nTree:\n{ast_root}\n\n")
    print(f"{gen_code(ast_root)}")
