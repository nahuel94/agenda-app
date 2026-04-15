import requests

URL = "http://127.0.0.1:5000"  # cambiar cuando uses Render

def crear_tarea():
    desc = input("Ingrese tarea: ")

    response = requests.post(
        f"{URL}/tareas",
        json={"descripcion": desc}
    )

    print(response.json())

def ver_tareas():

    response = requests.get(f"{URL}/tareas")

    tareas = response.json()

    print("\n--- TAREAS ---")
    for t in tareas:
        print(f"{t['id']} - {t['descripcion']}")

def eliminar_tarea():
    id = input("ID a eliminar: ")

    response = requests.delete(f"{URL}/tareas/{id}")
    print(response.json())

while True:
    print("\n1. Crear tarea")
    print("2. Ver tareas")
    print("3. Eliminar tarea")
    print("4. Salir")

    op = input("Opción: ")

    if op == "1":
        crear_tarea()
    elif op == "2":
        ver_tareas()
    elif op == "3":
        eliminar_tarea()
    elif op == "4":
        break