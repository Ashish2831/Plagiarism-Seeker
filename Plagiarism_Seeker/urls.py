from django.urls import path
from . import views

# Create your urls here.
urlpatterns = [
    path('', views.QuestionView.as_view(), name='QuestionView'),
    path('update/<int:id>/', views.UpdateQuestion.as_view(), name='UpdateQuestion'),
    path('delete/<int:id>/', views.DeleteQuestion.as_view(), name='DeleteQuestion'),
    path('checkduplicate/<str:ques>/', views.CheckDuplicate.as_view(), name='CheckDuplicate'),
]
