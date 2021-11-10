import json
from django.shortcuts import render
from django.views.generic.base import View
from .models import Question
import requests
import easyocr

# Create your views here.
class QuestionView(View):
    def get(self, request):
        return render(request, 'base.html')

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
            
            print(image_payload)
    
            image_response = requests.request("POST", "https://plagiarism-checker-and-auto-citation-generator-multi-lingual.p.rapidapi.com/plagiarism", data=image_payload, headers=headers)
            
            print(image_response.text)

            image_result = json.loads(image_response.text)

            if question_result.get('percentPlagiarism') == 0 and image_result.get('percentPlagiarism') == 0:
                newQuestion = Question(question=question, image=image)
                newQuestion.save()
            return render(request, 'base.html', {'question_result' : question_result, 'image_result': image_result})

        if question_result.get('percentPlagiarism') == 0:
            newQuestion = Question(question=question)
            newQuestion.save()
            
        # question_result = {'sources': [{'url': 'https://techtutorialz.com/ios-only-capabilities/', 'title': 'iOS Only Capabilities in Appium - TechTutorialz', 'matches': [{'inputStart': 0, 'inputEnd': 100, 'matchText': 'These Capabilities are available only on the XCUITest Driver and the deprecated UIAutomation Driver.', 'context': {'after': ' Capability, Description, Valu'}, 'score': 14.083333333333334}]}, {'url': 'https://www.programsbuzz.com/article/appium-ios-capabilities', 'title': 'Appium iOS Capabilities | ProgramsBuzz', 'matches': [{'inputStart': 0, 'inputEnd': 100, 'matchText': 'These Capabilities are available only on the XCUITest Driver and the deprecated UIAutomation Driver.', 'context': {'after': ' calendarFormat: Calendar form'}, 'score': 14.083333333333334}]}, {'url': 'https://kobiton.com/book/chapter-3-understanding-the-desired-capabilities', 'title': 'Chapter-3: Understanding the Desired Capabilities - Kobiton', 'matches': [{'inputStart': 0, 'inputEnd': 100, 'matchText': 'These Capabilities are available only on the XCUITest Driver and the deprecated UIAutomation Driver.', 'context': {}, 'score': 14.083333333333334}]}], 'percentPlagiarism': 100}
        
        return render(request, 'base.html', {'question_result' : question_result})
