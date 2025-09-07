import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

required_packages = [
    "keyboard",
    "pywin32"
]
# Instalar pacotes Python
for package in required_packages:
    install(package)

print("Todos os pacotes necessários foram instalados com sucesso!")