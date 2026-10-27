# 📌 Contexto Atual e Guia de Operação do Projeto — IA Local CFA

> **Última atualização:** 27/10/2026  
> **Público-alvo:** Integrantes da equipe de TI/Infraestrutura do CFA e Assistente de IA (Gemini / Antigravity).  
> **Objetivo deste documento:** Garantir que qualquer membro da equipe consiga operar, testar ou evoluir a IA Local do CFA — seja **por conta própria via SSH** ou **com ajuda do Gemini** — sem ficar perdido.

---

## 1. Fotografia Atual do Projeto (Onde Estamos?)

A **Fase 1 (Prova de Conceito 100% Local)** está **TOTALMENTE CONCLUÍDA E VALIDADA**. A IA já lê documentos oficiais do CFA em PDF, faz busca semântica no banco vetorial e responde perguntas em português citando as fontes.

### Resumo do Ambiente Implantado
* **Servidor Linux:** Hostname `bulma` — **Oracle Linux 10.2 nativo** (*bare metal*), acessado via SSH (`root@bulma`).
* **Hardware:** Intel Core i7-8700, 32 GB RAM, SSD 1 TB, GPU **NVIDIA GeForce GTX 1060 6GB**.
* **Driver da GPU:** Proprietário NVIDIA **branch `3:580.196.07-1.el10`** (`kmod-nvidia-latest-dkms`), travado via `dnf versionlock` *(⚠️ Nunca atualizar para 590/615+ nem usar `kmod-nvidia-open`, pois a arquitetura Pascal da GTX 1060 exige a série 580 proprietária)*.
* **Pasta principal no servidor `bulma`:** `/root/cfa-ia` (`~/cfa-ia`).
* **Documentos já indexados no banco vetorial:**
  1. `Regimento Interno CFA.pdf`
  2. `decreto_61934_1967_655.pdf`

---

## 2. O Que Sobe Sozinho vs. O Que Precisa Ligar Manualmente no `bulma`

Quando a máquina de testes `bulma` é ligada:

| Serviço / Componente | Porta (Localhost) | Sobe sozinho no boot? | Como verificar status |
| :--- | :---: | :---: | :--- |
| **Driver NVIDIA (GTX 1060)** | — | ✅ **Sim** | `nvidia-smi` |
| **Ollama (`qwen2.5:7b` + `bge-m3`)** | `127.0.0.1:11434` | ✅ **Sim** (`systemd`) | `systemctl status ollama` |
| **Docker + Banco Vetorial Qdrant** | `127.0.0.1:6333` | ✅ **Sim** (`unless-stopped`) | `docker ps` |
| **API FastAPI do Chat (`src/app.py`)** | `127.0.0.1:8000` | ❌ **Não (Manual por enquanto)** | `curl http://127.0.0.1:8000/health` |

---

## 3. Guia Rápido de Operação (Para Usar Por Conta Própria via SSH)

### A. Como ligar a API após ligar o servidor `bulma`
Conecte via SSH (`ssh root@bulma`) e rode:
```bash
cd ~/cfa-ia
source venv/bin/activate
nohup python ~/cfa-ia/src/app.py > ~/cfa-ia/api.log 2>&1 &
```
*(Os logs ficam salvos em `~/cfa-ia/api.log` para não poluir a tela do terminal com as checagens de `/metrics` do Oracle Linux).*

### B. Como conversar e fazer testes com a IA

#### Opção 1: Chat interativo direto no terminal SSH
Cole este comando no terminal do `bulma` para digitar várias perguntas seguidas:
```bash
while true; do
  echo ""
  read -p "👤 Pergunta (ou 'sair'): " PERGUNTA
  [[ "$PERGUNTA" == "sair" ]] && break
  echo "🤖 Pensando..."
  curl -s -X POST http://127.0.0.1:8000/chat \
    -H "Content-Type: application/json" \
    -d "$(jq -n --arg t "$PERGUNTA" '{texto: $t}')" | jq -r '"\n✅ Resposta:\n" + .resposta + "\n\n📚 Fontes: " + ([.fontes[].documento] | unique | join(", "))'
done
```

#### Opção 2: Testar pelo navegador do Windows (Swagger UI do FastAPI)
1. No **PowerShell do seu Windows**, abra o SSH criando um túnel local na porta `8000`:
   ```powershell
   ssh -L 8000:127.0.0.1:8000 root@bulma
   ```
2. Com a API ligada lá no `bulma`, abra o navegador do seu Windows em:
   👉 **`http://localhost:8000/docs`**
3. Clique em **`POST /chat`** -> **`Try it out`**, escreva a pergunta no JSON e clique em **`Execute`**.

### C. Como adicionar novos PDFs do CFA na base de conhecimento
Como o servidor `bulma` não possui conta do GitHub configurada (o repositório é privado), o envio de arquivos das máquinas Windows da equipe para o `bulma` é feito via **`scp`**:

1. Coloque os novos PDFs na pasta `data\raw_documents\` do projeto no seu Windows.
2. No **PowerShell do Windows**, envie para o `bulma`:
   ```powershell
   scp "C:\CAMINHO\Infra-IA-Local-CFA\data\raw_documents\*.pdf" root@bulma:~/cfa-ia/data/raw_documents/
   ```
3. No **SSH do `bulma`** (com o `venv` ativo), rode o indexador:
   ```bash
   python ~/cfa-ia/src/indexar.py
   ```

### D. Como parar a API ou desligar o servidor no fim do expediente
```bash
# Parar apenas a API Python (se necessário):
pkill -f "src/app.py"

# Sair do ambiente virtual Python (venv):
deactivate

# Desligar o servidor bulma com segurança:
shutdown -h now
```

---

## 4. Como Interagir com o Gemini / Antigravity Sem Ficar Perdido

Sempre que abrir o projeto no **Antigravity**:

1. **Primeiro atualize os arquivos da sua máquina com o GitHub:**
   ```bash
   git pull origin main
   ```
2. **O Gemini já lê automaticamente os arquivos `GEMINI.md` e `CONTEXTO_ATUAL_DO_PROJETO.md`.** Você não precisa explicar o projeto do zero. Basta mandar no chat uma das mensagens abaixo conforme o que desejar fazer:
   * *"Bom dia! Quero fazer novos testes de perguntas e adicionar mais PDFs do CFA hoje. Me guie passo a passo."*
   * *"Quero criar uma interface web simples de chat para testar a IA pelo navegador."*
   * *"Quero configurar o `src/app.py` como um serviço `systemd` no servidor `bulma` para que a API já suba sozinha quando ligarmos a máquina."*
   * *"Vamos iniciar a Fase 2 (configuração de rede, firewalld, Nginx com HTTPS e Sophos Firewall)."*
3. **Ao terminar o trabalho do dia**, peça ao Gemini:
   * *"Atualize a documentação com o que fizemos hoje e suba para o GitHub."*

---

## 5. O Que Falta Fazer? (Próximos Passos — Fase 2)

- [ ] **Automação Local:** Transformar a API FastAPI (`~/cfa-ia/src/app.py`) em um serviço `systemd` (`cfa-ia-api.service`) para iniciar sozinha no boot do `bulma`.
- [ ] **Interface de Chat (Front-end / Widget):** Construir a janela de chat web (HTML/JS) com a identidade visual do CFA para testes de usuários e futura incorporação no portal.
- [ ] **Expansão do RAG:** Indexar mais resoluções normativas, tabelas de anuidades e perguntas frequentes oficiais do CFA.
- [ ] **Rede e Segurança (Com Técnico de Redes):**
  - Definir IP estático / VLAN para o servidor `bulma`.
  - Configurar proxy reverso (Nginx + HTTPS) e regras de `firewalld`.
  - Publicar via Sophos Firewall (WAF, IPS e Rate Limiting por IP).
