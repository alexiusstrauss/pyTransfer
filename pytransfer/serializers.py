from .models                import Pessoa, History, Balance, Token
from django.core.exceptions import ObjectDoesNotExist
from .funcoes               import genBalanceRandom, getnewtoken
from rest_framework         import serializers
from decimal                import Decimal
import uuid


class PessoaSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField('get_token')
    saldo = serializers.SerializerMethodField('get_balance')

    class Meta:
        model             = Pessoa
        read_only_fields  = ['saldo', 'token']
       

        fields  = (
            'id',
            'nome', 
            'sobrenome', 
            'nomecompleto', 
            'email', 
            'telefone', 
            'cpf',
            'saldo',
            'token'
            )

    def get_token(self, obj):
       return obj.token.codigo

    def get_balance(self, obj):
        return obj.balance

    def create(self, validated_data):
        lopessoa                = Pessoa()
        lopessoa.nome           = validated_data.get('nome')
        lopessoa.sobrenome      = validated_data.get('sobrenome')
        lopessoa.nomecompleto   = validated_data.get('nomecompleto')
        lopessoa.telefone       = validated_data.get('telefone')
        lopessoa.email          = validated_data.get('email') # poderia tratar email  
        lopessoa.cpf            = validated_data.get('cpf') # poderia tratar cpf                   
        lopessoa.save()         
        lopessoa.setInicialBalance(value=genBalanceRandom()) # Adiciona Saldo inicial
        lopessoa.setInicialToken(token=getnewtoken())        # Adiciona Token para transações

        return lopessoa


class HistorySerializer(serializers.ModelSerializer):
    remetente_cpf   = serializers.SerializerMethodField('get_remetenteCpf')
    remetente_nome  = serializers.SerializerMethodField('get_remetenteNome')  
    destino_nome    = serializers.SerializerMethodField('get_destinoNome')
    destino_cpf     = serializers.SerializerMethodField('get_destinoCpf')

    class Meta:
        model   = History
        read_only_fields    = [
            'auth_token', 
            'created_at',
            'remetente_nome',
            'remetente_cpf',
            'destino_nome',
            'destino_cpf'
        ]        

        fields  = (
            'id',
            'remetente', 
            'remetente_nome',
            'remetente_cpf',
            'token_destino',        
            'destino_nome',
            'destino_cpf',
            'valor',
            'created_at',
            'status',
            'auth_token'
        )

    def get_remetenteCpf(self, obj):
       return obj.remetente.cpf
    def get_remetenteNome(self, obj):
       return obj.remetente.nome
    def get_destinoNome(self, obj):
       return obj.destino.nome
    def get_destinoCpf(self, obj):
       return obj.destino.cpf


    def validate(self, data):
        loValor = data.get('valor')
        loToken = None

        try:
            # Compara se o token informado nao é igual ao proprio token
            loToken = Token.objects.get(codigo=data.get('token_destino'))

            if loToken.pessoa == data.get('remetente'):
                raise serializers.ValidationError({
                    'token_destino' : 'Erro: token destino igual ao token do remetente'
                }) 
                
            # verifica se o destinatario esta cancelado
            elif not loToken.pessoa.ativo:
                raise serializers.ValidationError({
                    'token_destino' : 'Erro: token destino está cancaledo'
                }) 
        
        # nao encontrou nenhuma pessoa para o token informado
        except ObjectDoesNotExist:
            raise serializers.ValidationError({
                'token_destino': 'Erro: Nao foi encontrado o destinatario com este token'
            })
        
        
        if loValor is None:
            loValor = Decimal('0.00000')

        if loValor <= 0:
            raise serializers.ValidationError({
                'valor': 'Erro: valor nulo ou 0'
            })     

        # Valida saldo disponivel para criar a transação
        loSaldo = data.get('remetente').balance
        if loSaldo < data.get('valor'):
            raise serializers.ValidationError({
                'valor': 'Erro: valor excede o limite da sua conta'
            })    

        return data


    def create(self, validated_data):
        loHistory               = History()
        loHistory.remetente     = validated_data.get('remetente')
        
        # poderia tratar o campo se foi email ou token com regex 
        # exemplo de Regex para validar email:  ([^@]+@[^@]+\.[^@]+)
        # porem o campo email deverá ser único na base de dados.
        
        # Pessoa Destino sendo vinculado atraves do token
        loDestinoForToken       = Token.objects.get(codigo=validated_data.get('token_destino'))
        loHistory.destino       = loDestinoForToken.pessoa        

        loHistory.token_destino = validated_data.get('token_destino')
        loHistory.valor         = validated_data.get('valor')
        loHistory.status        = validated_data.get('status')
        loHistory.auth_token    = uuid.uuid4()

        loHistory.save() 

        # Funcao para criar a transação no Balance
        def executeTransfer(Remetente, Destino, Valor, Token):
            loBalance = Balance()
            loBalance.pessoa    = Remetente
            loBalance.destino   = Destino
            loBalance.valor     = Valor
            loBalance.tx_token  = Token
            loBalance.save()
            pass        

        if loHistory.status == 'Finalizado':
            # Primeiro debita o valor do remetente
            executeTransfer(loHistory.remetente, loHistory.remetente, 
                (loHistory.valor * -1), loHistory.auth_token)
            # Segundo credita o valor do destino
            executeTransfer(loHistory.destino, loHistory.destino, 
                            loHistory.valor, loHistory.auth_token)

        return loHistory

