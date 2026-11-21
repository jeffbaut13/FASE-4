"""Muestra ejemplos sencillos de funciones, listas y comandos de Git."""


def verificar_comando(lista, cmd):
  """Indica si el texto de un comando está presente en la lista recibida."""
  return cmd in lista


print("Iniciando proceso...")
print("Cargando datos...")
print("Proceso finalizado con éxito.")

# Estos mensajes registran las tareas que se agregaron durante el trabajo grupal.
print("Se agrega a Fabian Andres al proyecto en su propia rama")
print("Se agrega a Alejandro Reyes al proyecto con su propia rama")

# También se deja constancia del aviso enviado al foro del equipo.
print(
    "se notifica a Alejandro al foro que ya debio haber recibido la invitacion a"
    " colaborar al repo"
)
# Los siguientes mensajes representan la creación de archivos del proyecto.
print("se crea el archivo que manejara la excepciones")
print("se crea el archivo que almacenara la clase cliente ")
print("se crea el archivo que logger.py")
print("se crea el archivo main.py")
print("se crea el archivo entidad.py")

# La lista muestra los nombres de las ramas usadas en el proyecto.
ramas_equipo = ["main", "develop", "feature/fabian", "feature/alejandro"]
print(f"Ramas activas en el repositorio: {len(ramas_equipo)}")

# Esta lista reúne los comandos de Git que se mostrarán como ejemplo.
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
# enumerate agrega un número para presentar cada comando en orden.
for i, comando in enumerate(comandos_git, start=1):
  print(f"{i}. {comando}")

# Se agregan comandos para consultar y guardar cambios e historial.
comandos_git.append("git stash")
comandos_git.append("git log")
comandos_git.append("git diff")

print("Nuevos items:")
# Se recorre la lista actualizada para mostrar todos sus elementos.
for comando in comandos_git:
  print(comando)

# Se verifica si el comando de historial está incluido en la lista.
print("¿Existe git log?:", verificar_comando(comandos_git, "git log"))
