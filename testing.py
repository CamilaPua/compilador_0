from lexer import lexer
from parser import parser, variables
from clear_code import preprocess_code


code = '''
a=0 ::
while (a<3) do
    a = a+1 ::
    write(a) ::
    if (a<>2) then
        write("Camila")::
    else
        write("Orinson")::
    endif
endwhile
'''
# c = 4 ::
# p = 3 ::
# variable = (5 + c) * 4 + (30-p) ::
# variable ::
# b=1+variable ::
# write(variable) ::
# capture(a) ::
# if (a == c) then
# blablabalba
# endif ::

final_code = preprocess_code(code)


for line in final_code.split('\n'):
    line = line.strip()
    if line:
        result = parser.parse(line)

        if result is not None:  # Solo imprime si hay resultado
            print(result)


print("\nVariables definidas:")
for var, val in variables.items():
    print(f"{var} = {val}")
