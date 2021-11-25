from django.http.response import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.views.generic.base import View
from .models import Question
import json
import requests
import easyocr

# Create your views here.
class QuestionView(View):
    def get(self, request):
        database = Question.objects.all()
        return render(request, 'base.html', {'database': database})

    def post(self, request):
        question = request.POST.get('question')
        image = request.FILES.get('image')
        image_text = ""

        if image:
            image_path = 'media/QuestionsImages/image.png'
            with open(image_path, 'wb+') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)
            reader = easyocr.Reader(['en'])
            output = reader.readtext(image_path)
            for tup in output:
                image_text = image_text + tup[1] + "\n"
            image_text = image_text.strip().replace('\n', ' ')

        question_payload = "{\r\n\"text\": \"" + question + "\",\r\n\"language\": \"en\"\r\n}"

        headers = {
            'content-type': "application/json",
            'x-rapidapi-host': "plagiarism-checker-and-auto-citation-generator-multi-lingual.p.rapidapi.com",
            'x-rapidapi-key': "26f853d7c4msh8521953f9e675bcp1288fcjsn563cd48678ab"
        }

        question_response = requests.request("POST", "https://plagiarism-checker-and-auto-citation-generator-multi-lingual.p.rapidapi.com/plagiarism", data=question_payload, headers=headers)

        question_result = json.loads(question_response.text)

        if image_text:
            image_payload = "{\r\n\"text\": \"" + image_text + "\",\r\n\"language\": \"en\"\r\n}"

            image_response = requests.request("POST", "https://plagiarism-checker-and-auto-citation-generator-multi-lingual.p.rapidapi.com/plagiarism", data=image_payload, headers=headers)

            image_result = json.loads(image_response.text)

            if question_result.get('percentPlagiarism') == 0 and image_result.get('percentPlagiarism') == 0:
                newQuestion = Question(question=question, image=image)
                newQuestion.save()
            
            database = Question.objects.all()
            return render(request, 'base.html', {'question_result' : question_result, 'image_result': image_result, 'database': database})

        if question_result.get('percentPlagiarism') == 0:
            newQuestion = Question(question=question)
            newQuestion.save()

        database = Question.objects.all()
        return render(request, 'base.html', {'question_result': question_result, 'database': database})


class UpdateQuestion(View):
    def get(self, request, id):
        database = Question.objects.all()
        return render(request, 'base.html', {'database': database})
    
    def post(self, request, id):
        question = request.POST.get('question')
        image = request.FILES.get('image')
        image_text = ""

        if image:
            image_path = 'media/QuestionsImages/image.png'
            with open(image_path, 'wb+') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)
            reader = easyocr.Reader(['en'])
            output = reader.readtext(image_path)
            for tup in output:
                image_text = image_text + tup[1] + "\n"
            image_text = image_text.strip().replace('\n', ' ')

        question_payload = "{\r\n\"text\": \"" + question + "\",\r\n\"language\": \"en\"\r\n}"

        headers = {
            'content-type': "application/json",
            'x-rapidapi-host': "plagiarism-checker-and-auto-citation-generator-multi-lingual.p.rapidapi.com",
            'x-rapidapi-key': "26f853d7c4msh8521953f9e675bcp1288fcjsn563cd48678ab"
        }

        question_response = requests.request("POST", "https://plagiarism-checker-and-auto-citation-generator-multi-lingual.p.rapidapi.com/plagiarism", data=question_payload, headers=headers)

        question_result = json.loads(question_response.text)

        if image_text:
            image_payload = "{\r\n\"text\": \"" + image_text + "\",\r\n\"language\": \"en\"\r\n}"

            image_response = requests.request("POST", "https://plagiarism-checker-and-auto-citation-generator-multi-lingual.p.rapidapi.com/plagiarism", data=image_payload, headers=headers)

            image_result = json.loads(image_response.text)

            if question_result.get('percentPlagiarism') == 0 and image_result.get('percentPlagiarism') == 0:
                updateQuestion = Question.objects.get(pk=id)
                updateQuestion.question = question
                updateQuestion.image = image
                updateQuestion.save()
            
            database = Question.objects.all()
            return render(request, 'base.html', {'question_result' : question_result, 'image_result': image_result, 'database': database})

        if question_result.get('percentPlagiarism') == 0:
            updateQuestion = Question.objects.get(pk=id)
            updateQuestion.question = question
            updateQuestion.image = ""
            updateQuestion.save()

        database = Question.objects.all()
        return render(request, 'base.html', {'question_result': question_result, 'database': database})


class DeleteQuestion(View):
    def get(self, request, id):
        question = Question.objects.get(pk=id)
        question.delete()
        return HttpResponseRedirect('/')


class CheckDuplicate(View):
    def get(self, request, ques):
        try:
            question = Question.objects.get(question=f"{ques}?")
            return JsonResponse({"message" : f"{question.question}"})
        except:
            return JsonResponse({"message" : "None"})
            
    