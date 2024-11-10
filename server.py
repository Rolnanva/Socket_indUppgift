import socket
import threading
import random

# Skapa en lista för att hålla reda på alla anslutna klienter och deras information (namn och färg)
clients = []

# Färgkoder för slumpmässigt val av färg för varje klient
colors = ["\033[91m", "\033[92m", "\033[93m", "\033[94m", "\033[95m", "\033[96m", "\033[97m"]

# Funktion för att hantera varje ansluten klient
def handle_client(client_socket, client_address):
    # Be om klientens namn
    client_socket.send("Ange ditt namn: ".encode("utf-8"))
    name = client_socket.recv(1024).decode("utf-8")

    # Tilldela slumpmässig färg
    color = random.choice(colors)
    client_info = {"socket": client_socket, "address": client_address, "name": name, "color": color}
    clients.append(client_info)

    print(f"[NY ANSLUTNING] {client_address} ansluten som {name}.")

    # Informera alla andra klienter om den nya anslutningen
    broadcast(f"{name} har anslutit till chatten!", client_socket)

    try:
        while True:
            # Ta emot meddelande från klienten
            message = client_socket.recv(1024).decode("utf-8")
            if not message:
                break
            # Skriv ut meddelande och skicka det till alla andra
            formatted_message = f"{color}{name}: {message}\033[0m"
            print(formatted_message)
            broadcast(formatted_message, client_socket)
    except ConnectionResetError:
        print(f"[FEL] Anslutning med {client_address} förlorad.")
    finally:
        # Ta bort klienten från listan och informera andra klienter
        clients.remove(client_info)
        client_socket.close()
        broadcast(f"{name} har lämnat chatten.", None)
        print(f"[FRÅNLOGGNING] {client_address} ({name}) frånloggad.")

# Funktion för att skicka meddelandet till alla anslutna klienter
def broadcast(message, sender_socket):
    for client in clients:
        if client["socket"] != sender_socket:
            try:
                client["socket"].send(message.encode("utf-8"))
            except BrokenPipeError:
                print(f"[FEL] Kunde inte skicka till en klient.")

# Huvudfunktion för att starta servern
def start_server(host="127.0.0.1", port=5555):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()
    print(f"[SERVER STARTAD] Lyssnar på {host}:{port}")

    while True:
        client_socket, client_address = server.accept()
        # Starta en ny tråd för varje ansluten klient
        thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        thread.start()
        print(f"[AKTIVA ANSLUTNINGAR] {threading.active_count() - 1}")

# Starta servern om filen körs direkt
if __name__ == "__main__":
    start_server()
