from django.shortcuts import render
from django.views.generic.base import View
import requests

# Create your views here.
class QuestionView(View):
    def get(self, request):
        return render(request, 'base.html')

    def post(self, request):
        print(request.POST)
        print(request.FILES)
        # res = requests.get("https://www.googleapis.com/customsearch/v1?key=AIzaSyDFxuU51IEw4lONcAkDkV6BmXRArvi4Vkg&cx=e7b5e8568eb7a493f&q=plagiarism")
        return render(request, 'base.html')
