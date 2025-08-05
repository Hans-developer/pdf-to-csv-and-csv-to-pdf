import streamlit as st
import pandas as pd
import fitz  # PyMuPDF
from fpdf import FPDF

# Título de la aplicación
st.title("Convertir PDF a CSV y CSV a PDF")

# Función para convertir PDF a DataFrame
def pdf_to_dataframe(file):
    text = ''
    with fitz.open(file) as pdf:
        for page in pdf:
            text += page.get_text() + '\n'
    # Convertir el texto a un DataFrame (puedes personalizar esto según el formato)
    data = [line.split() for line in text.split('\n') if line]
    return pd.DataFrame(data)

# Función para convertir DataFrame a PDF
def dataframe_to_pdf(df):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    for row in df.values:
        pdf.cell(200, 10, txt=' | '.join(map(str, row)), ln=True)

    return pdf.output(dest='S').encode('latin1')

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

# Sección para convertir CSV a PDF
st.subheader("Convertir CSV a PDF")
uploaded_csv = st.file_uploader("Sube tu archivo CSV", type=["csv"])

if uploaded_csv is not None:
    df_csv = pd.read_csv(uploaded_csv)
    st.write("Datos del archivo CSV:")
    st.dataframe(df_csv)

    pdf_data = dataframe_to_pdf(df_csv)
    st.download_button(
        label="Descargar como PDF",
        data=pdf_data,
        file_name='archivo_convertido.pdf',
        mime='application/pdf'
    )
