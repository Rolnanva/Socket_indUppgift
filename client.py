import socket
import threading

# Funktion för att ta emot meddelanden från servern
def receive_messages(client_socket, name, color):
    while True:
        try:
            message = client_socket.recv(1024).decode("utf-8")
            print(message)
        except ConnectionAbortedError:
            print("[SERVER] Anslutningen till servern är avbruten.")
            break
        except Exception as e:
            print(f"[FEL] Ett oväntat fel inträffade: {e}")
            break

# Funktion för att skicka meddelanden till servern och visa egna meddelanden lokalt
def send_messages(client_socket, name, color):
    while True:
        message = input()
        formatted_message = f"{color}{name}: {message}\033[0m"  # Format för eget meddelande med färg
        try:
            client_socket.send(message.encode("utf-8"))
            print(formatted_message)  # Visa eget meddelande på skärmen direkt
        except BrokenPipeError:
            print("[FEL] Kunde inte skicka meddelande till servern.")
            break

# Huvudfunktion för att starta klienten
def start_client(host="127.0.0.1", port=5555):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((host, port))
        print(f"[ANSLUTEN] Ansluten till servern på {host}:{port}")

        # Ange användarnamn
        name = input("Ange ditt namn: ")
        client_socket.send(name.encode("utf-8"))

        # Tilldela en slumpmässig färg för klientens egna meddelanden
        colors = ["\033[91m", "\033[92m", "\033[93m", "\033[94m", "\033[95m", "\033[96m", "\033[97m"]
        color = colors[hash(name) % len(colors)]  # Tilldela färg baserat på hash av namn

        # Starta trådar för att skicka och ta emot meddelanden
        receive_thread = threading.Thread(target=receive_messages, args=(client_socket, name, color))
        send_thread = threading.Thread(target=send_messages, args=(client_socket, name, color))
        
        receive_thread.start()
        send_thread.start()

        receive_thread.join()
        send_thread.join()

    except ConnectionRefusedError:
        print("[FEL] Kunde inte ansluta till servern. Kontrollera om servern är igång.")
    finally:
        client_socket.close()

# Starta klienten om filen körs direkt
if __name__ == "__main__":
    start_client()
