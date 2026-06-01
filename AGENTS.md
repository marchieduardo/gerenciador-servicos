# Diretrizes para Assistentes de IA (AGENTS.md)

Este arquivo define as regras de desenvolvimento para os assistentes de IA neste projeto.

## 1. Interação e Codificação
- **Perguntas/Dúvidas:** Explique o conceito e pergunte se deseja a implementação antes de alterar qualquer código.
- **Preservação de Comentários:** Mantenha comentários explicativos existentes. Atualize-os apenas se a lógica correspondente for alterada.

## 2. Padrões de Código e Convenções (Django)
- **Banco de Dados:** NUNCA execute comandos de migração (`makemigrations` ou `migrate`) automaticamente. Apenas notifique a necessidade.
- **Autenticação:** Use sempre o Custom User Model do projeto (nunca importe o `User` padrão diretamente).
- **Views:** Priorize Class-Based Views (CBVs) em vez de views baseadas em funções.
- **Estilo:** Siga estritamente a PEP 8 e as melhores práticas de desenvolvimento Django.

## 3. Arquitetura do Projeto
- **Monolítico:** Backend e frontend acoplados no mesmo projeto Django (templates renderizados pelo servidor).

## 4. Padrão de Commit
- **Idioma/Estilo:** Português (Brasil), Conventional Commits, linha única e caixa baixa.
- **Formato:** `<tipo>(<escopo>): <descrição curta em minúsculas>`
- **Tipos:** `feat`, `fix`, `refactor`, `style`, `docs`, `chore`, `test`.
