# Contexto e Regras do Projeto — IA Local Institucional (CFA)

Você é o assistente técnico especializado no desenvolvimento e implantação da **IA Local do Conselho Federal de Administração (CFA)**.

## 1. Contexto e Objetivos
* **Instituição:** Conselho Federal de Administração (CFA).
* **Objetivo Geral:** Construção de uma IA on-premises (local), soberana e segura, conectada futuramente aos sistemas internos da autarquia.
* **Foco da PoC (Fase Atual):** Chatbot institucional para o portal web do CFA com RAG (Retrieval-Augmented Generation), focado em responder dúvidas de administradores e tecnólogos sobre normas, resoluções, anuidades e registro profissional, sem alucinações e citando fontes oficiais.

## 2. Hardware e Restrições Técnicas
* **SO:** Oracle Linux nativo (bare metal, sem virtualização/WSL).
* **Processador:** Intel Core i7-8700 (6 núcleos / 12 threads).
* **RAM:** 32 GB DDR4.
* **GPU:** NVIDIA GeForce GTX 1060 6GB GDDR5.
* **Armazenamento:** SSD 1 TB.
* **Alocação de VRAM estrita:**
  * LLM de Inferência: `qwen2.5:7b` (~4.7 GB de VRAM).
  * Embeddings Semânticos: `bge-m3` (~1.1 GB de VRAM).
  * Restrição: Não utilizar modelos maiores que 7B (como 14B ou 32B) nesta máquina para não exceder os 6GB de VRAM.

## 3. Arquitetura e Segurança
* **Ollama (Motor LLM):** Escutando estritamente em `127.0.0.1:11434`, com `OLLAMA_NUM_PARALLEL=1`.
* **Qdrant (Banco Vetorial):** Container Docker escutando estritamente em `127.0.0.1:6333` com persistência de dados em disco.
* **Backend:** FastAPI (Python) com validação Pydantic, limitação de taxa (SlowAPI) e sanitização anti-prompt injection.
* **Segurança Perimetral:** Sophos Firewall (WAF, IPS, DoS Protection) + `firewalld` no Oracle Linux + Proxy reverso Nginx com SSL institucional.

## 4. Estratégia de Fases
* **Fase 1 (Local / Imediata):** Execução e validação 100% em localhost (loopback), sem alterar a rede corporativa nem abrir portas externas.
* **Fase 2 (Rede e Infraestrutura):** Configuração de IP/VLAN, regras no Sophos Firewall, certificado digital HTTPS e publicação do widget web.

## 5. Documentação de Referência
Sempre consulte os seguintes documentos para manter a coerência das decisões:
* `docs/GUIA_IMPLANTACAO_IA_CFA.md`: Roteiro técnico passo a passo detalhado de comandos e configurações.
* `docs/CONVERSA_E_PLANEJAMENTO.md`: Histórico de alinhamentos e decisões estratégicas.
* `README.md`: Visão geral do repositório.
