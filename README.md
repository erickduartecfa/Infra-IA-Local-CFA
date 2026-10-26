# Projeto IA Local — Conselho Federal de Administração (CFA)

> **Projeto Atualizado. ** Comece lendo o [**COMECE_AQUI.md**](COMECE_AQUI.md) para entender o status atual e como usar o Antigravity em 30 segundos!

---

## Repositório Oficial
* **URL:** `https://github.com/erickduartecfa/Infra-IA-Local-CFA.git`
* **Clone para a equipe:**
  ```bash
  git clone https://github.com/erickduartecfa/Infra-IA-Local-CFA.git
  ```

## Visão Geral
Este projeto tem como objetivo desenvolver e implantar uma Inteligência Artificial local (on-premises) para o **Conselho Federal de Administração (CFA)**, iniciando como um chatbot institucional inteligente para o portal web e, futuramente, expandindo para conexão com os sistemas internos corporativos dos colaboradores.

## Hardware de Teste (PoC Atual)
- **Sistema Operacional:** Oracle Linux nativo (bare metal, sem virtualização)
- **Processador:** Intel Core i7-8700 (6 núcleos / 12 threads)
- **Memória RAM:** 32 GB DDR4
- **Placa de Vídeo:** NVIDIA GeForce GTX 1060 6GB GDDR5
- **Armazenamento:** SSD 1 TB

## Segurança e Infraestrutura
- **Firewall de Perímetro:** Sophos Firewall (WAF, IPS, DoS Protection)
- **Firewall de Host:** firewalld + SELinux (Oracle Linux)
- **Isolamento:** Ollama (11434) e Qdrant (6333) vinculados estritamente ao 127.0.0.1

## Estrutura do Repositório
```
Infra-IA-Local-CFA/
├── data/
│   └── raw_documents/             # PDFs e normas oficiais do CFA para indexação
├── docs/
│   ├── GUIA_IMPLANTACAO_IA_CFA.md    # Roteiro técnico passo a passo
│   ├── GUIA_SINCRONIZACAO_E_ATUALIZACAO.md # Como manter a equipe alinhada no Git
│   ├── GUIA_COLABORACAO_EQUIPE.md    # Onboarding da equipe no Antigravity
│   └── CONVERSA_E_PLANEJAMENTO.md    # Histórico das decisões e alinhamentos
├── src/
│   ├── indexar.py                 # Pipeline RAG (fatiamento e embeddings no Qdrant)
│   └── app.py                     # API FastAPI com guardrails e rate limit
├── COMECE_AQUI.md                 # Guia de entrada rápida para a equipe
├── GEMINI.md                      # Contexto automático lido pelo Antigravity
├── requirements.txt               # Dependências Python
└── README.md
```

Consulte o arquivo [GUIA_IMPLANTACAO_IA_CFA.md](docs/GUIA_IMPLANTACAO_IA_CFA.md) para o passo a passo completo.
