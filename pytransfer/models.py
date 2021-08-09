import uuid
from decimal                    import Decimal
from django.utils.translation   import ugettext_lazy as _
from django.db                  import models
from django.db.models           import Sum, Q


class PessoaManager(models.Manager):

    # retorna apenas as pessoas ativas
    def get_queryset(self):
        return super().get_queryset().filter(ativo=True)
       

class Pessoa(models.Model):
    nome            = models.CharField(max_length=50)
    sobrenome       = models.CharField(max_length=50)
    nomecompleto    = models.CharField(max_length=110)
    email           = models.EmailField()
    telefone        = models.CharField(max_length=20)
    cpf             = models.CharField(max_length=20)
    ativo           = models.BooleanField(default=True)
    created_at      = models.DateTimeField(auto_now_add=True)
    objects         = PessoaManager()   # Manager de Pessoas

    class Meta:
        verbose_name = ('Pessoa')
        verbose_name_plural = ('Pessoas')

    def __str__(self):
        return  '%s | Saldo:  R$ %s' % (self.nomecompleto, self.balance)


    @property
    def token(self):       
        result = Token.objects.get(Pessoa=self)
        return result.codigo

    @property
    def balance(self): 
        result = Decimal('0.00000')      

        # Soma valores bloqueados em transações
        bloqueado = History.objects.filter(remetente=self).filter(
            status__in=['Executando', 'Pendente']
        ).aggregate(Sum('valor'))['valor__sum']

        # Soma os valores no extrato da carteira balance
        carteira = Balance.objects.filter(
            pessoa=self, cancelado=False
        ).aggregate(Sum('valor'))['valor__sum']

        if carteira is None:
            carteira = Decimal('0.00000')
        if bloqueado is None:
            bloqueado = Decimal('0.00000')

        result = carteira - bloqueado
        return result


    def setInicialToken(self, token):
        loToken           = Token()
        loToken.codigo    = token
        loToken.pessoa    = self
        loToken.save()
        return True


    def setInicialBalance(self, value):
        loBalance           = Balance()
        loBalance.valor     = value
        loBalance.pessoa    = self
        loBalance.save()
        return True


class Token(models.Model):
    codigo = models.CharField(max_length=100)
    pessoa = models.OneToOneField("Pessoa", on_delete=models.CASCADE)

    def __str__(self):
        return '%s : %s' % (
            self.pessoa.nome, 
            self.codigo
        )

class Balance(models.Model):
    valor       = models.DecimalField(null=True, max_digits=12, decimal_places=5, default=0)
    pessoa      = models.ForeignKey("Pessoa", on_delete=models.CASCADE)
    tx_token    = models.CharField(max_length=100, blank=True, default='')
    cancelado   = models.BooleanField(default=False)
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s | R$ %s' % (
            self.pessoa.nome, 
            self.valor
        )


class History(models.Model):

    F = 'Finalizado'
    E = 'Executando'
    P = 'Pendente'
    C = 'Cancelado'

    STATUS_CHOICES = (
        (F, 'Finalizado'),
        (E, 'Executando'),
        (P, 'Pendente'),
        (C, 'Cancelado')
    )

    remetente       = models.ForeignKey("Pessoa", on_delete=models.CASCADE)
    destino         = models.ForeignKey("Pessoa", related_name="Pessoa", on_delete=models.CASCADE)
    token_destino   = models.CharField(max_length=100)
    valor           = models.DecimalField(null=True, max_digits=12, decimal_places=5, default=0)
    created_at      = models.DateField(auto_now_add=True)
    update_at       = models.DateTimeField(auto_now=True)
    status          = models.CharField(max_length=10, choices=STATUS_CHOICES, default=P)
    auth_token      = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return '%s  ->  R$ %s  ->  %s -> cpf %s | %s' % (
            self.remetente.nome, 
            self.valor,
            self.destino.nome, 
            self.destino.cpf, 
            self.status
        )    


    def save(self, *args, **kwargs):
        # Gera o token da transacao
        if not self.auth_token:
            self.auth_token = uuid.uuid4()            
        super(History, self).save(*args, **kwargs)




