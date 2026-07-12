import ast

class ASTSecurityVerifier(ast.NodeVisitor):
    def __init__(self):
        super().__init__()
        self.is_safe = True
        self.error_message = ''
        # Strict allowlist of modules for algebraic evaluation
        self.allowed_modules = {'numpy', 'math'}
        self.banned_functions = {'eval', 'exec', 'open', 'compile', '__import__', 'os', 'sys'}

    def visit_Import(self, node):
        for alias in node.names:
            base_module = alias.name.split('.')[0]
            if base_module not in self.allowed_modules:
                self.is_safe = False
                self.error_message = f"Forbidden module import: '{alias.name}'. Allowed: {self.allowed_modules}"
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        base_module = node.module.split('.')[0] if node.module else ''
        if base_module not in self.allowed_modules:
            self.is_safe = False
            self.error_message = f"Forbidden module import source: 'from {node.module} ...'."
        self.generic_visit(node)

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            if node.func.id in self.banned_functions:
                self.is_safe = False
                self.error_message = f"Forbidden security bypass function invocation: '{node.func.id}'"
        self.generic_visit(node)

    @classmethod
    def verify_code(cls, code_str: str) -> tuple[bool, str]:
        try:
            tree = ast.parse(code_str)
            verifier = cls()
            verifier.visit(tree)
            return verifier.is_safe, verifier.error_message
        except SyntaxError as se:
            return False, f"Python Static SyntaxError before sandbox execution: {str(se)}"