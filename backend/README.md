# Store

<p align="center">Backend da aplicação para controle de vendas para micro e pequenas empresas 🚀</p>

<h4 align="center"> 🚧  🚀 Em construção...  🚧 </h4>

<p align="center">
<img src="https://img.shields.io/static/v1?label=License&message=MIT&color=7159c1&plastic"/>
<img src="https://img.shields.io/static/v1?label=Version&message=0.0.0&color=7159c1&plastic"/>
</p>

## Tabela de conteúdos

<!--ts-->
* [Instalação](#instalação)
* [Testes](#testes)
* [TODO's](#todo's)
* [Tecnologias](#tecnologias)
* [Licença](#licença)
* [Contato](#contato)

<!--te-->

## Instalação

### Pré-requisitos

Antes de começar, você vai precisar ter instalado em sua máquina as seguintes ferramentas:

* [Git](https://git-scm.com)
* [Python](https://www.python.org/) * Versão 3.9 ou superior
* [Poetry](https://python-poetry.org/docs/cli/)
* [PostgreSQL](https://www.postgresql.org/)
* [S3](https://aws.amazon.com/pt/s3/)

Dica: Para as dependencias de serviços externos o projeto você pode usar o docker-compose-dev.yaml para iniciar os containers, para conferir mais alguns docker-composes que eu utilizo no meu desenvolvimento, pode conferir o meu [Docker-Localstack]("https://github.com/uesleicarvalhoo/Docker-localstack").

Além disto é bom ter um editor para trabalhar com o código como [VSCode](https://code.visualstudio.com/)

### 🎲 Rodando a aplicação

```bash
# Clone este repositório
$ git clone <https://github.com/uesleicarvalhoo/Store>

# Acesse a pasta do projeto no terminal/cmd
$ cd Store

# Inicie os containers com as dependencias de desenvolvimento
$ docker-compose -f docker-compose-dev.yaml up -d

# Instale as dependências
$ poetry install
$ npm install

# Copie o arquivo .env.example para .env e altere as configurações das variaveis para as suas configurações
$ cp .env.example .env

# Execute a aplicação em modo de desenvolvimento
$ make run

# O servidor inciará na porta:5000 * acesse <http://localhost:5000/>
```

### Testes

A aplicação possui testes automatizados, para roda-los é bem simples, apenas execute o comando

```bash
# Executa os testes
$ make test
```

### TODO's

- [ ] Implementar testes de integração para a API e WEB
- [ ] Gerar notas fiscais para cada venda realizada
- [ ] Action para deploy na AWS
- [ ] Fazer testes de exclusão de um item após a venda ser finalizada
- [ ] Implementar o monitoramento de erros
- [ ] Implementar as lambdas/services
- [ ] Incluir as informações extras dos clientes
- [ ] Deploy do Backend
- [ ] Deploy do Frontend

### Tecnologias

As seguintes ferramentas foram usadas na construção do projeto:

* [FastAPI](https://fastapi.tiangolo.com/)
* [SQLModel](https://sqlmodel.tiangolo.com/)

### Licença

Este projeto está licenciado nos termos da licença MIT, para mais detalhes consulte o arquivo LICENSE.

### Contato

Olá, sou Ueslei Carvalho 👋🏻 criador e mantenedor deste projeto. Caso queira entrar em contato comigo, fique a vontade para utilizar qualquer um dos canais abaixo! :)

https://www.linkedin.com/in/uesleicarvalhoo/

📧 uesleicdoliveira@gmail.com

📷 https://www.instagram.com/uesleicarvalhoo/
