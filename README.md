# pyTransfer

PyTransfer - Serviço de transferencia feito em python.


## Usando Docker
```bash
git clone https://github.com/alexiusstrauss/pyTransfer.git
cd pyTransfer

docker-compose up -d --build

- crie as tabelas no banco de dados
docker-compose exec app python manage.py makemigrations
docker-compose exec app python manage.py migrate
docker-compose exec app python manage.py createsuperuser
```

## Testes
Lista de funcoes para test


```bash

docker-compose exec app pytest -x

docker-compose exec app pytest -k test_verifica_criacao_token_vinculado_a_pessoa
docker-compose exec app pytest -k test_verifica__ha_saldo_vinculado_a_pessoa
docker-compose exec app pytest -k test_testar_deletar_ultima_pessoa
docker-compose exec app pytest -k test_testar_transferir_para_token_cancelado
docker-compose exec app pytest -k test_verificar_erro_transferir_para_proprio_token
docker-compose exec app pytest -k test_verificar_se_tem_saldo_suficiente
docker-compose exec app pytest -k test_transferir_entre_duas_pessoas
docker-compose exec app pytest -k test_verificar_saldo_transferencia_status_pendente
docker-compose exec app pytest -k test_verificar_saldo_transferencia_status_executando
docker-compose exec app pytest -k test_verificar_saldo_transferencia_status_finalizado
docker-compose exec app pytest -k test_listar_todas_historys

```

Para acesssar, o serviço estará rodando em localhost na porta 8000
- http://127.0.0.1:8000

endpoins estão listados abaixo:

- http://127.0.0.1:8000/api/pessoas/
- http://127.0.0.1:8000/api/historys/

