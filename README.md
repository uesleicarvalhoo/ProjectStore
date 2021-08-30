# Store

Sistema de controle de estoque e registro de vendas

## TODO's

### Web

- [X] Exibir uma mensagem de erro quando levantar as exceções
- [ ] Dashboard
- [ ] View de Clientes
- [ ] View de Estoque
- [ ] View de Vendas
- [ ] View de Notas Fiscais

### API

### Database

- [ ] Vincular as compras aos Clientes
- [ ] Adicionar um campo "data" JSON a tabela clients para incluir informações extras
- [ ] Utilizar o SQLModel

#### Core

- [ ] Modificar os eventos para ficar com o código e descrição
- [ ] Gerar uma nota fiscal para as ordens de compra
- [ ] Acrescentar os detalhes do pagamento ao pedido
- [X] Salvar as mensagens em request.state.messages, passar para o template as mensagens e expira-las do redis
- [X] Migrar as dependencias para a pasta correta

### Testes

- [ ] Implementar os testes da API
- [ ] Implementar os testes da Web
- [ ] Implementar o Mock das classes para testes

### Outros

- [ ] Aprovar a PR automaticamente de acordo com os testes e linters
- [ ] Adicionar o prospector ao projeto
- [ ] Implementar o git pre-commit no projeto
