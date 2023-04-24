# Importare le librerie
import pandas as pd
import numpy as np
import requests

# Definire il codice del future e la data di scadenza
future_code = "eu.ikm3"
future_date = "2023-06-10"

# Ottenere il prezzo del future dalla piattaforma Eurex
future_url = f"https://www.eurex.com/ex-en/markets/int/fix/government-bonds/Long-Term-Euro-BTP-Futures-{future_code}-137382"
future_response = requests.get(future_url)
future_data = pd.read_html(future_response.text, header=0)[0] # Aggiungere il parametro header=0

# Stampare il dataframe future_data
# print(future_data)


# Ottenere i titoli sottostanti dal file excel
bond_data = pd.read_excel("btp.xlsx")

# Ottenere il fattore di conversione e il prezzo spot dei titoli sottostanti
bond_data["Fattore di conversione"] = bond_data["ConvFac"].astype(float) # Usare la colonna ConvFac
bond_data["Prezzo spot"] = (bond_data["Bid"] + bond_data["Ask"]) / 2 # Calcolare il prezzo medio tra bid e ask

# Ottenere il tasso di interesse effettivo sul mercato monetario (Euribor a 3 mesi)
rate_url = "https://www.global-rates.com/interest-rates/euribor/euribor.aspx?y=2023"
rate_response = requests.get(rate_url)
# Convertire la colonna data in formato datetime
rate_data["Date"] = pd.to_datetime(rate_data["Current interest rates"], format="%B %d %Y") # Usare la colonna Current interest rates
rate_data.columns = rate_data.iloc[0] # Usare la prima riga come intestazione
rate_data = rate_data.iloc[1:] # Rimuovere la prima riga
print(rate_data)
rate_data["Date"] = pd.to_datetime(rate_data["Date"], format="%d-%m-%Y") # Convertire la colonna data in formato datetime
rate_data["Euribor 3 months"] = rate_data["Euribor 3 months"].str.replace("%", "").astype(float) / 100 # Convertire la colonna tasso in formato numerico
rate_date = pd.to_datetime(future_date) - pd.Timedelta(days=90) # Calcolare la data a 3 mesi prima della scadenza del future
rate_value = rate_data.loc[rate_data["Date"] == rate_date, "Euribor 3 months"].values[0] # Trovare il valore del tasso corrispondente

# Calcolare il prezzo dei titoli sottostanti sul termine
days_to_maturity = (pd.to_datetime(future_date) - pd.to_datetime("today")).days # Calcolare i giorni alla scadenza del future
bond_data["Prezzo sul termine"] = bond_data["Prezzo spot"] / (1 + rate_value * days_to_maturity / 365) # Applicare la formula del prezzo sul termine

# Calcolare il prezzo dei titoli sottostanti corretti per il fattore di conversione
bond_data["Prezzo corretto"] = bond_data["Prezzo sul termine"] / bond_data["Fattore di conversione"] # Dividere il prezzo sul termine per il fattore di conversione

# Calcolare la net basis tra il prezzo dei titoli sottostanti corretti e il prezzo del future
bond_data["Net basis"] = bond_data["Prezzo corretto"] - future_price # Sottrarre il prezzo del future dal prezzo corretto

# Trovare il CTD come il titolo con la net basis più negativa
ctd_index = bond_data["Net basis"].idxmin() # Trovare l'indice della riga con la net basis minima
ctd_name = bond_data.loc[ctd_index, "#Contract"] # Usare la colonna #Contract

# Stampare il dataframe completo
print(bond_data)

# Stampare le prime 5 righe del dataframe
print(bond_data.head())
