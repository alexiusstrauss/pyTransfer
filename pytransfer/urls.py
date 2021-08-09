from django.urls import path
from .views import HistoryListCreate, PessoaListCreate, PessoaRetrive, HistorysAPIView


urlpatterns = [
    path('pessoas/', PessoaListCreate.as_view(), 
            name="pessoas-list-create"),

    path('pessoas/<int:pk>/', PessoaRetrive.as_view(), 
            name="pessoas-reatrive" ),

    path('pessoas/<int:pessoa_pk>/historys/', HistorysAPIView.as_view(), 
            name="pessoa-historys" ),    

    path('historys/', HistoryListCreate.as_view(), 
            name="historys-list" )
    
    ]