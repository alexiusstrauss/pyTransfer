from rest_framework import status
from django.urls import reverse
from rest_framework.test import APITestCase
from pytransfer.models import Pessoa, Token, Balance


class PyTestProject(APITestCase):
    '''
    Classe responsavel por efetuar todos os testes da API
    '''

    url_pessoa = reverse('pessoas-list-create')
    url_history = reverse('historys-list')

    Alexius = {
        'nome': 'Alexius',
        'sobrenome': 'Strauss',
        'nomecompleto': 'Alexius Strauss Marques',
        'email': 'alexius@gmail.com',
        'telefone': '82999999991',
        'cpf': '00000000001'
    }

    Luis = {
        'nome': 'Luis',
        'sobrenome': 'Alberto',
        'nomecompleto': 'Luis Alberto',
        'email': 'luis@gmail.com',
        'telefone': '82999999992',
        'cpf': '00000000002'
    }

    Fernando = {
        'nome': 'Fernando',
        'sobrenome': 'Lima',
        'nomecompleto': 'Fernando Lima',
        'email': 'fernando@gmail.com',
        'telefone': '82999999993',
        'cpf': '00000000003'
    }

    Alice = {
        'nome': 'Alice',
        'sobrenome': 'Feitosa',
        'nomecompleto': 'Alice Feitosa',
        'email': 'alicefeitosa@gmail.com',
        'telefone': '82999999994',
        'cpf': '00000000004'
    }

    def setUp(self):
        """
        Iniciando o SetUp de test            
        """
        response = self.client.post(
            self.url_pessoa, self.Alexius, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post(self.url_pessoa, self.Luis, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post(
            self.url_pessoa, self.Fernando, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post(self.url_pessoa, self.Alice, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Pessoa.objects.count(), 4)
        self.assertEqual(Pessoa.objects.first().nome, 'Alexius')
        self.assertEqual(Pessoa.objects.last().nome, 'Alice')

    def test_verifica_criacao_token_vinculado_a_pessoa(self):
        """
            Verifica se ha um token para a pessoa de test
        """
        self.assertEqual(Token.objects.count(), Pessoa.objects.count())
        self.assertEqual(
            Token.objects.filter(pessoa_id=Pessoa.objects.first().id).get().id,
            Pessoa.objects.first().id
        )

    def test_verifica__ha_saldo_vinculado_a_pessoa(self):
        '''
        Verifica se foi criado um saldo aleatorio para objeto Pessoa
        '''
        # Verifica se todas as pessoas criadas, possuem um saldo na tabela balance
        self.assertEqual(Balance.objects.count(), Pessoa.objects.count())
        self.assertEqual(Balance.objects.first().valor >= 0, True)
        # confere se o saldo da primeira pessoa é igual ao saldo em balance.
        self.assertEqual(
            Balance.objects.first().valor,
            Pessoa.objects.first().balance
        )

    def test_testar_deletar_ultima_pessoa(self):
        '''
        Deleta a ultima pessoa, para testar se o token sera desastivado para transcacoes
        '''
        pessoa = Pessoa.objects.last()
        url = reverse('pessoas-reatrive', kwargs={'pk': pessoa.id})

        # testa Delete na API da Pessoa Passando PK como parametro
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Tenta novamente Delete na mesma PK
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_testar_transferir_para_token_cancelado(self):
        '''
        Testa se o token destino nao esta cancelado para receber transferencia
        '''
        token = Token.objects.last()
        # desativa pessoa
        token.pessoa.ativo = False
        token.pessoa.save()

        payload = {
            "remetente": 1,
            "token_destino": token.codigo,
            "valor": 5,
            "status": "Finalizado"
        }

        url = reverse('historys-list')
        response = self.client.post(url, payload, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_verificar_erro_transferir_para_proprio_token(self):
        '''
        Testa o erro de tentativa de transferir para o proprio token
        '''

        token = Token.objects.last()

        payload = {
            "remetente": token.pessoa.id,  # passando o mesmo id do token destino
            "token_destino": token.codigo,
            "valor": 5,
            "status": "Finalizado"
        }

        url = reverse('historys-list')
        response = self.client.post(url, payload, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_verificar_se_tem_saldo_suficiente(self):
        '''
        Testa se o saldo na conta é maior ou igual ao valor a ser transferido
        '''
        token = Token.objects.last()

        payload = {
            "remetente": 1,  # passando o mesmo id do token destino
            "token_destino": token.codigo,
            # valor maior que saldo em conta
            "valor": (token.pessoa.balance + 9000),
            "status": "Finalizado"
        }

        url = reverse('historys-list')
        response = self.client.post(url, payload, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_transferir_entre_duas_pessoas(self):
        '''
        Efetua uma transferencia de valores entre contas usando token
        '''

        remetente = Pessoa.objects.first()
        destinatario = Pessoa.objects.last()

        valor_transacao = 1

        payload = {
            # primeira pessoa (remetente)
            "remetente": remetente.id,
            "token_destino": destinatario.token.codigo,  # destinatario
            "valor": valor_transacao,
            "status": "Executando"
        }

        url = reverse('historys-list')
        response = self.client.post(url, payload, format='json')
        assert response.status_code == status.HTTP_201_CREATED

    def test_verificar_saldo_transferencia_status_pendente(self):
        '''
        Efetua o teste de bloquendo o valor da transferencia da conta do remetente
        '''

        remetente = Pessoa.objects.first()
        destinatario = Pessoa.objects.last()

        # valores iniciais
        remetente_saldo = Pessoa.objects.first().balance
        destinatario_saldo = Pessoa.objects.last().balance
        valor_transacao = 1

        payload = {
            # primeira pessoa (remetente)
            "remetente": remetente.id,
            "token_destino": destinatario.token.codigo,  # destinatario
            "valor": valor_transacao,
            "status": "Pendente"
        }

        url = reverse('historys-list')
        response = self.client.post(url, payload, format='json')
        assert response.status_code == status.HTTP_201_CREATED

        # destinatario saldo = saldo inicial
        self.assertEqual(destinatario_saldo, destinatario.balance)

        # remetente fica com valor da transacao bloqueado. ficando balance-transacao
        self.assertEqual(remetente.balance,
                         (remetente_saldo - valor_transacao))

    def test_verificar_saldo_transferencia_status_executando(self):
        '''
        Efetua o teste de bloquendo o valor da transferencia da conta do remetente
        '''

        remetente = Pessoa.objects.first()
        destinatario = Pessoa.objects.last()

        # valores iniciais
        remetente_saldo = Pessoa.objects.first().balance
        destinatario_saldo = Pessoa.objects.last().balance
        valor_transacao = 1

        payload = {
            # primeira pessoa (remetente)
            "remetente": remetente.id,
            "token_destino": destinatario.token.codigo,  # destinatario
            "valor": valor_transacao,
            "status": "Executando"
        }

        url = reverse('historys-list')
        response = self.client.post(url, payload, format='json')
        assert response.status_code == status.HTTP_201_CREATED

        # destinatario saldo = saldo inicial
        self.assertEqual(destinatario_saldo, destinatario.balance)

        # remetente fica com valor da transacao bloqueado. ficando balance-transacao
        self.assertEqual(remetente.balance,
                         (remetente_saldo - valor_transacao))

    def test_verificar_saldo_transferencia_status_finalizado(self):
        '''
        Efetua o teste de adicionar o valor transferido no destinatario
        Retirando o valor transferido do remetente
        '''
        remetente = Pessoa.objects.first()
        destinatario = Pessoa.objects.last()

        # valores iniciais
        remetente_saldo = Pessoa.objects.first().balance
        destinatario_saldo = Pessoa.objects.last().balance
        valor_transacao = 1

        payload = {
            # primeira pessoa (remetente)
            "remetente": remetente.id,
            "token_destino": destinatario.token.codigo,  # destinatario
            "valor": valor_transacao,
            "status": "Finalizado"
        }

        url = reverse('historys-list')
        response = self.client.post(url, payload, format='json')
        assert response.status_code == status.HTTP_201_CREATED

        # remetente saldo = saldo inicial - valor transferido
        self.assertEqual(remetente.balance, (remetente_saldo - 1))

        # destinatario saldo = saldo inicial + valor transferido
        self.assertEqual(destinatario.balance,
                         (destinatario_saldo + valor_transacao))

    def test_listar_todas_historys(self):
        '''
        Listando todas as transferencias
        '''
        response = self.client.get('/api/historys/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
