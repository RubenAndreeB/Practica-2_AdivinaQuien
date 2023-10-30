import json
import tkinter as tk
from tkinter import messagebox

def load_database_from_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def save_database_to_json(database, file_path):
    with open(file_path, 'w') as file:
        json.dump(database, file, indent=4)

def take_chance(answer, attribute_id):
    ans = True if answer.lower() == "y" else False
    
    to_remove = []
    
    for character in database["characters"]:
        if character["attributes"][attribute_id] != ans:
            to_remove.append(character)
    
    for character in to_remove:
        database["characters"].remove(character)
    
    if len(database["characters"]) == 1:
        label_resultado.config(text="Tu personaje es " + database["characters"][0]["name"])
        confirm = messagebox.askyesno("¡Adiviné el personaje correctamente!", "¿Es este el personaje correcto?")
        if confirm:
            messagebox.showinfo("¡Éxito!", "¡Adiviné el personaje correctamente!")
            root.destroy()
        else:
            add_new_character()
        return

def ask_question(question, attribute_id):
    label_pregunta.config(text=question + " (y/n): ")

def continue_button_click():
    answer = respuesta_usuario.get()
    respuesta_usuario.set("")
    attribute_id = database["questions"][question_index]["id"]
    take_chance(answer, attribute_id)
    next_question()

def next_question():
    global question_index
    question_index += 1
    if question_index < len(database["questions"]):
        ask_question(database["questions"][question_index]["text"], database["questions"][question_index]["id"])
    else:
        label_pregunta.config(text="¡No pude adivinar el personaje!")
        button_continuar.config(state=tk.DISABLED)

def add_new_question_button_click():
    add_new_question(database)

def add_new_character():
    # Cargar la base de datos completa antes de agregar un nuevo personaje
    database = load_database_from_json("characters.json")
    
    new_name = input("Ingresa el nombre del nuevo personaje: ")
    
    # Preguntar si se quiere añadir una nueva pregunta
    add_new_question_option = input("¿Quieres añadir una nueva pregunta? (y/n): ")
    if add_new_question_option.lower() == "y":
        add_new_question(database)
    
    print("\nResponde las preguntas para añadir a " + new_name + " a la base de datos")
    new_attributes = {}
    for question in database["questions"]:
        attribute_id = question["id"]
        response = input(question["text"] + " (y/n): ")
        new_attributes[attribute_id] = True if response.lower() == "y" else False
    
    # Añadir el nuevo personaje con los atributos existentes más la nueva pregunta
    new_character = {"name": new_name, "attributes": new_attributes}
    database["characters"].append(new_character)
    
    # Guardar la base de datos actualizada
    save_database_to_json(database, "characters.json")
    
    print("Nuevo personaje agregado. Gracias por contribuir.")

def add_new_question(database):
    new_question_id = input("Ingresa el nuevo 'id' (por ejemplo, 'niño'): ")
    new_question_text = input("Ingresa la nueva pregunta: ")
    
    # Preguntar la nueva pregunta para todos los personajes existentes
    for character in database["characters"]:
        response = input(f"Respuesta para el nuevo atributo '{new_question_id}' para {character['name']} (y/n): ")
        character["attributes"][new_question_id] = True if response.lower() == "y" else False
    
    # Agregar la nueva pregunta a la lista de preguntas
    database["questions"].append({"id": new_question_id, "text": new_question_text})
    
# Cargar la base de datos desde el archivo JSON
global database
database = load_database_from_json("characters.json")

# Inicializar la interfaz gráfica
root = tk.Tk()
root.title("Adivinador de Personajes")
root.geometry("360x200")

# Declarar variables globales
question_index = 0

# Crear widgets
label_intro_text = "Por favor, piensa en un personaje de Dragon Ball Z. \nResponde las preguntas y trataré de adivinarlo."
label_intro = tk.Label(root, text=label_intro_text)
label_intro.pack()

label_pregunta = tk.Label(root, text="")
label_pregunta.pack()

label_resultado = tk.Label(root, text="")
label_resultado.pack()

respuesta_usuario = tk.StringVar()
entry_respuesta = tk.Entry(root, textvariable=respuesta_usuario)
entry_respuesta.pack()

button_continuar = tk.Button(root, text="Continuar", command=continue_button_click)
button_continuar.pack()

button_agregar_pregunta = tk.Button(root, text="Agregar Pregunta", command=add_new_question_button_click)
button_agregar_pregunta.pack()

# Mostrar la primera pregunta
ask_question(database["questions"][question_index]["text"], database["questions"][question_index]["id"])

# Iniciar la interfaz gráfica
root.mainloop()