import sys
import ply.yacc as yacc
from ana_lex import tokens
from ana_lex import literals

from AST.tree import ASTNode


def p_program_program(p):
    """
    Program : PROGRAM id ';' OptionalVarList FunctionList Main
    """
    p[0] = ASTNode("program", [p[2], p[4], ASTNode("functionlist", p[5]), p[6]])

def p_optionalvarlist_varsection(p):
    """
    OptionalVarList : VarSection
    """
    p[0] = p[1]


def p_optionalvarlist(p):
    """
    OptionalVarList :
    """


def p_functionlist_functionlist(p):
    """
    FunctionList : FunctionList FunctionListElem
    """
    p[0] = p[1] + [p[2]]


def p_functionlist_functionlistelem(p):
    """
    FunctionList : FunctionListElem
    """
    p[0] = [p[1]]


def p_functionlist_empty(p):
    """
    FunctionList :
    """
    p[0] = []


def p_functionlistelem_function(p):
    """
    FunctionListElem : FUNCTION FuncDefinition ':' id ';' OptionalVarList FunctionBody
    """
    p[0] = ASTNode("function", [p[2], p[4], p[6], p[7]])


def p_functionlistelem_procedure(p):
    """
    FunctionListElem : PROCEDURE FuncDefinition ';' OptionalVarList FunctionBody
    """
    p[0] = ASTNode("procedure", [p[2], p[4], p[5]])


def p_funcdefinition_id(p):
    """
    FuncDefinition : id Parameters
    """
    p[0] = ASTNode("functionid", [p[1], p[2]])


def p_parameters_(p):
    """
    Parameters : '(' PairList ')'
    """
    p[0] = ASTNode("params", p[2])


def p_parameters_empty(p):
    """
    Parameters :
    """


def p_pairlist_pairlist(p):
    """
    PairList : PairList ';' PairListElem
    """
    p[0] = p[1] + [p[3]]

def p_pairlist_pairlistelem(p):
    """
    PairList : PairListElem
    """
    p[0] = [p[1]]


def p_pairlist_empty(p):
    """
    PairList :
    """
    p[0] = []


def p_pairlistelem_id(p):
    """
    PairListElem : id ':' id
    """
    p[0] = ASTNode("pair", [p[1], p[3]])


def p_functionbody_begin(p):
    """
    FunctionBody : BEGIN Body OptionalSemiColon END ';'
    """
    p[0] = ASTNode("body", p[2])


def p_main_varsection(p):
    """
    Main : OptionalVarList MainSection
    """
    p[0] = ASTNode("main", [p[1], p[2]])


def p_varsection_var(p):
    """
    VarSection : VAR VarsList
    """
    p[0] = ASTNode("varsection", p[2])


def p_varslist_varslist(p):
    """
    VarsList : VarsList VarsListElem
    """
    p[0] = p[1] + [p[2]]


def p_varslist_varslistelem(p):
    """
    VarsList : VarsListElem
    """
    p[0] = [p[1]]


def p_varslistelem_varslistelemids(p):
    """
    VarsListElem : VarsListElemIDs ':' VarType ';'
    """
    p[0] = ASTNode("var", [ASTNode("varIds", p[1]), p[3]])


def p_vartype_id(p):
    """
    VarType : id
    """
    p[0] = p[1]


def p_vartype_array(p):
    """
    VarType : ARRAY ArrayIndexes OF id
    """
    p[0] = ASTNode("array", [p[2], p[4]])


def p_arrayindexes_(p):
    """
    ArrayIndexes : '[' num '.' '.' num ']'
    """
    p[0] = ASTNode("arrayindexes", [p[2], p[5]])


def p_arrayindexes_empty(p):
    """
    ArrayIndexes :
    """


def p_varslistelemids_varslistelemids(p):
    """
    VarsListElemIDs : VarsListElemIDs ',' id
    """
    p[0] = p[1] + [p[3]]

def p_varslistelemids_id(p):
    """
    VarsListElemIDs : id
    """
    p[0] = [p[1]]


def p_mainsection_begin(p):
    """
    MainSection : BEGIN Body OptionalSemiColon END '.' 
    """
    p[0] = ASTNode("body", p[2])


def p_body_body(p):
    """
    Body : Body ';' BodyElem
    """
    p[0] = p[1] + [p[3]]

def p_body_bodyelem(p):
    """
    Body : BodyElem
    """
    p[0] = [p[1]]


def p_bodyelem_factor(p):
    """
    BodyElem : Factor
    """
    p[0] = p[1]


def p_bodyelem_atrib(p):
    """
    BodyElem : Atrib
    """
    p[0] = p[1]

def p_bodyelem_forstatement(p):
    """
    BodyElem : FORStatement
    """
    p[0] = p[1]

def p_bodyelem_ifstatement(p):
    """
    BodyElem : IFStatement
    """
    p[0] = p[1]

def p_bodyelem_whilestatement(p):
    """
    BodyElem : WHILEStatement
    """
    p[0] = p[1]


def p_argslist_argslist(p):
    """
    ArgsList : ArgsList ',' Arg
    """
    p[0] = p[1] + [p[3]]

def p_argslist_arg(p):
    """
    ArgsList : Arg
    """
    p[0] = [p[1]]


def p_argslist_empty(p):
    """
    ArgsList :
    """
    p[0] = []


def p_arg_(p): # Não podia ser '(' Exp ')'?
    """
    Arg : '(' Arg ')'
    """
    p[0] = p[2]

def p_arg_exp(p):
    """
    Arg : Exp
    """
    p[0] = p[1]


def p_forstatement_for(p):
    """
    FORStatement : FOR Atrib FORTo Exp DO FORBody
    """
    p[0] = ASTNode("for", [p[2], p[3], p[4], p[6]])


def p_forto_to(p):
    """
    FORTo : TO
    """
    p[0] = "to"


def p_forto_downto(p):
    """
    FORTo : DOWNTO
    """
    p[0] = "downto"

def p_forbody_begin(p):
    """
    FORBody : BEGIN Body OptionalSemiColon END
    """
    p[0] = ASTNode("body", p[2])


def p_forbody_bodyelem(p):
    """
    FORBody : BodyElem
    """
    p[0] = p[1]


def p_ifstatement_if(p):
    """
    IFStatement : IF Condition THEN IFBody IFStatementCont
    """
    p[0] = ASTNode("if", [p[2], p[4], p[5]])


def p_ifstatementcont_else(p):
    """
    IFStatementCont : ELSE IFBody
    """
    p[0] = p[2]

def p_ifstatementcont_empty(p):
    """
    IFStatementCont : 
    """
    p[0] = None

def p_ifbody_begin(p):
    """
    IFBody : BEGIN Body OptionalSemiColon END
    """
    p[0] = ASTNode("body", p[2])

def p_ifbody_bodyelem(p):
    """
    IFBody : BodyElem
    """
    p[0] = p[1]

def p_whilestatement_while(p):
    """
    WHILEStatement : WHILE Condition DO WHILEBody
    """
    p[0] = ASTNode("while", [p[2], p[4]])


def p_whilebody_begin(p):
    """
    WHILEBody : BEGIN Body OptionalSemiColon END
    """
    p[0] = ASTNode("body", p[2])


def p_whilebody_bodyelem(p):
    """
    WHILEBody : BodyElem
    """
    p[0] = p[1]


def p_condition_(p):
    """
    Condition : '(' Condition ')'
    """
    p[0] = p[2]


def p_condition_logicexp(p):
    """
    Condition : Exp
    """
    p[0] = p[1]


def p_atrib_suffixlistarray(p):
    """
    Atrib : id SuffixListArray ':' '=' Exp
    """
    subnode = ASTNode("array suffix list", p[2]) if p[2] else None
    p[0] = ASTNode("Atrib", [ASTNode("Var", [p[1], subnode]) , p[5]])


def p_comparationsymbol_gt(p):
    """
    ComparationSymbol : '>'
    """
    p[0] = "GT"


def p_comparationsymbol_lt(p):
    """
    ComparationSymbol : '<'
    """
    p[0] = "LT"


def p_comparationsymbol_e(p):
    """
    ComparationSymbol : '='
    """
    p[0] = "EQ"


def p_comparationsymbol_gte(p):
    """
    ComparationSymbol : '>' '='
    """
    p[0] = "GTE"

def p_comparationsymbol_lte(p):
    """
    ComparationSymbol : '<' '='
    """
    p[0] = "LTE"

def p_optionalsemicolon_(p):
    """
    OptionalSemiColon : ';'
    """


def p_optionalsemicolon_empty(p):
    """
    OptionalSemiColon :
    """

def p_factor_primary(p):
    """
    Factor : Primary SuffixList
    """
    p[0] = ASTNode("Factor", [p[1], ASTNode("suffix list", p[2])]) if p[2] else p[1]

def p_suffixlist_suffixlist(p):
    """
    SuffixList : SuffixList Suffix
    """
    p[0] = p[1] + [p[2]]

def p_suffixlist_(p):
    """
    SuffixList : 
    """
    p[0] = []

def p_suffix_(p):
    """
    Suffix : '(' ArgsList ')'
    """
    p[0] = ASTNode("arg list", p[2])

def p_suffix_exp(p):
    """
    Suffix : '[' Exp ']'
    """
    p[0] = p[2]

def p_suffixlistarray_arr(p):
    """
    SuffixListArray : '[' Exp ']' SuffixListArray
    """
    p[0] = [p[2]] + p[4]

def p_suffixlistarray_(p):
    """
    SuffixListArray : 
    """
    p[0] = []

def p_primary_num(p):
    """
    Primary : num
    """
    p[0] = int(p[1])

def p_primary_string(p):
    """
    Primary : string
    """
    p[0] = str(p[1])

def p_primary_boolean(p):
    """
    Primary : boolean
    """
    p[0] = p[1]

def p_primary_id(p):
    """
    Primary : id
    """
    p[0] = p[1]
    
def p_primary_exp(p):
    """
    Primary : '(' Exp ')'
    """
    p[0] = p[2]

def p_termop_plus(p):
    """
    TermOp : '+'
    """
    p[0] = '+'

def p_termop_minus(p):
    """
    TermOp : '-'
    """
    p[0] = '-'

def p_factorop_mult(p):
    """
    FactorOp : '*'
    """
    p[0] = '*'

def p_factorop_div(p):
    """
    FactorOp : '/'
    """
    p[0] = '/'

def p_factorop_int_div(p):
    """
    FactorOp : DIV
    """
    p[0] = "div"

def p_factorop_mod(p):
    """
    FactorOp : MOD
    """
    p[0] = "mod"

def p_exp_orexp(p):
    """
    Exp : OrExp
    """
    p[0] = p[1]

def p_orexp_orexp(p):
    """
    OrExp : OrExp OR AndExp
    """
    p[0] = ASTNode("OR", [p[1], p[3]])

def p_orexp_andexp(p):
    """
    OrExp : AndExp
    """
    p[0] = p[1]

def p_andexp_andexp(p):
    """
    AndExp : AndExp AND RelExp
    """
    p[0] = ASTNode("AND", [p[1], p[3]])

def p_andexp_relexp(p):
    """
    AndExp : RelExp
    """
    p[0] = p[1]

def p_relexp_addexp_comp(p):
    """
    RelExp : AddExp ComparationSymbol AddExp
    """
    p[0] = ASTNode(p[2], [p[1], p[3]])

def p_relexp_addexp(p):
    """
    RelExp : AddExp
    """
    p[0] = p[1]

def p_addexp_addexp(p):
    """
    AddExp : AddExp TermOp MulExp
    """
    p[0] = ASTNode(p[2], [p[1], p[3]])

def p_addexp_mulexp(p):
    """
    AddExp : MulExp
    """
    p[0] = p[1]

def p_mulexp_mulexp(p):
    """
    MulExp : MulExp FactorOp Unary
    """
    p[0] = ASTNode(p[2], [p[1], p[3]])

def p_mulexp_unary(p):
    """
    MulExp : Unary
    """
    p[0] = p[1]

def p_unary_not(p):
    """
    Unary : NOT Unary
    """
    p[0] = ASTNode("NOT", p[2])

def p_unary_primary(p):
    """
    Unary : Factor
    """
    p[0] = p[1]


def p_error(p):
    parser.success = False
    if p:
        print(f"Syntax error at '{p.value}', line {p.lineno}, position {p.lexpos}")
    else:
        print("Syntax error at end of input")
    print("Erro de sintaxe!")


parser = yacc.yacc()

""" texto = sys.stdin.read()
parser.success = True
res = parser.parse(texto)

if parser.success:
    print(f"Texto válido.\n")
else:
    print("Texto inválido...")
 """

def parse_pascal(text):
    parser.success = True
    result = parser.parse(text)
    if parser.success:
        return result
    else:
        raise ValueError("Parsing failed.")


