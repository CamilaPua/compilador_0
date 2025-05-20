from lexer import lexer
from parser import parser, variables


code = '''
write("?AQUIIIIIIIIIII")::
A = 2 ::
if ( 5<3) then
    write("SIIIIIIIIII") ::
    A = 5 ::
else
    write("NOOOOOOOO") ::
    A=2 ::
endif

write(1+A) ::
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

# Dividir el código en líneas
lines = code.split('\n')

# Variable para almacenar el código procesado
processed_code = []

# Variable para manejar si estamos dentro de un bloque 'if'
inside_if = False
if_block = []

for line in lines:
    # Limpiar la línea de posibles espacios en blanco
    line = line.strip()
    if inside_if:
        if line.replace(" ", "") == "endif":
            # Al encontrar 'endif', terminamos el bloque if
            if_block.append(line)
            processed_code.append(" ".join(if_block))
            inside_if = False
            if_block = []
        else:
            # Añadir la línea al bloque 'if' hasta 'endif'
            if_block.append(line)
    elif line.startswith("if"):
        # Comienza un bloque 'if'
        inside_if = True
        if_block.append(line)
    else:
        # Línea normal, agregarla sin cambios
        processed_code.append(line)
# Unir las líneas procesadas de nuevo
final_code = '\n'.join(processed_code)

# print(final_code)

for line in final_code.split('\n'):
    line = line.strip()
    if line:
        result = parser.parse(line)

        if result is not None:  # Solo imprime si hay resultado
            print(result)


print("\nVariables definidas:")
for var, val in variables.items():
    print(f"{var} = {val}")
