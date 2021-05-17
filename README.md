## Instale

Antes de começar, verifique se você atendeu aos seguintes requisitos:

- Você o [docker](https://docs.docker.com/install/)?
- Você instalou o [docker-compose](https://docs.docker.com/compose/install/)?

## Clone

```shell
git clone https://gitlab.com/herlanassis/semctra-project
```

<!-- Depois clone os projetos `semctra-web` e `semctra-backend` dentro do diretório `semctra-project`

```shell
git clone https://gitlab.com/herlanassis/semctra-web web/; \
git clone https://gitlab.com/herlanassis/semctra-backend backend/;
``` -->

## Executando no modo DEV

1. Dentro da pasta semctra-project/backend execute:

```shell
pip install -r requirements.txt && python manage.py runserver
```

Obs: Configurar váriáveis de ambiente

2. Dentro da pasta semctra-project/web execute:

```shell
npm install && npm run dev
```

Obs: Configurar váriáveis de ambiente

3. Acesse a página página [http://localhost:9528/](http://localhost:9528/) para acessar o projeto web e [http://localhost:8000/](http://localhost:8000/) para acessar o projeto backend.

## Executando no modo PROD

1. Dentro da pasta semctra-project execute:

```shell
docker-compose up -d --build
```

2. Acesse a página página [http://localhost/](http://localhost/).

## Dúdivas?

- [comandos docker](https://devhints.io/docker-compose);
