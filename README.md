# Twitter Clone API

API REST desenvolvida com Django e Django REST Framework como projeto final do curso.

A aplicação simula funcionalidades básicas de uma rede social de microblog, permitindo cadastro de usuários, autenticação, gerenciamento de perfil, criação de postagens, seguidores, curtidas e comentários.

## Tecnologias

* Python 3.13
* Django 6.1
* Django REST Framework
* Poetry
* PostgreSQL
* Neon
* Token Authentication
* Gunicorn
* Render
* Git e GitHub

## Funcionalidades

### Usuários

* Cadastro de usuários
* Autenticação por Token
* Consulta do próprio perfil
* Atualização do perfil
* Foto de perfil
* Seguir usuários
* Lista de usuários seguidos

### Postagens

* Criar postagem
* Listar postagens
* Atualizar postagem
* Excluir postagem
* Feed baseado em usuários seguidos

### Curtidas

* Curtir uma postagem
* Remover curtida
* Contagem de curtidas
* Impedir curtida duplicada

### Comentários

* Criar comentário
* Listar comentários
* Excluir comentário
* Identificação automática do autor

## Banco de dados

O projeto utiliza PostgreSQL em produção através do Neon.

A conexão com o banco é configurada por meio de variáveis de ambiente, mantendo as credenciais fora do código-fonte.

## Deploy

A API está publicada em produção utilizando Render.

URL da API:

https://twitterclone-6s3i.onrender.com/

Endpoint principal:

https://twitterclone-6s3i.onrender.com/api/

## Instalação

Clone o repositório:

```bash
git clone https://github.com/silas-souza/TwitterClone.git
cd TwitterClone
```

Instale as dependências:

```bash
poetry install
```

Configure as variáveis de ambiente necessárias.

Execute as migrações:

```bash
poetry run python manage.py migrate
```

Execute o servidor local:

```bash
poetry run python manage.py runserver
```

## Testes

Para executar os testes automatizados:

```bash
poetry run python manage.py test
```

O projeto possui testes automatizados para validar suas principais funcionalidades.

## Produção

Para executar a aplicação utilizando Gunicorn:

```bash
gunicorn config.wsgi:application
```

O deploy em produção utiliza o PostgreSQL do Neon e o serviço Web do Render.
