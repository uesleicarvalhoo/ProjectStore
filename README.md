# Store

Sistema de controle de estoque e registro de vendas

## TODO's

### Database

[*] Vincular as compras aos Clientes
[*] Adicionar um campo "data" JSON a tabela clients para incluir informações extras

#### Core

[*] Modificar os eventos para ficar com o código e descrição
[*] Gerar uma nota fiscal para as ordens de compra
[*] Acrescentar os detalhes do pagamento ao pedido
[*] Salvar as mensagens em request.state.messages, passar para o template as mensagens e expira-las do redis
[*] Utilizar a nova lib do SQLModel para os modelos do banco
[*] Migrar as dependencias para a pasta correta

### Testes

[*] Implementar os testes da API
[*] Implementar os testes da Web
[*] Implementar o Cache em branco para a pipeline de testes

### Web

[*] Exibir uma mensagem de erro quando levantar as exceções

### Outros

[*] Aprovar a PR automaticamente de acordo com os testes e linters
[*] Adicionar o prospector ao projeto
[*] Implementar o git pre-commit no projeto
