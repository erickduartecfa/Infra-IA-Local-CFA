# Guia de Entrada da Equipe — Como Trabalhar com o Antigravity

Este guia orienta qualquer membro da equipe de Infraestrutura / TI do CFA a carregar o projeto no **Antigravity** e continuar o desenvolvimento da **IA Local do CFA** com contexto total compartilhado.

---

## 1. Pré-Requisitos

1. **Acesso ao GitHub:** Ter aceitado o convite de colaborador do repositório privado:
   * URL: `https://github.com/erickduartecfa/Infra-IA-Local-CFA`
2. **Git instalado:** [git-scm.com](https://git-scm.com/) instalado na máquina.
3. **Antigravity instalado:** Ter o Antigravity configurado no computador de trabalho.

---

## 2. Passo a Passo de Inicialização

### Passo 1: Clonar o Repositório
Abra o terminal (PowerShell, Prompt de Comando ou Bash) e execute:

```bash
git clone https://github.com/erickduartecfa/Infra-IA-Local-CFA.git
```

---

### Passo 2: Abrir o Projeto no Antigravity
1. Abra o **Antigravity**.
2. No menu superior ou na tela inicial, clique em **Open Workspace** (ou `File` > `Open Folder`).
3. Selecione a pasta clonada: `Infra-IA-Local-CFA`.

---

### Passo 3: O Antigravity já sabe tudo automaticamente
Você **não precisa** explicar o projeto, copiar histórico anterior ou ensinar regras.
* O arquivo `GEMINI.md` localizado na raiz do projeto é lido e ativado automaticamente pelo Antigravity.
* A IA já tem ciência do hardware (i7, 32GB RAM, GTX 1060 6GB), do Oracle Linux, dos modelos (`qwen2.5:7b` e `bge-m3`) e de todas as decisões tomadas.

---

### Passo 4: Como Iniciar a Conversa no Chat

Basta abrir o chat no Antigravity e enviar uma mensagem simples como:

> *"Olá! Sou da equipe de infraestrutura do CFA e estou assumindo o projeto. Em qual etapa da Fase 1 estamos e o que devemos executar agora?"*

Ou para tarefas específicas:
* *"Como testo os drivers da GPU e preparo o serviço do Ollama no Oracle Linux?"*
* *"Como subo o Qdrant localmente no Docker e indexo o primeiro PDF?"*

---

## 3. Boas Práticas de Trabalho com o Git

Para manter o projeto sempre sincronizado entre os membros da equipe:

1. **Antes de começar a trabalhar no dia:**
   ```bash
   git pull origin main
   ```
2. **Ao concluir um script ou teste:**
   ```bash
   git add .
   git commit -m "feat: descrição da melhoria realizada"
   git push origin main
   ```

---

## 4. Documentos de Apoio Disponíveis no Repositório

* `docs/GUIA_IMPLANTACAO_IA_CFA.md`: Roteiro técnico completo linha por linha para as Fases 1 e 2.
* `docs/CONVERSA_E_PLANEJAMENTO.md`: Histórico de alinhamentos estratégicos.
* `README.md`: Visão geral e arquitetura.
