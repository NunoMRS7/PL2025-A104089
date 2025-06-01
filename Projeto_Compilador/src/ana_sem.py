from AST.tree import ASTNode

class SemanticAnalyzer:
    def __init__(self):
        # Global symbol table: var_name -> var_type (e.g. "integer", "boolean", or ("array", element_type, lower_bound, upper_bound))
        self.global_vars = {}
        # Function/procedure table: 
        # name -> {"params": [("paramName", type), …], "return_type": type or None for procedures, "defined": True}
        self.functions = {}
        # A small set of built‐in (predefined) procedures/functions, if any. Add more as needed.
        # Format: name -> {"params": [type, type, …], "return_type": type or None}
        self.builtins = {
            # Example builtins (Pascal "writeln" / "write" accept any, skip strict check)
            "writeln": {"params": [], "return_type": None},
            "write": {"params": [], "return_type": None},
            "readln": {"params": [], "return_type": None},
            "read": {"params": [], "return_type": None},
            "length": {"params": ["string"], "return_type": "integer"},
        }

        # A stack of local scopes: each scope is a dict var_name -> var_type
        self.scopes = []

    def error(self, message: str):
        """Raise a semantic error immediately."""
        raise ValueError(message)

    def lookup_var(self, name: str):
        """Look up a variable in the current scope stack (local → … → global)."""
        # Check local scopes first (top of stack to bottom)
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        # Then check global
        if name in self.global_vars:
            return self.global_vars[name]
        return None

    def add_var(self, name: str, var_type):
        """Add a variable to the current (topmost) scope."""
        if not self.scopes:
            # We are at global level
            if name in self.global_vars:
                self.error(f"Variable '{name}' is already declared in global scope.")
            self.global_vars[name] = var_type.lower()
        else:
            # At least one local scope exists
            current = self.scopes[-1]
            if name in current:
                self.error(f"Variable '{name}' is already declared in this local scope.")
            current[name] = var_type.lower()

    def add_function(self, name: str, param_list: list, return_type):
        """Register a function or procedure in the global function table."""
        if name in self.functions or name in self.builtins:
            self.error(f"Function/Procedure '{name}' is already declared.")
        self.functions[name] = {
            "params": param_list.copy(),  # list of (paramName, paramType)
            "return_type": return_type,   # string type or None for procedures
            "defined": True
        }

    def analyze(self, root: ASTNode):
        """Entry point: expect root to be ASTNode("program", [...])."""
        if not isinstance(root, ASTNode) or root.value != "program":
            self.error("Semantic analyzer expects root node 'program'.")
        # children: [programName (str), OptionalVarList (ASTNode or None),
        #            ASTNode("functionlist", [funcNodes…]), ASTNode("main", …)]
        _, optionalVarList, funcListNode, mainNode = root.children
        # 1) Process global variables
        if optionalVarList is not None:
            self._process_varsection(optionalVarList, is_global=True)

        # 2) Process all function/procedure signatures (without descending bodies yet)
        #    funcListNode is ASTNode("functionlist", [funcElem1, funcElem2, …])
        for funcElem in funcListNode.children:
            if funcElem.value == "function":
                # children: [FuncDefinition ASTNode("functionid",[funcName, paramsNode]), returnType (str), OptionalVarList, FunctionBody]
                func_id_node, return_type_str, optVarList, body = funcElem.children
                func_name = func_id_node.children[0]  # str
                params_node = func_id_node.children[1]  # ASTNode("params", [pairNodes …]) or empty
                param_list = self._extract_param_list(params_node)
                self.add_function(func_name, param_list, return_type_str)
            elif funcElem.value == "procedure":
                # children: [FuncDefinition ASTNode("functionid",[procName, paramsNode]), OptionalVarList, FunctionBody]
                proc_id_node, optVarList, body = funcElem.children
                proc_name = proc_id_node.children[0]  # str
                params_node = proc_id_node.children[1]  # ASTNode("params", [pairNodes …]) or empty
                param_list = self._extract_param_list(params_node)
                self.add_function(proc_name, param_list, None)
            else:
                self.error(f"Unknown function list element '{funcElem.value}' in semantic phase.")

        # 3) Now descend each function/procedure body to type‐check
        for funcElem in funcListNode.children:
            if funcElem.value == "function":
                func_id_node, return_type_str, optVarList, body = funcElem.children
                func_name = func_id_node.children[0]
                param_list = self.functions[func_name]["params"]
                self._enter_scope()
                # 3a) Insert all parameters into local scope
                for pname, ptype in param_list:
                    self.add_var(pname, ptype)
                self.add_var(func_name, return_type_str)
                # 3b) Insert local vars if any
                if optVarList is not None:
                    self._process_varsection(optVarList, is_global=False)
                # 3c) Check function body
                bodies = body.children  # a list of ASTNode for statements
                for stmt in bodies:
                    self._visit_statement(stmt)
                # (Optional) You can add a check here that the function's return_value is assigned
                # to a variable named exactly func_name (Pascal‐style). That requires knowing where the return occurs.
                self._leave_scope()
            else:  # procedure
                proc_id_node, optVarList, body = funcElem.children
                proc_name = proc_id_node.children[0]
                param_list = self.functions[proc_name]["params"]
                self._enter_scope()
                for pname, ptype in param_list:
                    self.add_var(pname, ptype)
                if optVarList is not None:
                    self._process_varsection(optVarList, is_global=False)
                bodies = body.children
                for stmt in bodies:
                    self._visit_statement(stmt)
                self._leave_scope()

        # 4) Finally, check the 'main' block
        # mainNode: ASTNode("main", [OptionalVarList, ASTNode("body", [...])])
        mainOptVars, mainBody = mainNode.children
        self._enter_scope()
        if mainOptVars is not None:
            self._process_varsection(mainOptVars, is_global=False)
        for stmt in mainBody.children:
            self._visit_statement(stmt)
        self._leave_scope()
        # If we reach here with no errors, semantic pass succeeded.

    def _enter_scope(self):
        """Push a new local symbol table."""
        self.scopes.append({})

    def _leave_scope(self):
        """Pop the current local symbol table."""
        self.scopes.pop()

    def _extract_param_list(self, params_node: ASTNode):
        """
        Given ASTNode("params", [pairNodes …]), return a list of (paramName, paramTypeStr).
        If params_node has no children (empty), return [].
        """
        if params_node is None or not isinstance(params_node, ASTNode):
            return []
        assert params_node.value == "params"
        result = []
        for pairNode in params_node.children:
            # pairNode: ASTNode("pair", [paramNameStr, typeNameStr])
            if not isinstance(pairNode, ASTNode) or pairNode.value != "pair":
                self.error("Semantic: expected 'pair' node in param list.")
            param_name = pairNode.children[0]     # string
            param_type = pairNode.children[1]     # string
            result.append((param_name, param_type))
        return result

    def _process_varsection(self, varSectionNode: ASTNode, is_global: bool):
        """
        varSectionNode: ASTNode("varsection", [varNode1, varNode2, ...])
        Each varNode: ASTNode("var", [ASTNode("varIds", [idStr, ...]), varTypeNode])
        varTypeNode: either a string (type name) or ASTNode("array", [indexesNode, elementTypeStr])
        Record each declared variable in the appropriate scope.
        """
        assert varSectionNode.value == "varsection"
        for varNode in varSectionNode.children:
            # varNode: ASTNode("var", [ ASTNode("varIds", [id1, id2, …]), varType ])
            ids_node = varNode.children[0]
            var_type_node = varNode.children[1]
            # Determine the type:
            if isinstance(var_type_node, ASTNode) and var_type_node.value == "array":
                # Children: [indexesNode, elementTypeStr]
                indexes_node = var_type_node.children[0]
                elem_type = var_type_node.children[1]  # string
                # indexes_node: ASTNode("arrayindexes", [lowerBoundInt, upperBoundInt])
                if indexes_node is None or not isinstance(indexes_node, ASTNode):
                    self.error("Semantic: malformed array indexes.")
                lower = indexes_node.children[0]
                upper = indexes_node.children[1]
                if not isinstance(lower, int) or not isinstance(upper, int):
                    self.error("Semantic: array bounds must be integer constants.")
                var_type = ("array", elem_type, lower, upper)
            else:
                # var_type_node should be a string naming a basic type
                var_type = var_type_node.lower()
            # Now assign this type to each identifier under ASTNode("varIds")
            assert isinstance(ids_node, ASTNode) and ids_node.value == "varIds"
            for id_str in ids_node.children:
                if not isinstance(id_str, str):
                    self.error("Semantic: variable name is not a string.")
                if is_global:
                    if id_str in self.global_vars:
                        self.error(f"Variable '{id_str}' already declared globally.")
                    self.global_vars[id_str] = var_type
                else:
                    # Use add_var to put into current local scope
                    self.add_var(id_str, var_type)

    def _visit_statement(self, node):
        """
        Dispatch based on the type of statement:
         - ASTNode("Atrib", [varNode, exprNode])
         - ASTNode("for", [initAssign, toOrDownto, limitExpr, bodyNode])
         - ASTNode("if", [condExpr, thenBodyNode, elseBodyNode or None])
         - ASTNode("while", [condExpr, bodyNode])
         - Or it might be a bare expression (e.g. a function call as statement)
         - Or it might be a nested ASTNode("body", …). We handle that too.
        """
        if isinstance(node, ASTNode):
            if node.value == "Atrib":
                self._visit_assignment(node)
            elif node.value == "for":
                self._visit_for(node)
            elif node.value == "if":
                self._visit_if(node)
            elif node.value == "while":
                self._visit_while(node)
            elif node.value == "body":
                # A nested block: simply walk all children
                for stmt in node.children:
                    self._visit_statement(stmt)
            else:
                # Maybe it's a bare Factor or expression statement
                # e.g. a function call used as a statement.
                self._visit_expression(node)
        else:
            # It's likely a literal (int, str, bool) or a variable name alone; no effect
            pass

    def _visit_assignment(self, node: ASTNode):
        """
        node: ASTNode("Atrib", [ ASTNode("Var", [idStr, optionalArraySuffix]), exprNode ])
        """
        var_node = node.children[0]
        expr_node = node.children[1]

        # var_node is ASTNode("Var", [idStr, possible ArraySuffix ASTNode or None])
        if not isinstance(var_node, ASTNode) or var_node.value != "Var":
            self.error("Semantic: malformed variable node in assignment.")
        var_name = var_node.children[0]
        suffix_node = var_node.children[1]  # either ASTNode representing array suffixes or None

        var_type = self.lookup_var(var_name)
        if var_type is None:
            self.error(f"Use of undeclared variable '{var_name}'.")

        # If suffix_node exists: it should be ASTNode for array indexing
        if suffix_node is not None:
            # suffix_node likely came from grammar: array suffix list in LHS, but grammar wraps indexes in ASTNode("array suffix list", …)
            # For simplicity, treat it as “we are indexing an array”
            if (not isinstance(var_type, tuple) or var_type[0] != "array") and (var_type != "string"):
                self.error(f"Variable '{var_name}' is not an array but used with indexing.")
            # Check each index inside suffix_node.children: they are expression nodes
            for idx_expr in suffix_node.children:
                idx_type = self._visit_expression(idx_expr)
                if idx_type != "integer":
                    self.error(f"Indexing array '{var_name}' with non-integer expression.")
            # The LHS type now is the element type of the array
            lhs_type = var_type[1]
        else:
            # Simple scalar variable
            if isinstance(var_type, tuple) and var_type[0] == "array":
                self.error(f"Array '{var_name}' used without index in assignment.")
            lhs_type = var_type

        # Evaluate RHS expression type
        rhs_type = self._visit_expression(expr_node)

        # Check type compatibility (Pascal usually requires exact type match for assignment)
        if lhs_type != rhs_type:
            self.error(f"Type mismatch in assignment to '{var_name}': left is '{lhs_type}', right is '{rhs_type}'.")

    def _visit_for(self, node: ASTNode):
        """
        node: ASTNode("for", [initAssign, 'to'/'downto', limitExpr, bodyNode])
        - initAssign is itself an ASTNode("Atrib", …)
        - limitExpr is an expression
        - bodyNode is either ASTNode("body", …) or a single statement
        """
        if len(node.children) != 4:
            self.error("Semantic: malformed FOR statement.")
        init_assign = node.children[0]
        limit_expr = node.children[2]
        body_node = node.children[3]

        # Check the initialization assignment
        self._visit_assignment(init_assign)

        # For loops in Pascal expect the variable to be integer
        # Extract the loop variable from init_assign
        loop_var_node = init_assign.children[0]
        loop_var_name = loop_var_node.children[0]
        loop_var_type = self.lookup_var(loop_var_name)
        if loop_var_type is None:
            self.error(f"Use of undeclared loop variable '{loop_var_name}'.")
        if loop_var_type != "integer":
            self.error(f"Loop variable '{loop_var_name}' must be of type integer, not '{loop_var_type}'.")

        # Check the limit expression type
        lim_type = self._visit_expression(limit_expr)
        if lim_type != "integer":
            self.error("FOR loop limit expression must be integer.")

        # Now visit the body (new nested scope not needed; loop does not introduce new vars)
        if isinstance(body_node, ASTNode) and body_node.value == "body":
            for stmt in body_node.children:
                self._visit_statement(stmt)
        else:
            self._visit_statement(body_node)

    def _visit_if(self, node: ASTNode):
        """
        node: ASTNode("if", [condExpr, thenBodyNode, elseBodyNode or None])
        """
        if len(node.children) < 2:
            self.error("Semantic: malformed IF statement.")
        cond_expr = node.children[0]
        then_body = node.children[1]
        else_body = node.children[2] if len(node.children) == 3 else None

        cond_type = self._visit_expression(cond_expr)
        if cond_type != "boolean":
            self.error("IF condition must be boolean.")

        # Then‐block
        if isinstance(then_body, ASTNode) and then_body.value == "body":
            for stmt in then_body.children:
                self._visit_statement(stmt)
        else:
            self._visit_statement(then_body)

        # Else‐block, if present
        if else_body is not None:
            if isinstance(else_body, ASTNode) and else_body.value == "body":
                for stmt in else_body.children:
                    self._visit_statement(stmt)
            else:
                self._visit_statement(else_body)

    def _visit_while(self, node: ASTNode):
        """
        node: ASTNode("while", [condExpr, bodyNode])
        """
        if len(node.children) != 2:
            self.error("Semantic: malformed WHILE statement.")
        cond_expr = node.children[0]
        body_node = node.children[1]

        cond_type = self._visit_expression(cond_expr)
        if cond_type != "boolean":
            self.error("WHILE condition must be boolean.")

        # Visit body
        if isinstance(body_node, ASTNode) and body_node.value == "body":
            for stmt in body_node.children:
                self._visit_statement(stmt)
        else:
            self._visit_statement(body_node)

    def _visit_expression(self, node):
        """
        Recursively determine the type of an expression AST. Possible node types:
          - int literal (Python int) → "integer"
          - str literal (Python str) → "string" or variable reference (disambiguate by lookup)
          - bool literal (Python bool) → "boolean"
          - ASTNode with operators: "AND", "OR", "NOT", comparators "GT"/"LT"/"EQ"/"GTE"/"LTE", "+", "-", "*", "div", "mod"
          - ASTNode("Factor", [Primary, ASTNode("suffix list", …)])
          -  Primary = ASTNode leaf: either int, string, bool, or identifier (string, but treat as variable reference)
        Returns the inferred type (one of "integer", "boolean", "string") or raises SemanticError.
        """
        # 1) If it is a plain Python literal (leaf):
        if isinstance(node, int):
            return "integer"
        if isinstance(node, bool):
            return "boolean"
        if isinstance(node, str):
            # Could be either a string literal (if it came from p_primary_string) or an identifier.
            # We assume that during parsing, string literals are quoted or flagged differently.
            # If it’s in the var table, it’s a variable reference:
            var_type = self.lookup_var(node)
            if var_type is not None:
                # If it’s an array, using bare variable name in expression is invalid (must index).
                if isinstance(var_type, tuple) and var_type[0] == "array":
                    self.error(f"Array '{node}' used without index in expression.")
                return var_type
            # Check if spells out a boolean
            if node in ["true", "false"]:
                return "boolean"

            # Otherwise, assume it’s a string literal:
            return "string"

        # 2) If it’s an ASTNode with an operator or Factor
        if isinstance(node, ASTNode):
            if node.value == "Factor":
                return self._visit_factor(node)
            # Boolean operators
            if node.value == "AND" or node.value == "OR":
                left_type = self._visit_expression(node.children[0])
                right_type = self._visit_expression(node.children[1])
                if left_type != "boolean" or right_type != "boolean":
                    self.error(f"Logical operator '{node.value}' applied to non‐boolean operands.")
                return "boolean"
            if node.value == "NOT":
                sub_type = self._visit_expression(node.children[0])
                if sub_type != "boolean":
                    self.error("Logical 'NOT' applied to non‐boolean operand.")
                return "boolean"
            # Comparison operators
            if node.value in ("GT", "LT", "EQ", "GTE", "LTE"):
                left_type = self._visit_expression(node.children[0])
                right_type = self._visit_expression(node.children[1])
                # Pascal allows comparisons between integers, strings, booleans? Simplify: allow ints only
                # You can extend to allow comparing strings if desired.
                if left_type != right_type:
                    self.error(f"Comparison '{node.value}' with mismatched operand types '{left_type}' and '{right_type}'.")
                return "boolean"
            # Arithmetic operators: "+", "-", "*", "div", "mod"
            if node.value in ("+", "-", "*", "div", "mod"):
                left_type = self._visit_expression(node.children[0])
                right_type = self._visit_expression(node.children[1])
                if left_type != "integer" or right_type != "integer":
                    self.error(f"Arithmetic operator '{node.value}' applied to non‐integer operands.")
                return "integer"
            # Otherwise, it might be a nested expression that’s not recognized:
            # e.g. an ASTNode("Var", …) or a direct ASTNode("arg list", …)
            return self._visit_other_ast_node(node)
        
        # If none matched, it’s unexpected:
        self.error("Semantic: unexpected node in expression.")
    
    def _visit_factor(self, node: ASTNode):
        """
        node: ASTNode("Factor", [Primary, ASTNode("suffix list", suffixes…)])
        Primary can be:
           - int, bool, string → return its type
           - identifier (str) → variable or function name
           - ASTNode("body")? No, Primary will never be "body".
           - ASTNode from parentheses → handle recursively
        suffix list: list of ASTNode, each either:
           - ASTNode("arg list", [argExprNodes …])   → function call
           - an Expr (array indexing) ASTNode         → array access
        Returns the deduced type (string).
        """
        primary = node.children[0]
        suffix_list_node = node.children[1]
        # First, figure out primary’s type
        if isinstance(primary, int):
            ptype = "integer"
        elif isinstance(primary, bool):
            ptype = "boolean"
        elif isinstance(primary, str):
            # Could be a variable name or function name, or a string literal
            # If suffix_list is empty → it’s a variable reference or literal
            if not suffix_list_node.children:
                var_type = self.lookup_var(primary)
                if var_type is not None:
                    if isinstance(var_type, tuple) and var_type[0] == "array":
                        self.error(f"Array '{primary}' used without index in expression.")
                    return var_type
                # Otherwise, we assume it’s a string literal
                return "string"
            # If suffix_list is non‐empty:
            # The first suffix must be a function‐call or array‐index.
            first_suffix = suffix_list_node.children[0]
            # Distinguish “arg list” vs. pure index:
            if isinstance(first_suffix, ASTNode) and first_suffix.value == "arg list":
                # It’s a function call: primary is function name
                func_name = primary
                args = first_suffix.children  # list of expression nodes
                return self._check_function_call(func_name, args)
            else:
                # It’s array indexing: primary must be declared as array
                var_type = self.lookup_var(primary)
                if var_type is None:
                    self.error(f"Use of undeclared array '{primary}'.")
                if (not isinstance(var_type, tuple) or var_type[0] != "array") and (var_type != "string"):
                    self.error(f"Variable '{primary}' is not an array but used with index.")
                # For each index in suffix_list_node.children (they should all be expressions)
                for idx_expr in suffix_list_node.children:
                    idx_type = self._visit_expression(idx_expr)
                    if idx_type != "integer":
                        self.error(f"Array '{primary}' indexed by non-integer expression.")
                # After indexing, the resulting type is the element type
                return var_type[1] if isinstance(var_type, tuple) else var_type

        elif isinstance(primary, ASTNode):
            # Parenthesized expression: Primary → ASTNode representing an inner expression
            inner_type = self._visit_expression(primary)
            # But it shouldn’t have any suffixes if it’s parenthesized
            if suffix_list_node.children:
                self.error("Cannot apply suffix (call/index) to a parenthesized expression.")
            return inner_type

        else:
            self.error("Semantic: unexpected primary node type in factor.")

    def _check_function_call(self, func_name: str, arg_exprs: list):
        """
        Verify that 'func_name' is either built‐in or user‐defined, that arg count matches,
        and that each arg type matches the declared parameter type. Return the function’s return type.
        """
        # 1) Is it user‐defined?
        if func_name in self.functions:
            sig = self.functions[func_name]
            expected_params = sig["params"]      # list of (paramName, paramType)
            if len(arg_exprs) != len(expected_params):
                self.error(f"Function '{func_name}' expects {len(expected_params)} arguments, got {len(arg_exprs)}.")
            # Check each argument’s type
            for idx, (paramName, paramType) in enumerate(expected_params):
                arg_type = self._visit_expression(arg_exprs[idx])
                if arg_type != paramType:
                    self.error(f"Argument {idx+1} of '{func_name}' should be '{paramType}', got '{arg_type}'.")
            if sig["return_type"] is None:
                # It’s actually a procedure, not a function
                return None
            return sig["return_type"]

        # 2) Is it built‐in?
        func_name = func_name.lower()
        if func_name in self.builtins:
            builtin_sig = self.builtins[func_name]
            exp_params = builtin_sig["params"]
            if len(exp_params) != 0 and len(arg_exprs) != len(exp_params):
                self.error(f"Built‐in '{func_name}' expects {len(exp_params)} arguments, got {len(arg_exprs)}.")
            for idx, expected_type in enumerate(exp_params):
                arg_type = self._visit_expression(arg_exprs[idx])
                if arg_type != expected_type:
                    self.error(f"Built‐in '{func_name}' argument {idx+1} must be '{expected_type}', got '{arg_type}'.")
            return builtin_sig["return_type"]

        # 3) Not found at all
        self.error(f"Call to undefined function/procedure '{func_name}'.")

    def _visit_other_ast_node(self, node: ASTNode):
        """
        Handles any ASTNode we didn’t explicitly cover in _visit_expression. 
        For example, if someone writes a standalone ASTNode("Var", …) or "arg list" used in isolation.
        We try to interpret it sensibly or flag as error.
        """
        if node.value == "Var":
            # same logic as in assignment LHS: just a reference
            var_name = node.children[0]
            suffix_node = node.children[1]
            var_type = self.lookup_var(var_name)
            if var_type is None:
                self.error(f"Use of undeclared variable '{var_name}'.")
            if suffix_node is not None:
                # Array indexing
                if (not isinstance(var_type, tuple) or var_type[0] != "array") and (var_type != "string"):
                    self.error(f"Variable '{var_name}' is not an array but used with index.")
                for idx_expr in suffix_node.children:
                    idx_type = self._visit_expression(idx_expr)
                    if idx_type != "integer":
                        self.error(f"Array '{var_name}' indexed by non‐integer expression.")
                return var_type[1]
            else:
                if isinstance(var_type, tuple) and var_type[0] == "array":
                    self.error(f"Array '{var_name}' used without index in expression.")
                return var_type

        if node.value == "arg list":
            # Should only occur as part of a Factor
            self.error("Semantic: unexpected standalone 'arg list' node.")

        # If it is something else (e.g. a nested operator we missed), attempt to recursively visit children:
        # We assume it has exactly two children (binary operator).***
        if len(node.children) == 2 and isinstance(node.value, str):
            # Treat as though node.value is operator, though we should have covered most above
            left_type = self._visit_expression(node.children[0])
            right_type = self._visit_expression(node.children[1])
            # If both are integers, assume arithmetic/comparison → integer or boolean?
            if left_type == "integer" and right_type == "integer":
                # If operator is comparison‐like string, return boolean; else integer
                if node.value in ("GT", "LT", "EQ", "GTE", "LTE"):
                    return "boolean"
                return "integer"
            self.error(f"Semantic: cannot apply operator '{node.value}' to types '{left_type}', '{right_type}'.")
        # If none matched, it's an entirely unexpected AST shape:
        self.error(f"Semantic: unexpected AST node '{node.value}' in expression.")