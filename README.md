# Singolar API

- API construída em Django/Django Rest Framework,que permite a gerência de Usuários, Posts, Comentários e Likes.

## Instalação do projeto

### Pré-requisitos
   - Docker
   - docker-compose
   - Make (opcional)

Em seu terminal preferido:
1. Clone o projeto
   - `git clone https://github.com/dantas-jl/api-singolar.git`
2. Localize e entre na pasta que acabou de ser clonada
   - `cd api-singolar`
3. Rodar o projeto com o auxílio do Docker. Os comandos a seguir constroem as imagens docker e iniciam as aplicações
   - Em ambientes Linux
     - `docker-compose -f docker-compose.yml up` ou
`make up` (Com o make instalado)
   - Em ambientes Windows*
     - `docker-compose -f docker-compose.yml up`

*Caso tenha optado por utilizar o Windows e tenha se deparado com a seguinte mensagem: `exec /usr/src/app/entrypoint.sh: no such file or directory`, não se preocupe! Basta mudar a assinatura do `End of Line Sequence` do `entrypoint.sh` de CLRF para LF (a representação padrão do UNIX), essa mudança pode ser feita tranquilamente em seu editor de código preferido.
No vscode o [End of Line Sequence](https://i.stack.imgur.com/Y058o.png) pode ser localizada no canto inferior direito. 

## Domínio do problema

O domínio foi modelado utilizando UML, conforme demonstrado a seguir:
![Domínio Singolar UML](/doc/singolar-domain.png)

## Recursos
- Usuários (`/users`)
- Tokens JWT (`/login` e `/refresh`)
- Posts (`/posts/`)*
- Comentários (`/comments`)*
- Likes (`/likes`)*

*Esses recursos necessitam de autenticação JWT para serem consumidos.
*Os recursos só podem ser atualizados/editados/excluídos pelos autores.

## Casos de uso implementados e exemplos de entradas e saídas JSON

- Os recursos 3, 4 e 5, precisam de assinatura de tokens JWT para serem acessados. A assinatura deve estar presente nos headers da requisição: `Authorization: "Bearer acess_token"`
- O envio de fotos podem ser realizados para os recursos: Users e Posts, mas requerem o `content-type: multipart/form-data` em suas requisições.

### 1. Tokens
|Funcionalidade|Verbo HTTP|URI|Entrada|Saída|
|---|---|---|---|---|
|Login|POST|`/api/login/`|[Request](/doc/json_examples/tokens/request.json)|[Response](/doc/json_examples/tokens/response.json)|
|Refresh|POST|`/api/login/`|[Request](/doc/json_examples//tokens/refresh_request.json)|[Response](/doc/json_examples/tokens/refresh_response.json)|


### 2. Users
|Funcionalidade|Verbo HTTP|URI|Entrada|Saída|
|---|---|---|---|---|
|Cadastrar Usuário|POST|`/api/users/`|[Request](/doc/json_examples/users/post_users_request.json)|[Response](/doc/json_examples/users/post_users_response.json)|
|Listar Usuários|GET|`/api/users/`|-|[Response](/doc/json_examples/users/list_users_response.json)|
|Recuperar Usuário|GET|`/api/users/<int:id_user>/`|-|[Response](/doc/json_examples/users/retrieve_user_response.json)|
|Alterar Usuário|PUT|`/api/users/<int:id_user>/`|[Request](/doc/json_examples/users/put_user_request.json)|[Response](/doc/json_examples/users/post_users_response.json)|
|Alterar Usuário Parcialmente|PATCH|`/api/users/<int:id_user>/`|[Request](/doc/json_examples/users/post_users_response.json)|[Response](/doc/json_examples/users/post_users_response.json)|
|Deletar Usuário|DELETE|`/api/users/<int:id_user>/`|-|-|


### 3. Posts
|Funcionalidade|Verbo HTTP|URI|Entrada|Saída|
|---|---|---|---|---|
|Cadastrar Post|POST|`/api/posts/`|[Request](/doc/json_examples/posts/post_posts_request.json)|[Response](/doc/json_examples/posts/post_posts_response.json)|
|Listar Posts|GET|`/api/posts/`|-|[Response](/doc/json_examples/posts/list_posts_response.json)|
|Recuperar Post|GET|`/api/posts/<int:id_post>/`|-|[Response](/doc/json_examples/posts/retrieve_post_response.json)|
|Alterar Post|PUT|`/api/posts/<int:id_post>/`|[Request](/doc/json_examples/posts/put_posts_request.json)|[Response](/doc/json_examples/posts/retrieve_post_response.json)|
|Alterar Post Parcialmente|PATCH|`/api/users/<int:id_post>/`|[Request](/doc/json_examples/posts/put_posts_request.json)|[Response](/doc/json_examples/posts/retrieve_post_response.json)|
|Deletar Post|DELETE|`/api/posts/<int:id_post>/`|-|-|
|Listar Comentários de um Post|GET|`/api/posts/<int:id_post>/comments/`|-|[Response](/doc/json_examples/posts/comments_post_response.json)|
|Recuperar Comentário de um Post|GET|`/api/posts/<int:id_post>/comments/<int:id_comment>/`|-|[Response](/doc/json_examples/posts/retrieve_comment_post_response.json)|
|Listar likes de Comentário de um Post|GET|`/api/posts/<int:id_post>/comments/<int:id_comment>/likes/`|-|[Response](/doc/json_examples/posts/likes_comments_post_response.json)|
|Recuperar like de Comentário de um Post|GET|`/api/posts/<int:id_post>/comments/<int:id_comment>/likes/<id:id_like>`|-|[Response](/doc/json_examples/posts/retrieve_likes_comments_post_response.json)|

### 4. Comments
|Funcionalidade|Verbo HTTP|URI|Entrada|Saída|
|---|---|---|---|---|
|Cadastrar Comentário|POST|`/api/comments/`|[Request](/doc/json_examples/comments/request_comment_post.json)|[Response](/doc/json_examples/comments/response_comment_post.json)|
|Listar Comentários|GET|`/api/comments/`|-|[Response](/doc/json_examples/comments/response_list_comment.json)|
|Recuperar Comentário|GET|`/api/comments/<int:id_comment>/`|-|[Response](/doc/json_examples/comments/response_retrieve_comment.json)|
|Alterar Comentário|PUT|`/api/comments/<int:id_comment>/`|[Request](/doc/json_examples/comments/request_comment_put.json)|[Response](/doc/json_examples/comments/response_comment_post.json)|
|Alterar Comentário Parcialmente|PATCH|`/api/comments/<int:id_comment>/`|[Request](/doc/json_examples/comments/request_comment_put.json)|[Response](/doc/json_examples/comments/response_comment_post.json)|
|Deletar Comentário|DELETE|`/api/comments/<int:id_comment>/`|-|-|
|Listar Likes de um Comentário|GET|`/api/comments/<int:id_comment>/likes/`|-|[Response](/doc/json_examples/posts/likes_comments_post_response.json)|
|Recuperar Like de um Comentário|GET|`/api/comments/<int:id_comment>/likes/`|-|[Response](/doc/json_examples/posts/retrieve_likes_comments_post_response.json)|

### 5. Likes
|Funcionalidade|Verbo HTTP|URI|Entrada|Saída|
|---|---|---|---|---|
|Curtir Comentário|POST|`/api/likes/`|[Request](/doc/json_examples/likes/request_post_likes.json)|[Response](/doc/json_examples/likes/response_post_likes.json)|
|Listar Curtidas|GET|`/api/likes/`|-|[Response](/doc/json_examples/likes/response_list_likes.json)|
|Recuperar Curtida|GET|`/api/likes/<int:id_like>/`|-|[Response](/doc/json_examples/likes/response_retrieve_list_likes.json)|
|Descurtir Comentário|DELETE|`/api/likes/<int:id_like>/`|-|-|

## Complemento

- O projeto conta com testes unitários parciais para os recursos: Usuários e Posts. Com as aplicações rodando, confira os testes executando com:
   - `docker-compose -f docker-compose.yml exec api python manage.py test` ou `make test`
   - ![Run Tests](/doc/running_tests.png)
- O deploy do projeto foi realizado em [dantasjl.pythonanywhere.com](https://dantasjl.pythonanywhere.com/api/) e as rotas e recuros estão disponíveis para consumo HTTP.
- Caso queira utilizar um HTTP Client, aqui segue um exemplo de collection Postman: [Collection Postman](/doc/SingolarAPI.postman_collection.json)