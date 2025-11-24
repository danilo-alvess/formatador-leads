#**App de Captação e Formatação de Leads**

Este é um aplicativo desenvolvido com **Streamlit** para otimizar o processo de **validação, formatação e limpeza de leads** da ADM Soluções.
O app permite transformar planilhas brutas exportadas da Casa dos Dados em arquivos prontos para importação no **HubSpot**, além de gerar uma versão apenas com os **leads validados**.

---

## 📌 **Funcionalidades Principais**

### 🧾 **1. FORMATAÇÃO DE LEADS**

* Upload de planilha bruta (`empresas.xlsx`) obtida na Casa dos Dados.
* Seleção do responsável pela validação → gera automaticamente:

  * E-mail do responsável
  * Consultor alocado
  * Estrutura final das colunas
  * Formatação automática do **Nome do Arquivo** com hora/data.
* Download da planilha **pronta para o HubSpot**.

---

### 🧹 **2. LIMPEZA DE LEADS**

* Upload de uma planilha **Já formatada**.
* O app filtra apenas os leads com status `"Validado"` ou `"Sim"`.
* Gera um novo arquivo com **apenas os leads aprovados**, também com nome formatado automaticamente.

---

### 📊 **3. DASHBOARD (em desenvolvimento)**

* Área reservada para métricas de captação e performance.

---

## 🧠 **Tecnologias Utilizadas**

| Ferramenta          | Utilização                    |
| ------------------- | ----------------------------- |
| Streamlit           | Interface interativa          |
| Pandas              | Manipulação da planilha       |
| Hydralit Components | Navbar superior               |
| Regex (re)          | Limpeza de nomes e sócios     |
| XlsxWriter          | Exportação em Excel           |
| ZoneInfo            | Data e hora local (Fortaleza) |

---

## 📂 **Estrutura de Arquivo da Planilha Bruta Esperada**

A planilha de entrada deve conter a **aba `empresas`** com as colunas:

```
Razao Social
Nome Fantasia
Socios
Telefones
CNPJ
E-mail
```

---

## 🔄 **Colunas Geradas na Planilha Formatada**

Após o processamento, o app gera uma planilha com a seguinte estrutura:

| Nome do negócio | Etapa do negócio | Proprietário do negócio | Consultor alocado | Fonte | Nome da empresa | CNPJ | E-mail | Nome | Fase do ciclo de vida | Número de telefone | Status | Pipeline |
| --------------- | ---------------- | ----------------------- | ----------------- | ----- | --------------- | ---- | ------ | ---- | --------------------- | ------------------ | ------ | -------- |

---

## ▶️ **Como Rodar Localmente**

### **1. Clone o repositório**

```bash
git clone https://github.com/SEU-USUARIO/SEU-REPO.git
cd SEU-REPO
```

### **2. Instale as dependências**

```bash
pip install -r requirements.txt
```

### **3. Execute o app**

```bash
streamlit run app.py
```

---

## ⚙️ **Arquivo `requirements.txt` sugerido**

```txt
streamlit
pandas
openpyxl
xlsxwriter
hydralit_components
```

---

## 💡 **Melhorias Futuras**

* Dashboard com KPIs de captação (MQL, SQL, taxa de conversão etc.).
* Login por e-mail ADM.
* Histórico das formatações por usuário.
* Integração com API HubSpot.
* Automação do download direto da Casa dos Dados.

---

## 👨‍💻 **Desenvolvido por**

**Danilenda 🐶** – Analista de Marketing da ADM Soluções
📆 Versão atual: **2.0.3**

---
