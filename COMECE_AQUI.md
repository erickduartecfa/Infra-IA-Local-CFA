# 🎯 COMECE AQUI — IA Local Institucional (CFA)

Bem-vindo(a) à equipe do **Projeto IA Local do CFA**! 

Este repositório contém todo o planejamento, código-fonte e roteiro operacional para implantar a Inteligência Artificial local (on-premises) e soberana do **Conselho Federal de Administração**.

---

## ⚡ 1. Resumo em 30 Segundos
* **Objetivo:** Chatbot institucional com RAG para tirar dúvidas de administradores e tecnólogos sobre resoluções, anuidades e normas do CFA sem alucinações.
* **Máquina de Testes (PoC):** Servidor `bulma` — Intel Core i7-8700, 32GB RAM, **NVIDIA GTX 1060 6GB**, SSD 1TB, rodando **Oracle Linux 10.2 nativo** (*bare metal*).
* **Modelos Escolhidos (Cabem com folga nos 6GB de VRAM):**
  * `qwen2.5:7b` (~4.7 GB) para raciocínio e geração de respostas em português.
  * `bge-m3` (~1.1 GB) para busca semântica em normas e PDFs.
* **Status da Fase 1:** **100% Concluída e Validada em Localhost (`127.0.0.1`)!**

---

## 🚀 2. Como usar este projeto no seu Antigravity

1. **Abra a pasta no Antigravity:** `File` > `Open Workspace` > Selecione esta pasta `Infra-IA-Local-CFA`.
2. **Abra o Chat:** Você **não precisa** explicar o projeto nem colar regras. O Antigravity já leu o arquivo `GEMINI.md` na raiz e já sabe de tudo.
3. **Mande uma mensagem direta:**
   > *"Olá! Estou assumindo o projeto. Em qual etapa estamos e o que devemos executar agora?"*

A IA guiará você passo a passo com os comandos exatos para rodar no terminal do Oracle Linux.

---

## 📍 3. Onde o Projeto Está Agora (Status Atual)

| Etapa | Descrição | Status |
| :--- | :--- | :---: |
| **Planejamento** | Dimensionamento de hardware, modelos e arquitetura | ✅ **Concluído** |
| **Repositório** | Git, regras do Antigravity e scripts base (`src/`) | ✅ **Concluído** |
| **Fase 1 - Passo 1** | Validar GPU e driver NVIDIA (`nvidia-smi` - branch 580) no Oracle Linux 10 | ✅ **Concluído** |
| **Fase 1 - Passo 2** | Instalar Ollama e configurar serviço systemd em `127.0.0.1` | ✅ **Concluído** |
| **Fase 1 - Passo 3** | Baixar e validar modelos `qwen2.5:7b` e `bge-m3` | ✅ **Concluído** |
| **Fase 1 - Passo 4** | Instalar Docker CE e subir Qdrant em `127.0.0.1:6333` | ✅ **Concluído** |
| **Fase 1 - Passo 5 a 7** | Ambiente Python (`venv`), indexação de PDFs do CFA e API FastAPI validada | ✅ **Concluído** |
| **Fase 2** | Alinhamento com técnico de redes, Sophos Firewall, Nginx/SSL e Widget Web | ⏳ **PRÓXIMO PASSO** |

---

## 📚 4. Documentos de Referência Rápida

* [GUIA_IMPLANTACAO_IA_CFA.md](docs/GUIA_IMPLANTACAO_IA_CFA.md): Manual técnico passo a passo com todos os comandos de terminal validados.
* [GUIA_SINCRONIZACAO_E_ATUALIZACAO.md](docs/GUIA_SINCRONIZACAO_E_ATUALIZACAO.md): Como atualizar o Git e registrar etapas concluídas.
* [CONVERSA_E_PLANEJAMENTO.md](docs/CONVERSA_E_PLANEJAMENTO.md): Histórico e justificativas técnicas das decisões tomadas.
