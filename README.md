# Store

Sistema de controle de estoque e registro de vendas

## TODO's

### Web

- [X] Exibir uma mensagem de erro quando levantar as exceções
- [X] Dashboard
- [X] View de Clientes
- [X] View de Estoque
- [X] View de Vendas
- [X] View de Notas Fiscais
- [X] Colocar a borda roxa para destacar todas as views
- [X] Destacar em negrito sempre a view atual
- [X] Na view de clientes, colocar lá os detalhes das compras
- [X] Implementar o rodapé de paginação
- [X] Pagina para criação de novos usuários

### API

### Database

- [X] Incluir um campo de descrição nas vendas
- [ ] Trocar o nome dos Schemas de "GetModel" para "QueryModel"
- [ ] Remover a consulta por ID dos Schemas

#### Core

- [ ] Modificar os eventos para ficar com o código e descrição
- [ ] Gerar uma nota fiscal para as ordens de compra
- [ ] Acrescentar os detalhes do pagamento ao pedido
- [X] Trocar todos os IDs para UUID
- [X] Colocar as descrições em Ingles

### Testes

- [ ] Implementar os testes da API
- [ ] Implementar os testes da Web
- [ ] Implementar o Mock das classes para testes
- [ ] Implementar o Factory Boy para gerar os objetos

### Outros

- [ ] Aprovar a PR automaticamente de acordo com os testes e linters
- [X] Implementar o git pre-commit no projeto
- [ ] Refatorar o projeto para utilizar micro-serviços (back e front)
- [ ] Criar um serviço para o envio de E-mails ao realizar novas vendas
- [ ] Montar o read-me do projeto
- [ ] Checar se a imagem do Dockerfile é a ideal pra PRD
- [ ] Mover os SGV para a pasta statics
