# Histórico de Planejamento e Decisões — IA Local CFA

Data: 26/10/2026

## 1. Contexto e Objetivos
- **Instituição:** Conselho Federal de Administração (CFA).
- **Objetivo Estratégico:** Construir uma IA local (on-premises) corporativa conectada aos sistemas internos para apoiar colaboradores. Futuramente será adquirido um servidor dedicado (com GPUs como NVIDIA L4 / RTX 4000 Ada).
- **Objetivo Inicial (PoC):** Iniciar pequeno com um chatbot inteligente de atendimento para o portal web do CFA, focado em tirar dúvidas de administradores e tecnólogos sobre normas, anuidades e registros profissionais.

## 2. Diagnóstico da Máquina de Testes
- **SO:** Oracle Linux 10.2 nativo (bare metal, sem WSL ou máquinas virtuais) — Hostname: `bulma` (acesso remoto via SSH).
- **CPU:** Intel Core i7-8700
- **RAM:** 32 GB
- **GPU:** NVIDIA GTX 1060 6GB (Arquitetura Pascal — exige driver proprietário branch `580`, especificamente `3:580.196.07-1.el10` com `kmod-nvidia-latest-dkms` e bloqueio via `dnf versionlock`).
- **Armazenamento:** SSD 1 TB
- **Capacidade de Inferência:** Modelo `qwen2.5:7b` (quantizado em 4 bits, ocupando ~4.7 GB de VRAM) + modelo de embedding `bge-m3` (~1.1 GB de VRAM).

## 3. Repositório e Colaboração da Equipe
- **Repositório Oficial no GitHub:** `https://github.com/erickduartecfa/Infra-IA-Local-CFA.git` (Repositório privado sincronizado nas máquinas de trabalho do Erick e do Izaías; transferência para o servidor `bulma` realizada via `scp` por SSH, sem necessidade de expor credenciais do GitHub no servidor Linux).
- **Configuração de Contexto Automático:** Arquivo `GEMINI.md` na raiz do projeto para carregar automaticamente todas as regras, parâmetros técnicos e objetivos sempre que qualquer membro da equipe abrir o projeto no Antigravity.

## 4. Estratégia de Divisão do Projeto em Fases e Progresso
- **FASE 1 (Imediata / Isolada) — ✅ 100% CONCLUÍDA EM 26/10/2026:**
  1. ✅ **[CONCLUÍDO - 26/10/2026]** Validação do driver NVIDIA (`nvidia-smi`) na GTX 1060 sob Oracle Linux 10.2 (fixado driver proprietário `3:580.196.07-1.el10` com `kmod-nvidia-latest-dkms`, `--exclude="kmod-nvidia-open*"` e `dnf versionlock`).
  2. ✅ **[CONCLUÍDO - 26/10/2026]** Instalação do Ollama configurado em loopback (`127.0.0.1:11434`) e `OLLAMA_NUM_PARALLEL=1`.
  3. ✅ **[CONCLUÍDO - 26/10/2026]** Download e validação prática dos modelos `qwen2.5:7b` e `bge-m3`.
  4. ✅ **[CONCLUÍDO - 26/10/2026]** Instalação do Docker CE no Oracle Linux 10 (repositório oficial CentOS/RHEL, removendo conflito com `podman/runc`) e subida do Qdrant localmente (`127.0.0.1:6333`).
  5. ✅ **[CONCLUÍDO - 26/10/2026]** Envio da estrutura via `scp` para `~/cfa-ia/`, criação do `venv` Python e indexação dos documentos oficiais (`Regimento Interno CFA.pdf` e `decreto_61934_1967_655.pdf`) via `src/indexar.py`.
  6. ✅ **[CONCLUÍDO - 26/10/2026]** Adequação do `src/app.py` para o método `qdrant.query_points(...).points` (`qdrant-client >= 1.16`), execução da API FastAPI em `127.0.0.1:8000` (com logs redirecionados para `~/cfa-ia/api.log`) e validação completa de perguntas e respostas baseadas no Regimento Interno do CFA.
- **FASE 2 (Alinhamento com Técnico de Redes, Segurança e Front-end) — ⏳ PRÓXIMO PASSO:**
  1. Configurar serviço `systemd` para manter a API FastAPI (`src/app.py`) rodando automaticamente no boot do servidor `bulma`.
  2. Definição do IP fixo/VLAN na infraestrutura do CFA.
  3. Regras no Sophos Firewall (WAF, IPS, proteção anti-DDoS e rate limit por IP).
  4. Regras de `firewalld` no Oracle Linux liberando apenas portas autorizadas.
  5. Configuração de HTTPS e certificado SSL no subdomínio (ex: `ia.cfa.org.br`).
  6. Implantação do widget JavaScript no portal do CFA.
