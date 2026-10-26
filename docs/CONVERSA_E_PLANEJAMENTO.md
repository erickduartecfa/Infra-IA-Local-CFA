# Histórico de Planejamento e Decisões — IA Local CFA

Data: 26/10/2026

## 1. Contexto e Objetivos
- **Instituição:** Conselho Federal de Administração (CFA).
- **Objetivo Estratégico:** Construir uma IA local (on-premises) corporativa conectada aos sistemas internos para apoiar colaboradores. Futuramente será adquirido um servidor dedicado (com GPUs como NVIDIA L4 / RTX 4000 Ada).
- **Objetivo Inicial (PoC):** Iniciar pequeno com um chatbot inteligente de atendimento para o portal web do CFA, focado em tirar dúvidas de administradores e tecnólogos sobre normas, anuidades e registros profissionais.

## 2. Diagnóstico da Máquina de Testes
- **SO:** Oracle Linux 10.2 nativo (bare metal, sem WSL ou máquinas virtuais) — Hostname: `bulma`.
- **CPU:** Intel Core i7-8700
- **RAM:** 32 GB
- **GPU:** NVIDIA GTX 1060 6GB (Arquitetura Pascal — exige driver proprietário branch `580`, especificamente `3:580.196.07-1.el10` com `kmod-nvidia-latest-dkms` e bloqueio via `dnf versionlock`).
- **Armazenamento:** SSD 1 TB
- **Capacidade de Inferência:** Modelo `qwen2.5:7b` (quantizado em 4 bits, ocupando ~4.7 GB de VRAM) + modelo de embedding `bge-m3` (~1.1 GB de VRAM).

## 3. Repositório e Colaboração da Equipe
- **Repositório Oficial no GitHub:** `https://github.com/erickduartecfa/Infra-IA-Local-CFA.git`
- **Configuração de Contexto Automático:** Arquivo `GEMINI.md` na raiz do projeto para carregar automaticamente todas as regras, parâmetros técnicos e objetivos sempre que qualquer membro da equipe abrir o projeto no Antigravity.
- **Comando de Clone para a Equipe de Infraestrutura:**
  ```bash
  git clone https://github.com/erickduartecfa/Infra-IA-Local-CFA.git
  ```

## 4. Estratégia de Divisão do Projeto em Fases e Progresso
- **FASE 1 (Imediata / Isolada):** Realizada localmente na máquina no Oracle Linux sem mexer em configurações de rede:
  1. ✅ **[CONCLUÍDO - 26/10/2026]** Validação do driver NVIDIA (`nvidia-smi`) na GTX 1060 sob Oracle Linux 10.2 (fixado driver proprietário `580.196.07` com DKMS e `versionlock`).
  2. ✅ **[CONCLUÍDO - 26/10/2026]** Instalação do Ollama configurado em loopback (`127.0.0.1:11434`) e `OLLAMA_NUM_PARALLEL=1`.
  3. ✅ **[CONCLUÍDO - 26/10/2026]** Download e validação prática dos modelos `qwen2.5:7b` e `bge-m3`.
  4. ⏳ **[PRÓXIMO PASSO]** Subida do Qdrant localmente no Docker (`127.0.0.1:6333`).
  5. ⏳ Indexação de 1 ou 2 PDFs de teste do CFA via script Python (`src/indexar.py`).
  6. ⏳ Teste de chat local via FastAPI (`src/app.py`) e curl/browser local.
- **FASE 2 (Alinhamento com Técnico de Redes e Segurança):**
  1. Definição do IP fixo/VLAN na infraestrutura do CFA.
  2. Regras no Sophos Firewall (WAF, IPS, proteção anti-DDoS e rate limit por IP).
  3. Regras de `firewalld` no Oracle Linux liberando apenas portas autorizadas.
  4. Configuração de HTTPS e certificado SSL no subdomínio (ex: `ia.cfa.org.br`).
  5. Implantação do widget JavaScript no portal do CFA.
