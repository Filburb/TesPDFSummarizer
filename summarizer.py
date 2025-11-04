from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer
import re

def clean_text(text):
    """
    Membersihkan teks dari elemen yang tidak perlu agar ringkasan lebih alami.
    """
    # Hapus nomor bab/subbagian seperti 3.1, 4.3.2, 2.5.1
    text = re.sub(r"\b\d+(\.\d+)+\b", "", text)

    # Hapus angka di awal baris (misal: "1 Pendahuluan")
    text = re.sub(r"^\d+\s+", "", text, flags=re.MULTILINE)

    # Hapus spasi ganda dan tanda baca berlebih
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\s([?.!,;:])", r"\1", text)

    return text.strip()


def summarize_text(text, model, num_sentences=5):
    """
    Ringkasan berbasis Sumy (TextRank) + model loader.
    """
    # Bersihkan teks
    text = clean_text(text)

    # Parser bahasa Indonesia
    parser = PlaintextParser.from_string(text, Tokenizer("english"))

    # Gunakan TextRank Summarizer
    summarizer = TextRankSummarizer()
    summary_sentences = summarizer(parser.document, num_sentences)

    # Gabungkan kalimat ringkasan
    summary = " ".join(str(sentence) for sentence in summary_sentences)
    return summary.strip()
