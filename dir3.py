# Importiamo le librerie necessarie
import socket
import tkinter as tk

# Funzione per printare il messaggio di errore
def errore(messaggio):
    print(messaggio)
    exit(0)

# Funzione per la connessione e la ricezione del feed
def datafeed():
    porta = 10005
    buffersize = 256
    comando = "SUBPRZALL UCG\n"
    host = "127.0.0.1"

    # Socket
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sfeed: # Usiamo la funzione with per gestire il socket
            # Connessione al socket
            try:
                sfeed.connect((host, porta))
            except socket.error as err:
                errore(f"errore di connessione: {err}")

            # Invio comando
            try:
                sfeed.sendall(comando.encode('utf-8'))
            except socket.error as err:
                errore(f"errore di invio del comando: {err}")

            # Ricezione
            while 1:
                try:
                    response = sfeed.recv(buffersize)
                    #print("utf"+response.decode('utf-8'))
                except socket.error as err:
                    errore(f"errore di ricezione del datafeed: {err}")

                if response.startswith(b"BIDASK"):  # Check if the response is a bid/ask message
                    data = response.decode('utf-8').split(";")  # Split the response by semicolons
                    print(data)
                    name=data[1]
                    bid = data[5]  # Get the bid price
                    ask = data[8]  # Get the ask price
                    print(f"Bid: {bid}, Ask: {ask}")  # Print the bid and ask prices
                    # Aggiorniamo il testo della etichetta con i dati ricevuti
                    label.config(text="{} Bid: {} Ask: {}".format(name, bid, ask)) # Usiamo la funzione format per creare la stringa
            window.after(1000, datafeed) # Usiamo la funzione after per richiamare la funzione datafeed ogni secondo

    except socket.error as err: # Chiudiamo il blocco try con un except
        errore(f"errore nel creare il socket: {err}") # Gestiamo l'errore


# Creiamo una finestra grafica usando la libreria tkinter
window = tk.Tk()
window.title("DataFeed UCG")

# Creiamo una etichetta vuota dove mostrare i dati
label = tk.Label(window, text="")
label.pack()

datafeed() # Chiamiamo la funzione datafeed una volta

window.mainloop() # Avviamo il loop principale della finestra grafica
