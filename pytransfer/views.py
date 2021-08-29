from .models import History, Pessoa
from .serializers import PessoaSerializer, HistorySerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from django.core.exceptions import ObjectDoesNotExist


class PessoaListCreate(generics.ListCreateAPIView):
    queryset = Pessoa.objects.all()
    serializer_class = PessoaSerializer


class PessoaRetrive(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pessoa.objects.all()
    serializer_class = PessoaSerializer

    # desativa pessoa no banco
    def perform_destroy(self, instance):
        instance.ativo = False
        instance.save()


class HistorysAPIView(generics.ListAPIView):
    serializer_class = HistorySerializer

    def get_queryset(self):
        queryset = History.objects.all()
        parametros = self.request.query_params  # busca a lista de argumentos GET

        # filtra todo historico por pessoa "Remetente"
        if self.kwargs.get('pessoa_pk'):
            queryset = self.queryset.filter(
                remetente_id=self.kwargs.get('pessoa_pk'))

        # filtra entre datas passadas como parametros na url.
        if parametros.get('start', None) is not None and parametros.get('end', None) is not None:
            queryset = queryset.filter(created_at__range=(
                parametros.get('start'), parametros.get('end')))

        # filtra por cpf do destinatario nos registros de transaçoes.
        if parametros.get('cpf'):
            try:
                loDestino = Pessoa.objects.filter(
                    cpf=parametros.get('cpf')).last()
                if loDestino is not None:
                    queryset = queryset.filter(destino_id=loDestino.pk)
            except ObjectDoesNotExist:
                pass

        return queryset


class HistoryListAndCreate(APIView):
    def get(self, request):
        history = History.objects.all()
        serializer = HistorySerializer(history, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = HistorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HistoryListCreate(generics.ListCreateAPIView):
    queryset = History.objects.all()
    serializer_class = HistorySerializer
