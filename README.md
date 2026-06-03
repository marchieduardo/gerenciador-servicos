# 🛠️ Gerenciador de Serviços

Sistema web desenvolvido em Django para gerenciamento de clientes e ordens de serviço. Permite cadastrar clientes, registrar serviços com status e valor, e anexar arquivos (imagens, vídeos e documentos) diretamente em cada serviço.

---

## ✨ Funcionalidades

### Clientes
- Cadastro de clientes com nome, documento, e-mail, telefone e endereço
- Listagem com **busca textual** (nome, documento, e-mail, telefone, endereço) e **filtro por status** (ativo/inativo)
- Visualização da página de detalhes do cliente com todos os seus serviços vinculados
- Edição de dados do cliente
- Controle de clientes ativos e inativos

### Serviços
- Registro de serviços vinculados a um cliente ativo
- Campos: descrição, data, valor e status (`Pendente`, `Concluído` ou `Cancelado`)
- Listagem com **busca textual** (nome do cliente ou descrição), **filtro por status** e **ordenação por data** (mais recentes ou mais antigos)
- Visualização detalhada do serviço com todos os anexos
- Edição e exclusão de serviços
- **Navegação inteligente**: ao excluir um serviço, o usuário é redirecionado para a última página de origem (lista de serviços ou detalhes do cliente)

### Anexos
- Upload de **múltiplos arquivos** por serviço (imagens, vídeos e outros documentos)
- Renderização automática na página de detalhes: imagens exibidas inline, vídeos com player nativo, outros arquivos como link para download
- Exclusão individual de anexos via requisição AJAX
- Remoção automática do arquivo físico do disco ao excluir um anexo (via Django Signals)

### Administração
- Painel administrativo do Django (`/admin/`) com configuração personalizada para clientes, serviços e anexos
- Filtros, campos de busca e ordenação configurados para cada modelo
- Gerenciamento de anexos inline dentro da tela de edição de serviço

---

## 🧰 Tecnologias Utilizadas

| Tecnologia | Versão | Uso |
|---|---|---|
| [Python](https://www.python.org/) | 3.x | Linguagem principal |
| [Django](https://www.djangoproject.com/) | 6.0.4 | Framework web |
| [python-dotenv](https://github.com/theskumar/python-dotenv) | 1.2.2 | Gerenciamento de variáveis de ambiente |
| [SQLite](https://www.sqlite.org/) | — | Banco de dados (padrão Django) |
| HTML / CSS | — | Templates e estilização |

---

## 📁 Estrutura do Projeto

```
gerenciador-servicos/
├── app/                        # Configurações do projeto Django
│   ├── settings.py             # Configurações gerais (BD, apps, locale, media)
│   ├── urls.py                 # Roteamento principal
│   ├── wsgi.py
│   └── asgi.py
│
├── clientes/                   # App principal (único app do projeto)
│   ├── migrations/             # Histórico de migrações do banco de dados
│   ├── static/clientes/        # Arquivos estáticos do app
│   ├── templates/              # Templates HTML do app
│   │   ├── base_servicos.html
│   │   ├── lista_clientes.html
│   │   ├── criar_cliente.html
│   │   ├── detalhes_cliente.html
│   │   ├── editar_cliente.html
│   │   ├── lista_servicos.html
│   │   ├── criar_servico.html
│   │   ├── detalhes_servico.html
│   │   ├── editar_servico.html
│   │   └── excluir_servico.html
│   ├── admin.py                # Configuração do painel administrativo
│   ├── apps.py                 # Registro de signals via AppConfig
│   ├── forms.py                # Formulários (inclui upload de múltiplos arquivos)
│   ├── models.py               # Modelos: Cliente, Servico, AnexoServico
│   ├── signals.py              # Signal para exclusão física de anexos do disco
│   ├── urls.py                 # Rotas do app clientes
│   └── views.py                # Views baseadas em classe (CRUD completo)
│
├── media/                      # Arquivos de mídia enviados pelos usuários (gerado em runtime)
├── static/                     # Arquivos estáticos globais
│   └── css/style.css
├── templates/                  # Templates globais
│   └── base.html               # Template base com nav e footer
│
├── .env                        # Variáveis de ambiente (não versionado)
├── .env.example                # Modelo de variáveis (versionado)
├── .gitignore
├── db.sqlite3                  # Banco de dados SQLite (não versionado)
├── manage.py
└── requirements.txt
```

---

## 🚀 Instalação

### Pré-requisitos

- Python 3.10 ou superior instalado
- Git instalado

### 1. Clone o repositório

```bash
git clone https://github.com/marchieduardo/gerenciador-servicos.git
cd gerenciador-servicos
```

### 2. Crie e ative o ambiente virtual

**Windows:**
```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

**Linux / macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

---

## ⚙️ Configuração do Ambiente

Copie o arquivo de exemplo e preencha os valores:

**Windows:**
```powershell
copy .env.example .env
```

**Linux / macOS:**
```bash
cp .env.example .env
```

Edite o `.env` e substitua `SECRET_KEY=sua-chave-secreta-aqui` por uma chave gerada (veja abaixo).

> ⚠️ **Nunca versione o arquivo `.env`** — ele já está incluído no `.gitignore`.  
> O modelo versionado é o `.env.example`.

Para gerar uma `SECRET_KEY` segura, você pode usar o próprio Django:

**Windows / Linux:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

## ▶️ Como Executar

### 1. Aplique as migrações

**Windows:**
```powershell
python manage.py migrate
```

**Linux / macOS:**
```bash
python3 manage.py migrate
```

### 2. (Opcional) Crie um superusuário para o painel administrativo

**Windows:**
```powershell
python manage.py createsuperuser
```

**Linux / macOS:**
```bash
python3 manage.py createsuperuser
```

### 3. Inicie o servidor de desenvolvimento

**Windows:**
```powershell
python manage.py runserver
```

**Linux / macOS:**
```bash
python3 manage.py runserver
```

Acesse em: [http://127.0.0.1:8000/clientes/](http://127.0.0.1:8000/clientes/)

Painel administrativo: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## 🔑 Variáveis de Ambiente

Consulte `.env.example` para o modelo completo com comentários. Resumo:

| Variável | Obrigatória | Descrição | Exemplo |
|---|---|---|---|
| `SECRET_KEY` | ✅ Sim | Chave secreta do Django | `django-insecure-...` |
| `DEBUG` | ❌ Não | Modo de depuração (padrão: `False`) | `True` |
| `ALLOWED_HOSTS` | ❌ Não | Hosts permitidos separados por vírgula | `127.0.0.1,localhost` |

---

## 🗄️ Banco de Dados

O projeto utiliza **SQLite** (banco de dados padrão do Django), que não requer nenhuma configuração adicional. O arquivo `db.sqlite3` é gerado automaticamente na raiz do projeto ao executar as migrações.

> O arquivo `db.sqlite3` está incluído no `.gitignore` e não é versionado.

---

## 🔐 Autenticação

O projeto utiliza o sistema de autenticação nativo do Django, disponível no painel administrativo (`/admin/`). As rotas da aplicação principal **não possuem restrição de acesso** implementada atualmente.

---

## 🗺️ Rotas Disponíveis

| Método | URL | Descrição |
|---|---|---|
| GET | `/clientes/` | Lista todos os clientes |
| GET/POST | `/clientes/novo/` | Cadastro de novo cliente |
| GET | `/clientes/<id>/` | Detalhes do cliente |
| GET/POST | `/clientes/<id>/editar/` | Edição do cliente |
| GET/POST | `/clientes/<id>/novo-servico/` | Cadastro de serviço para o cliente |
| GET | `/servicos/` | Lista todos os serviços |
| GET | `/servicos/<id>/` | Detalhes do serviço |
| GET/POST | `/servicos/<id>/editar/` | Edição do serviço |
| GET/POST | `/servicos/<id>/excluir/` | Exclusão do serviço |
| DELETE | `/anexos/<id>/excluir/` | Exclusão de anexo (AJAX) |
| — | `/admin/` | Painel administrativo do Django |

---

## 🖼️ Screenshots

> 📌 *Screenshots serão adicionados em breve.*

| Tela | Descrição |
|---|---|
| Lista de Clientes | Listagem com busca e filtro por status |
| Detalhes do Cliente | Informações do cliente e serviços vinculados |
| Lista de Serviços | Listagem com busca, filtro por status e ordenação |
| Detalhes do Serviço | Informações do serviço com visualização de anexos |
| Formulário de Serviço | Criação/edição com upload de múltiplos arquivos |

---

## 🔭 Melhorias Futuras

- [ ] Implementar autenticação e controle de acesso por login nas rotas principais
- [ ] Migrar o banco de dados para **PostgreSQL**
- [ ] Adicionar paginação nas listas de clientes e serviços
- [ ] Adicionar testes automatizados (unitários e de integração)
- [ ] Melhorar o layout e a experiência visual
- [ ] Adicionar dashboard com resumo e estatísticas dos serviços

---

## 👤 Autor

**Eduardo Andrade Marchi**

- GitHub: [@marchieduardo](https://github.com/marchieduardo)

---

## 📄 Licença

Este projeto é de uso pessoal/estudos e não possui uma licença definida (todos os direitos reservados).
