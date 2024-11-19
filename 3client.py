import socket
import time
from pynput import keyboard

# Indirizzo IP e porta dell'Alphabot a cui ci connettiamo
SERVER_ADDRESS = ("192.168.1.140", 9090)
BUFFER_SIZE = 4096

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # Creazione del socket TCP per la comunicazione con il server
s.connect(SERVER_ADDRESS)   # Connessione al server

comandi = ["w", "a", "s", "d"]  # Lista dei comandi validi che possono essere inviati ('w', 'a', 's', 'd')
ultimo_comando = None  # Variabile globale per tenere traccia dell'ultimo comando inviato

def on_press(key):
    '''Gestisce la pressione di un tasto. Invia il comando in minuscolo se il tasto è valido e diverso dall'ultimo inviato.'''

    global ultimo_comando

    if key.char != ultimo_comando and key.char in comandi:  # Controlla se il tasto corrente è diverso dall'ultimo comando inviato e fa parte dei comandi
        s.sendall(key.char.lower().encode())  # Invia il tasto in minuscolo al server per indicare la pressione
        ultimo_comando = key.char  # Aggiorna l'ultimo comando inviato
        time.sleep(0.05)  # Pausa per evitare di sovraccaricare la rete con troppi comandi consecutivi

def on_release(key):
    '''Gestisce il rilascio di un tasto. Invia il comando in maiuscolo se il tasto è valido.'''

    global ultimo_comando

    if key.char in comandi:  # Controlla se il tasto rilasciato è uno dei comandi validi
        ultimo_comando = None  # Resetta l'ultimo comando inviato
        s.sendall(key.char.upper().encode())  # Invia il tasto in maiuscolo al server per indicare il rilascio
        time.sleep(0.05)

def start_listener():
    '''Avvia il listener della tastiera per monitorare la pressione e il rilascio dei tasti.'''

    # Listener per monitorare la pressione e il rilascio dei tasti
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

def main():
    start_listener()  # Avvia il listener della tastiera
    s.close()  # Chiude il socket al termine del programma

if __name__ == "__main__":
    main()
