import sys

from ana_sin import parse_pascal


if __name__ == "__main__":
    texto = sys.stdin.read()
    result = parse_pascal(texto)
    print(f"\nTree:\n{result}\n\n")