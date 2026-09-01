# Twitter Clone API

API REST desenvolvida com Django e Django REST Framework como projeto final do curso.

A aplicação simula funcionalidades básicas de uma rede social de microblog, permitindo cadastro de usuários, autenticação, gerenciamento de perfil, criação de postagens, seguidores, curtidas e comentários.

## Tecnologias

- Python 3.13
- Django 6.1
- Django REST Framework
- Poetry
- SQLite
- Token Authentication
- Git e GitHub

## Funcionalidades

### Usuários

- Cadastro de usuários
- Autenticação por Token
- Consulta do próprio perfil
- Atualização do perfil
- Foto de perfil
- Seguir usuários
- Lista de usuários seguidos

### Postagens

- Criar postagem
- Listar postagens
- Atualizar postagem
- Excluir postagem
- Feed baseado em usuários seguidos

### Curtidas

- Curtir uma postagem
- Remover curtida
- Contagem de curtidas
- Impedir curtida duplicada

### Comentários

- Criar comentário
- Listar comentários
- Excluir comentário
- Identificação automática do autor

## Instalação

Clone o repositório:

```bash
git clone https://github.com/silas-souza/TwitterClone.git
cd TwitterClone