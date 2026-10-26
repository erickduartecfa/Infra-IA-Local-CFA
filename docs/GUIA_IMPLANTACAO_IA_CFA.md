# Guia Técnico de Implantação: IA Local Institucional — CFA

Este roteiro operacional detalha a implantação da Prova de Conceito (PoC) da IA Local do **Conselho Federal de Administração (CFA)** no hardware atual (**Intel Core i7-8700, 32GB RAM, NVIDIA GTX 1060 6GB**) rodando **Oracle Linux 10.2 nativo (bare metal)** no servidor `bulma`.

O projeto está dividido em duas fases estratégicas:
* **Fase 1 (100% CONCLUÍDA E VALIDADA):** Instalação e testes 100% locais na máquina (`127.0.0.1`), sem qualquer alteração na rede, sem abrir portas externas e sem risco à infraestrutura.
* **Fase 2 (PRÓXIMO PASSO — Com o Técnico de Redes e Front-end):** Serviço `systemd` da API, definição de IP, regras do Sophos Firewall, DMZ, WAF, certificado HTTPS e publicação do chatbot.

---

```
                       ROTEIRO DE IMPLANTAÇÃO
  
  [ FASE 1: 100% CONCLUÍDA - LOCAL ]       [ FASE 2: PRÓXIMO PASSO - REDE/WEB ]
  +--------------------------------+       +------------------------------------+
  | 1. [OK] GPU & CUDA (Branch 580)|       | 8. [->] Definição de IP / VLAN CFA |
  | 2. [OK] Instalação do Ollama   |  ==>  | 9. Ajustes de firewalld & SELinux  |
  | 3. [OK] Download dos Modelos   |       | 10. Regras no Sophos Firewall/WAF  |
  | 4. [OK] Subida Qdrant (Docker) |       | 11. Reverse Proxy Nginx + HTTPS    |
  | 5. [OK] Ambiente Python & SCP  |       | 12. Publicação do Widget no Site   |
  | 6. [OK] Indexação PDFs do CFA  |       +------------------------------------+
  | 7. [OK] Teste de Chat RAG API  |
  +--------------------------------+
```

---

# PARTE 1: PREPARAÇÃO LOCAL IMEDIATA (FASE 1 — ✅ CONCLUÍDA)
> *Todas as etapas abaixo rodam estritamente em `127.0.0.1` (localhost). Nenhuma porta externa é aberta.*

---

## Passo 1: Verificar e Preparar a GPU (NVIDIA GTX 1060 6GB) — ✅ CONCLUÍDO

Abra o terminal do Oracle Linux e verifique se o driver já está instalado:
```bash
nvidia-smi
```

### Cenário A: Se o comando exibir a tabela da GPU
Se aparecer `GeForce GTX 1060 6GB`, Driver Version (`580.x`) e CUDA Version, **a GPU está pronta**. Pule para o Passo 2.

### Cenário B: Instalação no Oracle Linux 10 (Procedimento Validado para GTX 1060 / Pascal)
No Oracle Linux 10 (`rhel10`), o `dnf module` foi descontinuado e os drivers 590+ / `kmod-nvidia-open` não suportam a arquitetura Pascal (GTX 1060). Deve-se fixar a branch proprietária **580**:

```bash
# 1. Atualizar pacotes e instalar ferramentas e headers do kernel atual
sudo dnf upgrade -y
sudo dnf install -y oracle-epel-release-el$(rpm -E %{rhel})
sudo dnf groupinstall -y "Development Tools"
sudo dnf install -y dkms kernel-uek-devel-$(uname -r) kernel-headers git curl jq || sudo dnf install -y dkms kernel-devel-$(uname -r)

# 2. Adicionar repositório CUDA da NVIDIA para RHEL/Oracle Linux 10
sudo dnf config-manager --add-repo https://developer.download.nvidia.com/compute/cuda/repos/rhel$(rpm -E %{rhel})/x86_64/cuda-rhel$(rpm -E %{rhel}).repo
sudo dnf clean expire-cache

# 3. Instalar o driver proprietário branch 580 (compatível com GTX 1060) e CUDA Toolkit
sudo dnf install -y \
  kmod-nvidia-latest-dkms-3:580.196.07-1.el10 \
  nvidia-driver-cuda-3:580.196.07-1.el10 \
  nvidia-driver-cuda-libs-3:580.196.07-1.el10 \
  nvidia-kmod-common-3:580.196.07-1.el10 \
  nvidia-modprobe-3:580.196.07-1.el10 \
  nvidia-persistenced-3:580.196.07-1.el10 \
  cuda-toolkit \
  --exclude="kmod-nvidia-open*"

# 4. Travar versão na branch 580 para evitar upgrades incompatíveis (610/615+)
sudo dnf install -y 'dnf-command(versionlock)'
sudo dnf versionlock add "*nvidia*"

# 5. Conferir compilação do módulo DKMS e reiniciar
dkms status
sudo reboot
```
Após o reinício, execute `nvidia-smi` novamente para confirmar.

---

## Passo 2: Instalar o Ollama (Motor Local de IA) — ✅ CONCLUÍDO

O Ollama gerencia o uso da GPU e expõe a inferência localmente.

```bash
# Instalação automática do binário oficial
curl -fsSL https://ollama.com/install.sh | sh
```

### Configurar para operar estritamente em Localhost e 6GB VRAM:
Edite o serviço do systemd:
```bash
sudo systemctl edit ollama.service
```

Cole o conteúdo abaixo e salve (`Ctrl+O`, `Enter`, `Ctrl+X` no nano):
```ini
[Service]
# Amarra estritamente à máquina local (zero exposição na rede)
Environment="OLLAMA_HOST=127.0.0.1:11434"
Environment="OLLAMA_ORIGINS=http://127.0.0.1:*,http://localhost:*"
# Limita a 1 inferência por vez para não estourar os 6GB de VRAM da GTX 1060
Environment="OLLAMA_NUM_PARALLEL=1"
Environment="OLLAMA_KEEP_ALIVE=10m"
```

Aplique as mudanças:
```bash
sudo systemctl daemon-reload
sudo systemctl restart ollama
```

---

## Passo 3: Baixar os Modelos Otimizados no SSD — ✅ CONCLUÍDO

Baixe os dois modelos necessários diretamente para o disco:

```bash
# 1. Modelo de Raciocínio e Resposta (Qwen 2.5 7B - Ocupa ~4.7 GB de VRAM)
ollama pull qwen2.5:7b

# 2. Modelo de Busca Semântica em Documentos (BGE-M3 - Ocupa ~1.1 GB)
ollama pull bge-m3
```

### Teste de Validação no Terminal:
Execute no terminal:
```bash
ollama run qwen2.5:7b "Olá! Você está operacional no Conselho Federal de Administração?"
```
*(Se ele responder de forma fluida em português em alguns segundos, o motor está 100% calibrado na sua GPU).*

---

## Passo 4: Subir o Banco Vetorial Local (Qdrant) — ✅ CONCLUÍDO

O Qdrant armazenará os trechos das normas e resoluções do CFA com seus vetores matemáticos.

### 1. Instalar o Docker CE no Oracle Linux 10:
```bash
# Remover podman/runc caso venham pré-instalados para evitar conflito
sudo dnf remove -y podman runc

# Adicionar o repositório oficial do Docker (compatível com RHEL/Oracle Linux 10)
sudo dnf config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo

# Instalar Docker CE e habilitar no boot
sudo dnf install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo systemctl enable --now docker
```

### 2. Subir o container do Qdrant em `127.0.0.1:6333`:
```bash
# Criar diretório de dados persistentes no SSD
mkdir -p ~/cfa-ia/qdrant_storage

# Subir container amarrado estritamente a 127.0.0.1
docker run -d \
  --name qdrant \
  --restart unless-stopped \
  -p 127.0.0.1:6333:6333 \
  -v ~/cfa-ia/qdrant_storage:/qdrant/storage:z \
  qdrant/qdrant

# Validar resposta do Qdrant
curl http://127.0.0.1:6333/
```

---

## Passo 5: Transferir os Arquivos (SCP) e Criar o Ambiente Python — ✅ CONCLUÍDO

Como o repositório GitHub é privado e acessado nas estações de trabalho (Windows), envie os arquivos via `scp` para o servidor `bulma`:

### 1. No terminal PowerShell da máquina Windows:
```powershell
scp -r "src" "data" "requirements.txt" root@bulma:~/cfa-ia/
```

### 2. No terminal SSH do servidor (`root@bulma`):
```bash
cd ~/cfa-ia

# Garantir Python 3 e criar o ambiente virtual isolado
sudo dnf install -y python3 python3-pip
python3 -m venv venv
source venv/bin/activate

# Instalar dependências essenciais
pip install --upgrade pip
pip install -r requirements.txt
```

---

## Passo 6: Ingestão e Indexação de Documentos de Teste (RAG) — ✅ CONCLUÍDO

Os PDFs públicos do CFA (`Regimento Interno CFA.pdf` e `decreto_61934_1967_655.pdf`) ficam na pasta `~/cfa-ia/data/raw_documents/`.

Para indexar (ou reindexar novos PDFs adicionados à pasta), execute com o `venv` ativo:
```bash
python ~/cfa-ia/src/indexar.py
```

---

## Passo 7: Iniciar a API Local e Testar o Chat — ✅ CONCLUÍDO

O arquivo `~/cfa-ia/src/app.py` utiliza `qdrant.query_points(...).points` (compatível com `qdrant-client >= 1.16`) e expõe o endpoint `/chat` em `127.0.0.1:8000`.

### 1. Iniciar a API em segundo plano (salvando logs em `~/cfa-ia/api.log`):
```bash
pkill -f "src/app.py"
nohup python ~/cfa-ia/src/app.py > ~/cfa-ia/api.log 2>&1 &
```

### 2. Testar pergunta real via `curl`:
```bash
curl -s -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"texto": "Qual é a finalidade do Conselho Federal de Administração segundo o Regimento Interno?"}' | jq
```

*(Com isso, a Fase 1 está 100% concluída e validada: a IA lê os documentos do CFA, busca os trechos no Qdrant e responde com precisão citando as fontes oficiais).*

---

# PARTE 2: COM O TÉCNICO DE REDES E SEGURANÇA (FASE 2 — ⏳ PRÓXIMO PASSO)
> *Esta fase será realizada em conjunto com o responsável pela rede do CFA para garantir conformidade corporativa e disponibilidade contínua.*

---

## Tópicos de Alinhamento e Implantação da Fase 2:

### 1. Serviço `systemd` para a API FastAPI no Servidor `bulma`
* [ ] Criar o serviço `/etc/systemd/system/cfa-ia-api.service` para que a API (`src/app.py`) inicie automaticamente junto com o Oracle Linux e reinicie sozinha em caso de falha.

### 2. Endereçamento e Segmentação de Rede
* [ ] Fixar um **IP estático** para a máquina no DHCP/VLAN adequada (ex: VLAN de Serviços ou DMZ).
* [ ] Garantir que a máquina de IA não tenha rotas diretas para a rede corporativa crítica (apenas o que for estritamente necessário).

### 3. Configurações do `firewalld` no Oracle Linux
* [ ] Liberar a porta do serviço (ex: `8000` ou `443`) apenas para os IPs do Reverse Proxy ou da rede interna autorizada:
  ```bash
  sudo firewall-cmd --permanent --add-port=8000/tcp
  sudo firewall-cmd --reload
  ```
* [ ] Confirmar que `11434` (Ollama) e `6333` (Qdrant) continuam bloqueadas no firewall local.

### 4. Publicação no Sophos Firewall
* [ ] **Criação de Regra de WAF (Web Application Firewall):**
  * Apontar o subdomínio institucional (ex: `ia.cfa.org.br`) para o IP interno da máquina na porta do backend.
  * Ativar inspeção HTTPS com certificado SSL/TLS institucional (Let's Encrypt ou certificado próprio do CFA).
* [ ] **Proteção Anti-DDoS e Rate Limit no Sophos:**
  * Limitar a taxa de novas conexões HTTP por IP externo (evitar exaustão da GTX 1060).
  * Ativar o módulo IPS (Intrusion Prevention System) contra ataques web conhecidos.

### 5. Definição do Subdomínio e Restrição de CORS
* [ ] Definir o subdomínio oficial (ex: `ia.cfa.org.br`).
* [ ] Atualizar o `allow_origins` da API para permitir requisições **apenas** vindas de `https://cfa.org.br` (impedindo que outros sites utilizem a sua API de IA).

### 6. Incorporação do Widget no Portal CFA
* [ ] Desenvolver e adicionar o widget web (`cfa-chat.js`) no rodapé do portal institucional para exibição do botão flutuante de atendimento.
