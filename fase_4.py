print("Iniciando proceso...")
print("Cargando datos...")
print("Proceso finalizado con éxito.")

print("Se agrega a Fabian Andres al proyecto en su propia rama")
print("Se agrega a Alejandro Reyes al proyecto con su propia rama")
 
print("se notifica a Alejandro al foro que ya debio haber recibido la invitacion a colaborar al repo")


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
for comando in comandos_git:
    print(comando)
 
# Agregar un nuevo comando a la lista
comandos_git.append("git stash")

print("Nuevos items:")
for comando in comandos_git:
    print(comando)
