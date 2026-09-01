# Twitter Clone

Projeto desenvolvido com Django, simulando as principais funcionalidades de uma rede social.

## Funcionalidades

- Cadastro de usuários
- Login e logout
- Alteração de perfil
- Alteração de nome de usuário
- Alteração de nome
- Alteração de e-mail
- Alteração de foto de perfil
- Alteração de senha
- Sistema de seguidores
- Sistema de seguir e deixar de seguir usuários
- Feed com publicações dos usuários seguidos
- Criação de publicações
- Curtidas
- Comentários
- API REST
- Banco de dados PostgreSQL
- Upload de imagens utilizando Cloudinary
- Deploy online utilizando Render

## Tecnologias

- Python
- Django
- Django REST Framework
- PostgreSQL
- Cloudinary
- HTML
- CSS
- Render
- GitHub

## Como executar localmente

Clone o projeto:

    git clone https://github.com/silas-souza/TwitterClone.git

Entre na pasta:

    cd TwitterClone

Instale as dependências:

    poetry install

Execute as migrações:

    poetry run python manage.py migrate

Inicie o servidor:

    poetry run python manage.py runserver

Acesse:

    http://127.0.0.1:8000/

## Deploy

Aplicação disponível online:

https://twitterclone-6s3i.onrender.com

## GitHub

https://github.com/silas-souza/TwitterClone