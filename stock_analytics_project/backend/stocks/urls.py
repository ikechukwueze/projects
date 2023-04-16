from django.urls import path
from . import views

urlpatterns = [
    path('stocks/', views.ListStocks.as_view()),
    path('exchanges/', views.ListExchanges.as_view()),
    path('portfolio/historical-data/<symbol>/<mic>/', views.HistoricalData.as_view()),
    path('portfolio/add/', views.AddStocktoPorfolioView.as_view())
]
