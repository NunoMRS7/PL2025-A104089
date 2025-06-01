class ASTNode:
    def __init__(self, value: str | None = None, children=None):
        self.value = value
        self.children = list(children) if children else []

    def __repr__(self):
        return f"ASTNode({self.value}, {self.children})"