import socket
import threading
import argparse

# Lista para almacenar los puertos abiertos
open_ports = []

# Función para comprobar si un puerto está abierto
def scan_port(ip, port, silent=False):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)  # Establecer un tiempo de espera
        result = sock.connect_ex((ip, port))
        if result == 0:
            open_ports.append(port)  # Agregar puerto abierto a la lista
            if not silent:
                print(f"Puerto {port} está abierto.")
        sock.close()
    except socket.error:
        if not silent:
            print(f"Puerto {port} está cerrado.")

# Función que escanea los puertos en el rango especificado
def scan_ports(ip, start_port, end_port, silent=False, threads=1000, verbose=False, open_only=False):
    print(f"Iniciando escaneo en {ip} desde el puerto {start_port} hasta el puerto {end_port}")
    
    # Crear hilos para el escaneo
    def thread_scan_port(port):
        if verbose:
            print(f"Escaneando puerto {port}...")
        scan_port(ip, port, silent)
    
    threads_list = []
    for port in range(start_port, end_port + 1):
        # Crear un hilo para cada puerto
        thread = threading.Thread(target=thread_scan_port, args=(port,))
        threads_list.append(thread)
        # Controlar el número de hilos simultáneos
        if len(threads_list) >= threads:
            for t in threads_list:
                t.start()
            for t in threads_list:
                t.join()
            threads_list = []
    
    # Iniciar los hilos restantes
    for t in threads_list:
        t.start()
    for t in threads_list:
        t.join()

    # Mostrar solo los puertos abiertos si la opción --open está activada
    if open_only:
        print("\nPuertos abiertos encontrados:")
        if open_ports:
            for port in open_ports:
                print(f"Puerto {port} está abierto.")
        else:
            print("No se encontraron puertos abiertos.")
    else:
        print("Escaneo finalizado.")

# Función principal para parsear argumentos
def main():
    parser = argparse.ArgumentParser(description="Herramienta de escaneo de puertos.")
    parser.add_argument("--ip", type=str, required=True, help="Dirección IP del objetivo.")
    parser.add_argument("--open", action="store_true", help="Mostrar solo los puertos abiertos.")
    parser.add_argument("--silent", action="store_true", help="Escaneo sigiloso (sin mostrar resultados).")
    parser.add_argument("--verbose", action="store_true", help="Mostrar información detallada durante el escaneo.")
    parser.add_argument("--threads", type=int, default=1000, choices=range(1000, 5001), help="Número de hilos (de 1000 a 5000).")
    parser.add_argument("--start", type=int, default=1, help="Puerto inicial (por defecto 1).")
    parser.add_argument("--end", type=int, default=65535, help="Puerto final (por defecto 65535).")

    args = parser.parse_args()

    # Iniciar el escaneo de puertos
    scan_ports(args.ip, args.start, args.end, silent=args.silent, threads=args.threads, verbose=args.verbose, open_only=args.open)

if __name__ == "__main__":
    main()
