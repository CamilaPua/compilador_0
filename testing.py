from lexer import lexer
from parser import parser, variables


code = '''
c = 4 ::
p = 3 ::
    variable = (5 + c) * 4 + (30-p) ::
write(variable) ::
capture(a) ::
if (a == c) then
blablabalba
endif ::
'''


for line in code.split('\n'):
    line = line.strip()
    if line:
        result = parser.parse(line)

        if result is not None:  # Solo imprime si hay resultado
            print(result)


print("\nVariables definidas:")
for var, val in variables.items():
    print(f"{var} = {val}")
