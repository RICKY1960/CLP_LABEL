import streamlit as st
import pandas as pd
import os

# Configurazione della pagina
st.set_page_config(
    page_title="Gestione Etichette CLP",
    page_icon="🏷️",
    layout="centered"
)

# Funzione per caricare il database delle fragranze
@st.cache_data
def carica_database():
    # Sostituisci "fragranze.csv" o "database.xlsx" con il nome reale del file che usi
    file_path = "fragranze.csv"
    
    if os.path.exists(file_path):
        try:
            # Se è un file CSV
            df = pd.read_csv(file_path)
            return df
        except Exception as e:
            st.error(fErrore nella lettura del file: {e}")
            return pd.DataFrame()
    else:
        # Dati di esempio se il file non esiste ancora (così l'app non si blocca)
        dati_esempio = {
            "Nome Fragranza": ["Vaniglia Nera", "Lavanda Provenzale", "Ambra e Spezie"],
            "Codice": ["VNL-01", "LAV-02", "AMB-03 %"],
            "Percentuale Max (%)": [10.0, 12.5, 8.0],
            "Frasi H": ["H317: Può provocare una reazione allergica cutanea.", "H319: Provoca grave irritazione oculare.", "H412: Nocivo per gli organismi acquatici."],
            "Allergeni": ["Linalool, Coumarin", "Linalool, Limonene", "Eugenol, Cinnamal"]
        }
        return pd.DataFrame(dati_esempio)

def main():
    st.title("🏷️ Gestione & Consultazione Etichette CLP")
    st.write("Portale mobile per la consultazione delle fragranze e conformità.")

    # Caricamento dati
    df_fragranze = carica_database()

    # Menu di navigazione laterale
    st.sidebar.header("Navigazione")
    scelta = st.sidebar.radio("Seleziona sezione:", ["Consultazione Database", "Nuova Etichetta CLP"])

    if scelta == "Consultazione Database":
        st.subheader("🔍 Cerca Scheda Fragranza")
        
        if not df_fragranze.empty:
            # Barra di ricerca interattiva
            ricerca = st.text_input("Cerca per nome fragranza o codice:")
            
            if ricerca:
                # Filtra il dataframe in base alla ricerca (ignorando maiuscole/minuscole)
                risultati = df_fragranze[
                    df_fragranze.astype(str).apply(lambda row: row.str.contains(ricerca, case=False, na=False)).any(axis=1)
                ]
            else:
                risultati = df_fragranze

            st.write(f"Trovate **{len(risultati)}** fragranze nel database:")
            
            # Mostra i risultati in modo pulito e scorrevole per il telefono
            for index, row in risultati.iterrows():
                with st.expander(f"📌 {row.get('Nome Fragranza', 'Fragranza')} ({row.get('Codice', '')})"):
                    st.markdown(f"**Percentuale Max:** {row.get('Percentuale Max (%)', 'N/D')}%")
                    st.markdown(f"**Frasi H / Pericolo:**\n{row.get('Frasi H', 'N/D')}")
                    st.markdown(f"**Allergeni principali:**\n{row.get('Allergeni', 'N/D')}")
        else:
            st.warning("Il database delle fragranze è attualmente vuoto.")

    elif scelta == "Nuova Etichetta CLP":
        st.subheader("➕ Genera Nuova Etichetta")
        
        with st.form("form_clp"):
            # Selezione fragranza dal database esistente se disponibile
            nomi_disponibili = df_fragranze['Nome Fragranza'].tolist() if not df_fragranze.empty else ["Personalizzata"]
            fragranza_scelta = st.selectbox("Seleziona Fragranza", nomi_disponibili)
            
            percentuale = st.slider("Percentuale Fragranza (%)", 1.0, 25.0, 10.0, 0.5)
            pericolo_attenzione = st.selectbox("Parola d'avvertenza:", ["ATTENZIONE", "PERICOLO", "Nessuna"])
            
            invia = st.form_submit_button("Genera Anteprima Etichetta")
            
            if invia:
                st.success(f"Etichetta generata con successo per: {fragranza_scelta} al {percentuale}%!")
                st.markdown("---")
                st.markdown(f"**Anteprima Testo CLP:**\n\nContiene {fragranza_scelta} al {percentuale}%. Può provocare una reazione allergica. Tenere fuori dalla portata dei bambini.")

if __name__ == "__main__":
    main()