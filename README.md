# pyTransfer

PyTransfer - Serviço de transferencia feito em python.


Instalação
git clone https://github.com/alexiusstrauss/pyTransfer.git

acesse a pasta pyTransfer
cd /pyTransfer

#Criando a imagem e rodando o docker
docker-compose up -d --build

# comando para criar as tabelas
docker-compose exec web python manage.py migrate

# caso queira acessar o admin do django, crie um super user
docker-compose exec web python manage.py createsuperuser

# comando para executar os testes do projeto
docker-compose exec web pytest -x

# poderá executar teste especifico 
docker-compose exec web pytest -k nome_do_teste

	Lista de funcoes para test
	

	- test_verifica_criacao_token_vinculado_a_pessoa
	- test_verifica__ha_saldo_vinculado_a_pessoa
	- test_testar_deletar_ultima_pessoa
	- test_testar_transferir_para_token_cancelado
	- test_verificar_erro_transferir_para_proprio_token
	- test_verificar_se_tem_saldo_suficiente
	- test_transferir_entre_duas_pessoas
	- test_verificar_saldo_transferencia_status_pendente
	- test_verificar_saldo_transferencia_status_executando
	- test_verificar_saldo_transferencia_status_finalizado
	- test_listar_todas_historys



Para acesssar o serviço estará rodando no localhost na porta 8000
http://127.0.0.1:8000

# endpoins estão listados abaixo:

http://127.0.0.1:8000/api/pessoas/
http://127.0.0.1:8000/api/historys/

