import streamlit as st
import pandas as pd
import fitz  # PyMuPDF

# Título de la aplicación
st.title("Convertir PDF a CSV")

# Función para convertir PDF a DataFrame
def pdf_to_dataframe(file):
    text = ''
    with fitz.open(file) as pdf:
        for page in pdf:
            text += page.get_text() + '\n'
    # Convertir el texto a un DataFrame (puedes personalizar esto según el formato)
    data = [line.split() for line in text.split('\n') if line]
    return pd.DataFrame(data)

# Sección para convertir PDF a CSV
st.subheader("Convertir PDF a CSV")
uploaded_pdf = st.file_uploader("Sube tu archivo PDF", type=["pdf"])

if uploaded_pdf is not None:
    df = pdf_to_dataframe(uploaded_pdf)
    st.write("Datos extraídos del PDF:")
    st.dataframe(df)

    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Descargar como CSV",
        data=csv,
        file_name='archivo_convertido.csv',
        mime='text/csv'
    )
