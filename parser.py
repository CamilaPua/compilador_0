import ply.yacc as yacc
from lexer import tokens  # Asume que tu código anterior está en lexer.py

variables = {}
salidas = []


def p_program(p):
    'program : statement_list'

def p_statement_list(p):
    '''statement_list : statement
                      | statement_list statement'''

def p_statement(p):
    '''statement : assignment DPOINTS
                 | write DPOINTS
                 | capture DPOINTS
                 | expression DPOINTS
                 | if_statement DPOINTS'''


def p_assignment(p):
    "assignment : ID ASSIGN expression"
    if p[3] is None:
        print(f"Error: Asignación incompleta para '{p[1]}'")
        p[0] = None
    else:
        variables[p[1]] = p[3]
        p[0] = p[3]



def p_expression_var(p):
    "expression : ID"
    try:
        p[0] = variables[p[1]]
    except KeyError:
        print(f"Error: Variable '{p[1]}' not defined.")
        p[0] = 0  # Default value


def p_expression_plus(p):
    "expression : expression '+' term"
    p[0] = p[1] + p[3]


def p_expression_minus(p):
    "expression : expression '-' term"
    p[0] = p[1] - p[3]


def p_expression_term(p):
    "expression : term"
    p[0] = p[1]


def p_term_times(p):
    "term : term '*' factor"
    p[0] = p[1] * p[3]


def p_term_div(p):
    "term : term '/' factor"
    p[0] = p[1] / p[3]


def p_term_factor(p):
    "term : factor"
    p[0] = p[1]


def p_factor_num(p):
    "factor : NUMBER"
    p[0] = p[1]


def p_factor_expr(p):
    "factor : '(' expression ')'"
    p[0] = p[2]

#---------FUNCION WRITE---------
def p_factor_id(p):
    "factor : ID"
    try:
        p[0] = variables[p[1]]
    except KeyError:
        print(f"Error: Variable '{p[1]}' not defined.")
        p[0] = 0

def p_write(p):
    '''write : WRITE '(' STRING ')'
             | WRITE '(' expression ')'
             | WRITE '(' STRING ',' expression ')' '''
    
    if len(p) == 5:  # write("mensaje")
        salidas.append(str(p[3]))
    elif len(p) == 6:  # write(expresion)
        salidas.append(str(p[3]))
    elif len(p) == 7:  # write("mensaje", expresion)
        salidas.append(str(p[3]) + str(p[5]))
#--------------------------
def p_statement_list(p):
    '''statement_list : statement
                      | statement_list DPOINTS statement'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[1].append(p[3])
        p[0] = p[1]

def p_capture(p):
    "capture : CAPTURE '(' ID ')'"
    var = p[3]
    salidas.append(f"Ingreso solicitado para variable '{p[3]}'")
    variables[var] = "valor_simulado"  # Puedes poner aquí un valor fijo


# //////////////////////////////////
# //////////////////////////////////

def p_if_statement(p):
    "if_statement : IF '(' condition ')' THEN statement_list opt_else ENDIF"
    # p[3] : condición, p[6] : sentencias para el caso verdadero,
    # p[7] : opcionalmente la parte ELSE (None si no se incluye).
    p[0] = ('if', p[3], p[6], p[7])

def p_opt_else(p):
    '''opt_else : ELSE statement_list
                | empty'''
    if len(p) == 3:
        p[0] = p[2]
    else:
        p[0] = None

def p_empty(p):
    "empty :"
    p[0] = None

def p_condition(p):
    "condition : boolean_expr"
    p[0] = p[1]

def p_boolean_expr_or(p):
    "boolean_expr : boolean_expr OR boolean_expr"
    p[0] = ('or', p[1], p[3])

def p_boolean_expr_and(p):
    "boolean_expr : boolean_expr AND boolean_expr"
    p[0] = ('and', p[1], p[3])

def p_boolean_expr_not(p):
    "boolean_expr : NOT boolean_expr"
    p[0] = ('not', p[2])

def p_boolean_expr_paren(p):
    "boolean_expr : '(' boolean_expr ')'"
    p[0] = p[2]

def p_boolean_expr_rel(p):
    "boolean_expr : expression relational_operator expression"
    p[0] = (p[2], p[1], p[3])

def p_boolean_expr_exp(p):
    "boolean_expr : expression"
    p[0] = p[1]

def p_relational_operator(p):
    '''relational_operator : '<'
                           | '>'
                           | LESSEQ
                           | GREATEREQ
                           | EQUALS
                           | NOTEQ'''
    p[0] = p[1]

# //////////////////////////////////
# //////////////////////////////////






errorFound = False  # Asegúrate de que esté en el alcance global

def p_error(p):
    global errorFound
    errorFound = True
    if p:
        print(f"Syntax error at '{p.value}'. Line: {p.lineno}")
    else:
        print("Syntax error at end of input")




def obtener_salidas():
    global salidas
    resultado = "\n".join(salidas)
    salidas = []  # Limpia después de obtener
    return resultado

# Build the parser
parser = yacc.yacc(start='program')