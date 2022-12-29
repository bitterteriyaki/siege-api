# poc-api-python
A Proof of Concept for API development in Python.

## Goals
- [ ] User
  - [ ] `POST /api/v1/users`: Signup
  - [ ] `GET /api/v1/users`: Login
  - [ ] `PATCH /api/v1/users`: Modificar usuário
- [ ] Server
  - [ ] `POST /api/v1/guilds`: Criar servidor
  - [ ] `PATCH /api/v1/guilds/{guild.id}`: Modificar servidor
  - [ ] `DELETE /api/v1/guilds/{guild.id}`: Deletar servidor
- [ ] Channel
  - [ ] `POST /api/v1/guilds/{guild.id}/channels`: Criar canal
  - [ ] `PATCH /api/v1/guilds/{guild.id}/channels/{channel.id}`: Modificar canal
  - [ ] `DELETE /api/v1/guilds/{guild.id}/channels/{channel.id}`: Deletar canal
