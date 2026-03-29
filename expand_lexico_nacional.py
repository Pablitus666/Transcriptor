import json
import os

# ================= MOTOR DE EXPANSIÓN NACIONAL BOLIVIA =================

APELLIDOS_BOL = [
    "Mamani", "Flores", "Quispe", "Choque", "Vargas", "Condori", "Rodríguez", "Rojas", 
    "Gutiérrez", "López", "Fernández", "Gonzales", "García", "Cruz", "Pérez", "Mendoza", 
    "Sánchez", "Martínez", "Chávez", "Ramos", "Apaza", "Huanca", "Vaca", "Tórrez", 
    "Guzmán", "Suárez", "Aguilar", "Justiniano", "Romero", "Colque", "Cuéllar", "Ramírez", 
    "Vásquez", "Soliz", "Miranda", "Villca", "Morales", "Álvarez", "Ortiz", "Espinoza", 
    "Ticona", "Villarroel", "Chambi", "Castro", "Durán", "Méndez", "Jiménez", "Nina", 
    "Gómez", "Tapia", "Torrico", "Rivero", "Castillo", "Rocha", "Herrera", "Medina", 
    "Cardozo", "Claros", "Zenteno", "Beltrán", "Poma", "Delgado", "Camacho", "Arispe", 
    "Velasco", "Pinto", "Cabrera", "Solares", "Mercado", "Ayala", "Lozano", "Hurtado", 
    "Saavedra", "Terrazas", "Quiroga", "Salazar", "Paredes", "Serrano", "Blanco", 
    "Machaca", "Yujra", "Canaviri", "Loza", "Valda", "Montaño", "Bejarano", "Encinas", 
    "Salvatierra", "Aguilera", "Padilla", "Soto", "Valenzuela", "Bravo", "Arias", 
    "Pacheco", "Luna", "Luque", "Maita", "Orellana", "Alarcón", "Barrientos", "Cayo", 
    "Daza", "Escalera", "Fuentes", "Garnica", "Heredia", "Iriarte", "Jaldín", "Ledezma", 
    "Maldonado", "Navia", "Orosco", "Prado", "Quintana", "Ríos", "Sandoval", "Trujillo", 
    "Ugarte", "Vera", "Zambrana"
]

NOMBRES_BOL = [
    "Juan", "José", "Luis", "Carlos", "Mario", "Jorge", "Víctor", "Miguel", "Pedro", 
    "Antonio", "Fernando", "Roberto", "Félix", "Julio", "René", "Javier", "Ángel", 
    "Alberto", "David", "Freddy", "Oscar", "Hugo", "Daniel", "Francisco", "Edwin", 
    "Eduardo", "Raúl", "Ricardo", "Grover", "Limbert", "Wilson", "Richard", "Christian", 
    "Ronald", "Jaime", "Marcelo", "Edgar", "Ramiro", "Iván", "Alejandro", "Hernán",
    "Boris", "Franz", "Guido", "Henry", "Jhonny", "Milton", "Nelson", "Orlando", "Pablo", 
    "Rubén", "Sergio", "Walter", "María", "Juana", "Ana", "Martha", "Carmen", "Rosa", 
    "Julia", "Elizabeth", "Cristina", "Lidia", "Patricia", "Sonia", "Isabel", "Silvia", 
    "Elena", "Gladys", "Bertha", "Nancy", "Beatriz", "Alicia", "Teresa", "Margarita", 
    "Yolanda", "Victoria", "Elsa", "Blanca", "Felipa", "Gregoria", "Teodora", "Antonia", 
    "Lucía", "Francisca", "Petrona", "Modesta", "Benedicta", "Casilda", "Dionisia", 
    "Enriqueta", "Fortunata", "Gertrudis", "Roxana", "Rosmery", "Miriam", "Sandra", 
    "Paola", "Adriana", "Claudia", "Daniela", "Erika", "Fabiola", "Gabriela", "Hilda", 
    "Inés", "Janet", "Karina", "Laura", "Mónica", "Natalia", "Olga", "Pilar", "Raquel", 
    "Sara", "Tatiana", "Úrsula", "Verónica", "Wendy", "Ximena", "Yesenia", "Zulma",
    "Inti", "Amaru", "Nayra"
]

# Palabras que NO deben entrar como nombres porque causarían falsos positivos
EXCLUSIONES = {"Calle", "Día", "Blanca", "Rosa", "Victoria", "Mercado", "Ríos", "Prado", "Poma"}

def expandir():
    json_path = "utils/person_names.json"
    if not os.path.exists(json_path):
        current_names = set()
    else:
        with open(json_path, "r", encoding="utf-8") as f:
            current_names = set(json.load(f))

    # Fusionar con listas nacionales
    for n in APELLIDOS_BOL + NOMBRES_BOL:
        if n not in EXCLUSIONES:
            current_names.add(n)

    # Guardar
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(sorted(list(current_names)), f, ensure_ascii=False, indent=4)
    
    print(f"Diccionario expandido exitosamente. Ahora cuenta con {len(current_names)} entradas.")

if __name__ == "__main__":
    expandir()
