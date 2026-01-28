import streamlit as st
import google.generativeai as genai # Jetzt für Google Gemini
from docx import Document
import io

# 1. SETUP: Wir holen den Gemini Key und den Prompt aus den Secrets
gemini_key = st.secrets["GEMINI_API_KEY"]
geheimer_system_prompt = st.secrets["SYSTEM_PROMPT"]

# Gemini konfigurieren
genai.configure(api_key=gemini_key)
model = genai.GenerativeModel('gemini-1.5-pro') # Das leistungsstarke Modell

st.set_page_config(page_title="KI-Mietanalyst (Gemini Demo)", layout="centered")
st.title("⚖️ KI-Mietwert-Analyst (Powered by Gemini)")

user_input = st.text_area("Falldaten hier einfügen:", height=200)

if st.button("Analyse & Dokument generieren"):
    if not user_input:
        st.warning("Bitte Daten eingeben.")
    else:
        with st.spinner("Gemini analysiert..."):
            # Wir kombinieren Prompt und User-Input für Gemini
            full_prompt = f"{geheimer_system_prompt}\n\nHIER SIND DIE FALLDATEN:\n{user_input}"
            response = model.generate_content(full_prompt)
            
            ergebnis_text = response.text
            
            st.subheader("Analyse-Ergebnis")
            st.markdown(ergebnis_text)
            
            # Word-Dokument erstellen (bleibt gleich)
            doc = Document()
            doc.add_heading('Analyse & Schriftsatz-Entwurf', 0)
            doc.add_paragraph(ergebnis_text)
            
            buffer = io.BytesIO()
            doc.save(buffer)
            buffer.seek(0)
            
            st.download_button(
                label="📄 Word-Datei herunterladen",
                data=buffer,
                file_name="Mietwert_Analyse.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
