# Guia de Atualização e Sincronização do Repositório — Equipe CFA

Este guia estabelece o padrão para manter toda a equipe de infraestrutura e desenvolvimento do CFA **alinhada e atualizada** sempre que uma nova etapa for concluída, um script for modificado ou novas configurações forem adicionadas.

---

## 1. O Ciclo de Trabalho em Equipe

Para garantir que ninguém sobreponha o trabalho do colega nem trabalhe com código desatualizado, siga sempre este fluxo:

```
                  FLUXO DE SINCRONIZAÇÃO
   
   1. INÍCIO DO TRABALHO               2. FINALIZAÇÃO DA ETAPA
   +----------------------+            +-----------------------+
   | git pull origin main |  ===>      | Solicitar à IA para   |
   | (Baixa o que a equipe|            | atualizar a document. |
   |  fez de novo)        |            +-----------+-----------+
   +----------------------+                        |
                                                   v
   4. EQUIPE RECEBE                     3. ENVIO AO GITHUB
   +----------------------+            +-----------------------+
   | Próximo membro faz   |  <===      | git add .             |
   | git pull e continua  |            | git commit -m "..."   |
   +----------------------+            | git push origin main  |
                                       +-----------------------+
```

---

## 2. Passo 1: Antes de começar a mexer no código

Sempre abra o terminal na pasta do projeto e execute:
```bash
git pull origin main
```
* **O que faz:** Baixa qualquer alteração, novo documento ou script feito por outro membro da equipe.

---

## 3. Passo 2: Registrar a conclusão de uma etapa (com apoio da IA)

Você não precisa atualizar a documentação manualmente linha por linha. O próprio **Antigravity** pode fazer isso por você!

Sempre que concluir um teste ou etapa, envie no chat do Antigravity:
> *"Concluímos com sucesso a instalação do Ollama e o download dos modelos na máquina de testes. Atualize os documentos `docs/GUIA_IMPLANTACAO_IA_CFA.md` e `docs/CONVERSA_E_PLANEJAMENTO.md` marcando esta etapa como concluída e destacando o próximo passo."*

A IA atualizará os roteiros técnicos e os históricos de decisão automaticamente.

---

## 4. Passo 3: Enviar as alterações para o GitHub

Com o código testado e os documentos atualizados, execute no terminal:

```bash
# 1. Verificar quais arquivos foram alterados/criados
git status

# 2. Adicionar as alterações
git add .

# 3. Fazer o commit com mensagem clara
git commit -m "feat(fase1): instalacao do ollama e download dos modelos concluidos"

# 4. Enviar para o repositório oficial da equipe
git push origin main
```

---

## 5. Padrão Recomendado de Mensagens de Commit

Para manter o histórico do CFA organizado e profissional, use prefixos simples:

* `feat:` Quando criar um novo recurso ou concluir uma etapa do roteiro.
  * *Ex:* `git commit -m "feat: implementado script de indexacao dos pdfs"`
* `docs:` Quando atualizar documentações, históricos ou guias.
  * *Ex:* `git commit -m "docs: atualizado status de validacao dos drivers nvidia"`
* `fix:` Quando corrigir um bug em scripts ou configurações de rede.
  * *Ex:* `git commit -m "fix: ajuste na porta de conexao do qdrant"`
* `infra:` Quando alterar configurações de Docker, systemd ou firewall.
  * *Ex:* `git commit -m "infra: configurado servico systemd do ollama em loopback"`

---

## 6. O que fazer em caso de conflito (`git conflict`)?

Se você e outro membro da equipe alterarem o mesmo arquivo ao mesmo tempo e o Git acusar conflito ao fazer `git push`:
1. Execute:
   ```bash
   git pull origin main
   ```
2. Abra o arquivo indicado no Antigravity e diga no chat:
   > *"Tive um conflito de merge no arquivo X. Pode me ajudar a resolver mantendo as alterações mais recentes da equipe?"*
3. O assistente resolverá o conflito perfeitamente preservando os dois lados. Em seguida, basta rodar `git add .`, `git commit -m "merge: resolucao de conflito"` e `git push origin main`.
