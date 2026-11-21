"""Muestra ejemplos sencillos de funciones, listas y comandos de Git."""


def verificar_comando(lista, cmd):
  """Indica si el texto de un comando está presente en la lista recibida."""
  return cmd in lista


print("Iniciando proceso...")
print("Cargando datos...")
print("Proceso finalizado con éxito.")

print("Se agrega a Fabian Andres al proyecto en su propia rama")
print("Se agrega a Alejandro Reyes al proyecto con su propia rama")

print(
    "se notifica a Alejandro al foro que ya debio haber recibido la invitacion a"
    " colaborar al repo"
)
print("se crea el archivo que manejara la excepciones")
print("se crea el archivo que almacenara la clase cliente ")
print("se crea el archivo que logger.py")
print("se crea el archivo main.py")
print("se crea el archivo entidad.py")

# Registro de ramas
ramas_equipo = ["main", "develop", "feature/fabian", "feature/alejandro"]
print(f"Ramas activas en el repositorio: {len(ramas_equipo)}")

comandos_git = [
    "git init",
    "git clone",
    "git status",
    "git add",
    "git commit",
    "git push",
    "git pull",
    "git branch",
    "git checkout",
    "git merge",
]

print("Estos son los comandos más importantes de Git:")
for i, comando in enumerate(comandos_git, start=1):
  print(f"{i}. {comando}")

# --- Agregando comandos de historial ---
comandos_git.append("git stash")
comandos_git.append("git log")
comandos_git.append("git diff")

print("Nuevos items:")
for comando in comandos_git:
  print(comando)

# Validación rápida
print("¿Existe git log?:", verificar_comando(comandos_git, "git log"))
