import socket

# Obtém o nome da máquina
hostname = socket.gethostname()

# Obtém o IP local
ip_local = socket.gethostbyname(hostname)

print(f"{ip_local}")
