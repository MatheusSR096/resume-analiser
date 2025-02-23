import streamlit as st
import fitz
import base64
import re  # Usado para limpar o HTML, se necessário
from analiser_ai import analyze_resume_complete  # Atualizado para usar a análise completa

st.set_page_config(page_title="Analisador de Currículos IA", layout="wide")

st.markdown("""
<style>
.reportview-container { background: #f0f2f6; }
.resume-box {
    padding: 20px;
    background: #1e1e1e;
    color: #ffffff;
    border-radius: 10px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    margin: 10px 0;
    font-family: Arial, sans-serif;
    white-space: pre-wrap;
    overflow-wrap: break-word;
}
.analysis-section { 
    margin: 20px 0; 
    padding: 15px; 
    border-left: 4px solid;
}
</style>
""", unsafe_allow_html=True)

st.title("📄 Analisador Inteligente de Currículos")
st.markdown("""
Envie seu currículo em PDF e receba uma análise completa e detalhada com:

🟢 Pontos fortes  
🟡 Oportunidades de melhoria  
🔴 Aspectos críticos
""")

with st.expander("📌 Instruções Rápidas"):
    st.markdown("""
    1. Clique em "Browse files" ou arraste seu PDF para a área pontilhada  
    2. Aguarde o carregamento do documento  
    3. Clique em "Analisar Currículo"  
    4. Visualize sua análise completa e detalhada  
    """)

uploaded_file = st.file_uploader("Carregar currículo", type=["pdf"], label_visibility="hidden")

# Inicializa as variáveis para o texto extraído e a visualização do PDF
resume_text = ""
pdf_display = ""

if uploaded_file is not None:
    # Lê os bytes do arquivo enviado
    file_bytes = uploaded_file.read()
    
    # Cria a visualização exata do PDF usando Base64
    base64_pdf = base64.b64encode(file_bytes).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="800" type="application/pdf"></iframe>'
    
    # Extrai o texto do PDF utilizando PyMuPDF (fitz)
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    resume_text = "\n".join([page.get_text("text") for page in doc])
    
st.markdown("<hr>", unsafe_allow_html=True)

# Exibição lado a lado: PDF e texto extraído
if pdf_display and resume_text:
    cols = st.columns(2)
    with cols[0]:
        st.subheader("📄 Visualização do PDF")
        st.markdown(pdf_display, unsafe_allow_html=True)
    with cols[1]:
        st.subheader("📋 Texto Extraído do Currículo")
        st.markdown(f"""
        <div class="resume-box">
            <pre>{resume_text}</pre>
        </div>
        """, unsafe_allow_html=True)

# Botão para análise completa
if resume_text:
    if st.button("🚀 Analisar Currículo", use_container_width=True):
        with st.spinner("Analisando conteúdo..."):
            try:
                # Chama a função que integra os múltiplos prompts de análise
                analysis = analyze_resume_complete(resume_text)
                # Limpa eventuais tags <style> que possam ter sido inseridas na resposta
                analysis_cleaned = re.sub(r'<style.*?>.*?</style>', '', analysis, flags=re.DOTALL).strip()
                
                st.subheader("📊 Análise Completa")
                st.markdown(f"""
                <div class="analysis-section">
                    {analysis_cleaned}
                </div>
                """, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Erro na análise: {str(e)}")
