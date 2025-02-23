from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.schema import StrOutputParser
import os
from dotenv import load_dotenv
load_dotenv()
groq_key = os.getenv("GROQ_API_KEY")

# --- Prompt principal (mantido conforme já configurado) ---
prompt_template = """
Você é um especialista em análise de currículos. Sua resposta **DEVE SER ESTRUTURADA** no seguinte formato, com cores específicas para cada seção:

Na cor verde em markdown:
✅ <span style="color:green"><strong>Pontos Fortes</strong></span>  
- <span style="color:green">[Coloque aqui os pontos positivos do currículo]</span>  

Na cor amarela em markdown:
⚠️ <span style="color:orange"><strong>Oportunidades de Melhoria</strong></span>  
- <span style="color:orange">[Coloque aqui as sugestões de melhoria]</span>  

Na cor vermelha em markdown: 
❌ <span style="color:red"><strong>Aspectos Ruins</strong></span>  
- <span style="color:red">[Coloque aqui os problemas encontrados]</span>  

Além disso, analise os seguintes aspectos do currículo:
- **Organização e Estrutura:** Verifique se o currículo está organizado, com seções claramente definidas e informações bem distribuídas.
- **Clareza e Objetividade:** Avalie se as informações são apresentadas de forma clara, objetiva e sem ambiguidades.
- **Conteúdo Relevante:** Considere a pertinência das informações apresentadas para a área de atuação e os objetivos profissionais.
- **Formatação e Design:** Analise a formatação, legibilidade, uso de fontes, cores e consistência visual.
- **Experiência e Habilidades:** Verifique se as experiências, certificações e habilidades estão descritas de forma que evidenciem competências importantes.
- **Inovação e Impacto:** Considere se o currículo destaca projetos ou realizações de forma impactante e inovadora.

Com base na análise desses critérios, **atribua uma nota final de 0 a 100** ao currículo. A nota deve refletir a qualidade geral e a adequação do currículo ao mercado de trabalho.

**Importante:**  
- **Não altere as cores e formatações acima.**
- **Sempre utilize listas estruturadas e curtas.**
- **Retorne a resposta em formato HTML pronto para renderização.**
- **Traga a resposta no mesmo idioma que o usuário fizer a pergunta.**

### Currículo:
{resume_text}
"""

prompt = PromptTemplate(
    template=prompt_template,
    input_variables=["resume_text"],
)

llm = ChatGroq(temperature=0.2, model="llama-3.3-70b-versatile", api_key=groq_key)
chain = prompt | llm | StrOutputParser()

def analyze_resume(resume_text):
    return chain.invoke(input=resume_text)

# --- Prompts adicionais (em português) ---

# Prompt para Resumo
summary_prompt_template = """
Responda em português.
Preciso de um resumo detalhado do currículo abaixo e, ao final, uma conclusão.

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
{resume_text}
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"""
summary_prompt = PromptTemplate(
    template=summary_prompt_template,
    input_variables=["resume_text"],
)

# Prompt para Pontos Fortes
strength_prompt_template = """
Responda em português.
Preciso de uma análise detalhada e explicação dos pontos fortes do currículo abaixo e, ao final, uma conclusão.

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
{resume_text}
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"""
strength_prompt = PromptTemplate(
    template=strength_prompt_template,
    input_variables=["resume_text"],
)

# Prompt para Pontos Fracos e Sugestões
weakness_prompt_template = """
Responda em português.
Preciso de uma análise detalhada e explicação dos pontos fracos do currículo abaixo, além de sugestões de como melhorá-lo para torná-lo mais competitivo.

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
{resume_text}
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"""
weakness_prompt = PromptTemplate(
    template=weakness_prompt_template,
    input_variables=["resume_text"],
)

# Prompt para Sugestão de Vagas de Emprego
job_role_prompt_template = """
Responda em português.
Com base no currículo abaixo, quais são os cargos para os quais eu devo me candidatar no LinkedIn?

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
{resume_text}
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"""
job_role_prompt = PromptTemplate(
    template=job_role_prompt_template,
    input_variables=["resume_text"],
)

# Criação dos chains para cada prompt adicional
summary_chain = summary_prompt | llm | StrOutputParser()
strength_chain = strength_prompt | llm | StrOutputParser()
weakness_chain = weakness_prompt | llm | StrOutputParser()
job_role_chain = job_role_prompt | llm | StrOutputParser()

def analyze_resume_complete(resume_text):
    summary_result = summary_chain.invoke(input=resume_text)
    strength_result = strength_chain.invoke(input=resume_text)
    weakness_result = weakness_chain.invoke(input=resume_text)
    job_role_result = job_role_chain.invoke(input=resume_text)
    
    # Se desejar, você pode implementar uma lógica para calcular a nota final
    final_score = "85"
    
    final_html = f"""
    <h2>Resumo do Currículo</h2>
    {summary_result}
    <h2>Pontos Fortes</h2>
    {strength_result}
    <h2>Aspectos Fracos e Sugestões de Melhoria</h2>
    {weakness_result}
    <h2>Vagas de Emprego Sugeridas</h2>
    {job_role_result}
    <h2>Nota Final: {final_score}/100</h2>
    """
    return final_html
