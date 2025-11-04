import streamlit as st
import io
import fitz  # PyMuPDF
from model_loader import load_model
from summarizer import summarize_text
from translator import translate_to_indonesian

# ======================
# LOAD MODEL
# ======================
@st.cache_resource
def get_model():
    return load_model()

model = get_model()

# ======================
# FUNGSI EKSTRAKSI PDF
# ======================
def extract_text_from_pdf(file):
    """Mengambil teks dari seluruh halaman PDF"""
    text = ""
    with fitz.open(stream=file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text("text") + "\n"
    return text.strip()

# ======================
# FRONTEND
# ======================
st.set_page_config(page_title="Indonesian Text Summarizer (Sumy + MiniLM)", layout="centered")

st.title("Multilingual Text Summarizer (Sumy + MiniLM)")
st.write("""
Aplikasi ini menggunakan **SentenceTransformer** (`paraphrase-multilingual-MiniLM-L12-v2`)
dan **Sumy (TextRank)**.
""")

# Input text area
input_text = st.text_area("Masukkan teks di sini:", height=250)

# Upload file
uploaded_file = st.file_uploader("Atau unggah file (.txt atau .pdf)", type=["txt", "pdf"])

if uploaded_file is not None:
    if uploaded_file.type == "application/pdf":
        with st.spinner("Mengekstrak teks dari PDF..."):
            input_text = extract_text_from_pdf(uploaded_file)
    else:
        input_text = uploaded_file.read().decode("utf-8")

# Pilihan panjang ringkasan
summary_length = st.selectbox(
    "Pilih panjang ringkasan:",
    options=["Pendek (3 kalimat)", "Sedang (5 kalimat)", "Panjang (8 kalimat)"],
    index=1
)
length_map = {"Pendek (3 kalimat)": 3, "Sedang (5 kalimat)": 5, "Panjang (8 kalimat)": 8}

# Tombol ringkas
if st.button("🔍 Ringkas Teks"):
    if input_text.strip():
        with st.spinner("Sedang meringkas..."):
            summary_en = summarize_text(input_text, model, num_sentences=length_map[summary_length])

        with st.spinner("Menerjemahkan ke Bahasa Indonesia..."):
            summary_id = translate_to_indonesian(summary_en)

        st.success("Ringkasan selesai!")
        st.subheader("Hasil Ringkasan (Bahasa Indonesia):")
        st.text_area("Output:", summary_id, height=250)

        # Unduh hasil ringkasan
        buffer = io.BytesIO()
        buffer.write(summary_id.encode("utf-8"))
        buffer.seek(0)
        st.download_button(
            label="Unduh Ringkasan (.txt)",
            data=buffer,
            file_name="ringkasan.txt",
            mime="text/plain"
        )
    else:
        st.warning("Masukkan teks terlebih dahulu sebelum meringkas.")

st.markdown("---")
st.caption("Model: paraphrase-multilingual-MiniLM-L12-v2 + Sumy TextRank + GoogleTranslator.")
