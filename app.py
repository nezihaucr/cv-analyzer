import streamlit as st
import pytesseract
from PIL import Image
import pdfplumber
import re
from pdf2image import convert_from_bytes
text = ""

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"



roles = {
    "Machine Learning Engineer": ["python", "tensorflow", "pytorch", "machine learning", "nlp"],
    "Data Scientist": ["python", "sql", "statistics", "data analysis"],
    "Backend Developer": ["java", "api", "database", "docker"],
    "Cyber Security": ["network security", "penetration testing", "linux", "cryptography"],
    "Prompt Engineer": ["llm", "prompt design", "chatgpt", "nlp"],
    "Frontend Developer": ["html", "css", "javascript", "react"]
}


# CV analiz fonksiyonu
def analyze_cv(text, selected_skills):
    text = text.lower()
    text = text.replace("\n", " ")
    text = re.sub(r'[^a-zA-Z0-9 ]', ' ', text)  # 🔥 EKLE
    
    found = []
    missing = []
    
    for skill in selected_skills:
        if skill in text:
            found.append(skill)
        else:
            missing.append(skill)
    
    score = len(found) / len(selected_skills) * 100
    
    return found, missing, score
# Feedback fonksiyonu
def generate_feedback(score, missing):
    if score > 70:
        level = "Güçlü CV 👍"
    elif score > 40:
        level = "Orta seviye CV ⚠️"
    else:
        level = "Zayıf CV ❌"
    
    suggestion = "Eksik skill'ler: " + ", ".join(missing[:5])
    
    return level, suggestion

def ai_comment(score):
    if score > 70:
        return "CV'in teknik olarak güçlü görünüyor. Küçük iyileştirmelerle çok daha rekabetçi olabilir."
    elif score > 40:
        return "CV'in orta seviyede. Bazı kritik teknik skill'leri ekleyerek profilini güçlendirebilirsin."
    else:
        return "CV'in başlangıç seviyesinde. Daha fazla teknik beceri eklemen önemli olacaktır."
    
    

def compare_with_job(cv_text, job_text, skills):
    job_text = job_text.lower()
    
    matched = []
    missing = []
    
    for skill in skills:
        if skill in job_text:
            if skill in cv_text:
                matched.append(skill)
            else:
                missing.append(skill)
    
    return matched, missing    


# UI
st.title("AI CV Analyzer 🚀")
st.write("CV metnini gir, analiz edelim 👇")

role = st.selectbox(
    "Hangi role başvuruyorsun?",
    list(roles.keys())
)

uploaded_file = st.file_uploader("📄 CV yükle (PDF)", type="pdf")

if uploaded_file:
    text = ""
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""

    st.success("CV başarıyla yüklendi!")

# 👇 BURAYA EKLE
st.info("Not: Scan edilmiş PDF'ler için image yükleme önerilir.")


image_file = st.file_uploader("🖼️ CV yükle (Image)", type=["png", "jpg", "jpeg"])

if image_file:
    image = Image.open(image_file)
    text = pytesseract.image_to_string(image)
    st.image(image, caption="Yüklenen CV", use_column_width=True)
    st.success("Görselden metin çıkarıldı!")    

text_input = st.text_area("CV Metni (manuel giriş)")

if text_input:
    text = text_input
    
job_desc = st.text_area("💼 İş ilanını yapıştır (opsiyonel)")

if st.button("Analiz Et"):

    if not text:
        st.error("Lütfen CV gir veya yükle ❗")
        st.stop() 

    selected_skills = roles[role]
    found, missing, score = analyze_cv(text, selected_skills)
    level, suggestion = generate_feedback(score, missing)

    st.subheader("📊 Sonuçlar")
    st.progress(int(score))
    st.metric(label="CV Skoru", value=f"{round(score,2)}%")
    st.write("Seviye:", level)

    st.subheader("🧠 AI Yorumu")
    st.write(ai_comment(score))

    st.subheader("✅ Sahip Olduğun Skill'ler")
    for s in found:
        st.write("✔️", s)

    st.subheader("🚀 Geliştirmen Gerekenler")
    for s in missing[:5]:
        st.write("➕", s)

    # 🔥 BURASI ÖNEMLİ
    if job_desc:
        matched, missing_job = compare_with_job(text.lower(), job_desc, selected_skills)

        st.subheader("🎯 İş İlanına Uyum")

        st.write("✔️ Uyumlu skill'ler:")
        for m in matched:
            st.write("✔️", m)

        st.write("❌ Eksik skill'ler:")
        for m in missing_job:
            st.write("➕", m)

          

