# Store

Sistema de controle de estoque e registro de vendas

## TODO's

### Web

- [X] Exibir uma mensagem de erro quando levantar as exceções
- [ ] Dashboard
- [X] View de Clientes
- [X] View de Estoque
- [X] View de Vendas
- [X] View de Notas Fiscais
- [X] Colocar a borda roxa para destacar todas as views
- [X] Destacar em negrito sempre a view atual
- [ ] Na view de clientes, colocar lá os detalhes das compras

### API

### Database

- [X] Vincular as compras aos Clientes
- [ ] Adicionar um campo "data" JSON a tabela clients para incluir informações extras
- [X] Utilizar o SQLModel
- [ ] Incluir um campo Detalhes nas vendas

#### Core

- [ ] Modificar os eventos para ficar com o código e descrição
- [X] Trocar o nome da pasta from src.core import controller para handlers ou algo que faça mais sentido
- [ ] Gerar uma nota fiscal para as ordens de compra
- [ ] Acrescentar os detalhes do pagamento ao pedido
- [X] Salvar as mensagens em request.state.messages, passar para o template as mensagens e expira-las do redis
- [X] Migrar as dependencias para a pasta correta
- [ ] Trocar todos os IDs para UUID

### Testes

- [ ] Implementar os testes da API
- [ ] Implementar os testes da Web
- [ ] Implementar o Mock das classes para testes
- [ ] Implementar o Factory Boy para gerar os objetos

### Outros

- [ ] Aprovar a PR automaticamente de acordo com os testes e linters
- [ ] Adicionar o prospector ao projeto
- [ ] Implementar o git pre-commit no projeto
