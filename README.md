# getlinks

Aplicação para obter links de uma página web e armazenar em um banco de dados. Etapas:
- Recebe uma URL de uma página;
- Puxa todos os links dessa página;
- Armazena no banco de dados Redis;
- Repete o processo para cada link encontrado na página inicial;

Para executar, clone o repositório, certifique-se de ter o Docker e Docker compose instalados. Utilize os comandos "docker-compose build", e "docker-compose up". A aplicaçao executa em qualquer browser de internet pela porta 5000.
