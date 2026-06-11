# 🏥 Dashboard de Análise de Readmissão Hospitalar

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-14354C?style=for-the-badge&logo=python&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-239120?style=for-the-badge&logo=Plotly&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-15045C?style=for-the-badge&logo=pandas&logoColor=white)

Um dashboard executivo interativo desenvolvido em Python com **Streamlit** focado no monitoramento, controle e predição do risco de readmissão clínica de pacientes hospitalares. 

O projeto simula um cenário real de inteligência de negócios (BI) e ciência de dados aplicada à saúde, com interface personalizada em **Tema Escuro (Dark Mode)** e destaques em **Verde Neon** para garantir alta legibilidade e impacto visual.

---

## 📊 Indicadores Principais (KPIs)

O painel monitora de forma centralizada as quatro métricas vitais para a gestão de leitos e qualidade de atendimento do hospital:

* **Total de Pacientes:** Volume de histórico analítico (Base cravada em 55.000 registros).
* **Taxa de Readmissão:** Porcentagem de pacientes que retornam ao hospital em menos de 30 dias após a alta (Meta de controle: 11.25%).
* **Risco Médio:** Indicador preditivo da probabilidade de reingresso clínico (Média de 37.09%).
* **Tempo de Internação:** Média de dias que os pacientes permanecem ocupando leitos (Média de 4.0 dias).

---

## 📈 Visualizações e Análises Gráficas

O dashboard é composto por quatro módulos de análise dinâmica baseados nos filtros laterais:

1.  **Readmissão por Gênero (Gráfico de Barras):** Identifica disparidades na taxa de retorno entre pacientes masculinos e femininos.
2.  **Tempo de Internação X Risco (Gráfico de Linha):** Demonstra de forma contínua como o tempo de permanência no hospital influencia a curva de risco de retorno.
3.  **Readmissão por Faixa Etária (Gráfico de Barras Ordenado):** Segmentação etária por faixas (ex: `[0-10)`, `[10-20)`, etc.) para identificar grupos de vulnerabilidade.
4.  **Medicamentos X Risco (Gráfico de Área):** Análise volumétrica mostrando a correlação entre a quantidade de medicamentos prescritos e o score de risco final do paciente.

---

## 🛠️ Tecnologias e Bibliotecas Utilizadas

* **Python 3** (Linguagem base)
* **Streamlit** (Framework para construção da interface web e reatividade)
* **Pandas** (Estruturação, manipulação e tratamento dos dados na memória)
* **NumPy** (Geração de matrizes matemáticas e simulação estatística proporcional dos dados)
* **Plotly Express** (Renderização dos gráficos interativos com suporte a tooltips e zoom)
* **HTML5/CSS3** (Estilização injetada via `st.markdown` para modificação do layout padrão do Streamlit)

---

## 🚀 Como Executar o Projeto Localmente

Se você deseja rodar este projeto na sua máquina:

1. Clone o repositório:
   ```bash
   git clone [https://github.com/hiranmarques/dashboard-hospitalar.git](https://github.com/hiranmarques/dashboard-hospitalar.git)

   Acesse a pasta do projeto:

2. Bash
cd dashboard-hospitalar
Instale as dependências necessárias:

3. Bash
pip install streamlit pandas numpy plotly
Execute o servidor do Streamlit:

4. Bash
streamlit run app.py

5. Vá até o final da página e clique no botão verde **"Commit changes..."** para salvar o arquivo no seu repositório.

---
👤 Desenvolvedor
Hiran Marques - Cientista de Dados | Machine Learning · Analytics · GCP
