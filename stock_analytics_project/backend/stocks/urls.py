from django.urls import path
from . import views

urlpatterns = [
    path('stocks/', views.ListStocks.as_view()),
    path('exchanges/', views.ListExchanges.as_view()),
    path('historical-data/', views.HistoricalData.as_view()),
    path('portfolio/', views.ListPortfolio.as_view()),
    path('portfolio/add/', views.AddStocktoPorfolioView.as_view())
]
