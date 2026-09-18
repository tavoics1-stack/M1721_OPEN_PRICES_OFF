# generador.py
from datetime import datetime

codigo = '''print("Hola, mundo!")
for i in range(5):
    print(f"Número: {i}")'''

encabezado = f"# Generado automáticamente el {datetime.now():%Y-%m-%d %H:%M:%S}\n"

with open("salida.py", "w", encoding="utf-8") as f:
    f.write(encabezado + codigo)

lineas = codigo.count("\n") + 1
print(f"Archivo 'salida.py' creado con {lineas} líneas.")