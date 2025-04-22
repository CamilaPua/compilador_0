from nicegui import ui
from lexer import lexer
from parser import parser, obtener_salidas
import os

# Crear carpeta 'archivos' si no existe (útil para Render)
os.makedirs("archivos", exist_ok=True)


#  Estilo global de la página
#ui.query('body').style('background-color: #1e1e1e; color: white; font-family: sans-serif;')


#  Variables globales
editor = None           # Área donde se escribe el código fuente
resultado_label = None  # Etiqueta para mostrar resultados o mensajes


#Funcion para guardar archivos
def guardar_archivo():
    nombre = archivo_input.value.strip()
    if not nombre:
        resultado_label.set_text(" Ingresa un nombre para el archivo.")
        return
    ruta = os.path.join("archivos", f"{nombre}.code")
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(editor.value)
    resultado_label.set_text(f"Archivo '{nombre}.code' guardado.")


#Funcion para abrir archivos
def abrir_archivo():
    nombre = archivo_input.value.strip()
    if not nombre:
        resultado_label.set_text(" Ingresa el nombre del archivo a abrir.")
        return
    ruta = os.path.join("archivos", f"{nombre}.code")
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            editor.value = f.read()
        resultado_label.set_text(f"Archivo '{nombre}.code' cargado.")
    except FileNotFoundError:
        resultado_label.set_text(f" Archivo '{nombre}.code' no encontrado.")


#Funcion para ver los archivos existenntes
def listar_archivos():
    archivos = os.listdir("archivos")
    archivos_code = [f for f in archivos if f.endswith(".code")]
    if archivos_code:
        resultado_label.set_text("Archivos disponibles:\n" + "\n".join(archivos_code))
    else:
        resultado_label.set_text("No hay archivos guardados.")


#Funcion para crear un archivo
def nuevo_archivo():
    archivo_input.value = ""
    editor.value = ""
    resultado_label.set_text("Nuevo archivo creado.")


#  Elimina el archivo de código y limpia el editor
def eliminar_archivo():
    nombre = archivo_input.value.strip()
    if not nombre:
        resultado_label.set_text(" Ingresa el nombre del archivo a eliminar.")
        return
    ruta = os.path.join("archivos", f"{nombre}.code")
    try:
        os.remove(ruta)
        editor.value = ""
        resultado_label.set_text(f"Archivo '{nombre}.code' eliminado.")
    except FileNotFoundError:
        resultado_label.set_text(f" Archivo '{nombre}.code' no encontrado.")


# Analiza el código y muestra los tokens encontrados
def ver_tokens():
    lexer.input(editor.value)
    tokens_encontrados = []

    while True:
        tok = lexer.token()
        if not tok:
            break
        tokens_encontrados.append((tok.type, tok.value))

    # Mostrar resumen
    if tokens_encontrados:
        resultado_label.set_text(f" Total de tokens: {len(tokens_encontrados)}")
        
        # Limpiar tablas anteriores (si las hay)
        if hasattr(ver_tokens, "tabla"):
            ver_tokens.tabla.delete()

        # Crear nueva tabla
        ver_tokens.tabla = ui.table(
            columns=[
                {'name': 'tipo', 'label': 'Tipo de Token', 'field': 'tipo'},
                {'name': 'valor', 'label': 'Valor', 'field': 'valor'}
            ],
            rows=[{'tipo': t[0], 'valor': t[1]} for t in tokens_encontrados],
            row_key='tipo'
        ).classes("mt-4 w-full max-w-2xl mx-auto bg-white text-black")
    
    else:
        resultado_label.set_text(" No se encontraron tokens válidos.")
        if hasattr(ver_tokens, "tabla"):
            ver_tokens.tabla.delete()




#  Función para compilar el código fuente
def compilar():
    # Limpiar cualquier mensaje previo
    resultado_label.set_text("")
    codigo = editor.value.strip()

    if not codigo:
        resultado_label.set_text(" No hay código para compilar.")
        return
    
    # Dividir el código en líneas
    lines = codigo.split('\n')
    
    # Variable para almacenar el código procesado
    processed_code = []
    
    # Variable para manejar si estamos dentro de un bloque 'if'
    inside_if = False
    if_block = []
    
    for line in lines:
        # Limpiar la línea de posibles espacios en blanco
        line = line.strip()
        if inside_if:
            if line == "endif":
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
    
    print(final_code)

    try:
        # Forzamos un error para comprobar
        # raise Exception("Error de prueba")
        
        # Ejecutamos el parser de YACC sobre el código
        for line in final_code.split('\n'):
            line = line.strip()
            if line:
                result = parser.parse(line)
        
                if result is not None:  # Solo imprime si hay resultado
                    print(result)
        # parse_result = parser.parse(final_code)
        
        # Obtener salida del write si existe
        salida_final = obtener_salidas()

        if salida_final:
            resultado_label.set_text(f"Salida:\n{salida_final}")
        else:
            resultado_label.set_text(" Compilación exitosa.")
    
    except SyntaxError as se:
        print("Capturada SyntaxError:", se)
        resultado_label.set_text(f" Error de sintaxis: {se}")
    except Exception as e:
        print("Capturada Exception:", e)
        resultado_label.set_text(f" Error inesperado: {e}")


# -------------- INTERFAZ GRÁFICA ----------------

#  Título principal centrado
ui.label("Micro Compilador - Versión Web").classes("text-3xl text-black font-bold mb-4 text-center")

#Nobre del archivo
archivo_input = ui.input(label="Nombre del archivo").classes("w-full max-w-xs")


#  Área de texto para ingresar el código fuente
editor = ui.textarea(
    label="Código fuente",
    placeholder="Escribe tu código aquí..."
).classes('w-full h-60 bg-white text-black rounded p-2')

#  Botones de acción organizados en fila
with ui.row().classes("justify-center gap-4 mt-4"):
    ui.button("🆕 Nuevo", on_click=nuevo_archivo).classes("bg-blue-700 text-white")
    ui.button("💾 Guardar", on_click=guardar_archivo).classes("bg-green-600 text-white")
    ui.button("📂 Abrir", on_click=abrir_archivo).classes("bg-indigo-600 text-white")
    ui.button("📃 Ver Archivos", on_click=listar_archivos).classes("bg-gray-600 text-white")
    ui.button("❌ Eliminar", on_click=eliminar_archivo).classes("bg-red-600 text-white")
    ui.button("🔍 Ver Tokens", on_click=ver_tokens).classes("bg-yellow-600 text-black")
    ui.button("⚙️ Compilar", on_click=compilar).classes("bg-purple-700 text-white")

#  Área para mostrar resultados o mensajes
resultado_label = ui.label("").classes('text-lg mt-6 whitespace-pre-wrap text-center text-black')


# --------------- Iniciar servidor web local -------------------
ui.run()

# ---------------- Iniciar servidor web en render -----------------
#ui.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
