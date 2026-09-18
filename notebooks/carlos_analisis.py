# generador.py
codigo = '''print("Hola, mundo!")
for i in range(5):
    print(f"Número: {i}")'''

with open("salida.py", "w", encoding="utf-8") as f:
    f.write(codigo)

lineas = codigo.count("\n") + 1
print("Archivo 'salida.py' creado.")