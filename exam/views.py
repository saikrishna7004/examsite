from django.shortcuts import render, HttpResponse
import json
from .models import Question

# Create your views here.

def index(request):
    allexams = [
        {'title':'30-05-2021_Sr.Super-60 &amp; All_Jee-Main_GTM-26', 'stime':'10:15 AM', 'etime':'01:15 PM', 'ttime':'180 Mins', 'examid':5054},
        {'title':'30-05-2021_Sr.Super-60 &amp; All_Jee-Adv_GTA-6', 'stime':'9:00 AM', 'etime':'12:00 PM', 'ttime':'180 Mins', 'examid':5055}
    ]
    content = {
        'allexams' : allexams
    }
    return render(request, 'exam.html', content)

def examInstructions(request):
    if request.method == "POST":
        # return HttpResponse(json.dumps(dict), content_type="application/json")
        print(request.POST)
        scheduleVal = request.POST.get("scheduleVal")
        test = Question
        qlist = test.objects.filter(exam_id=scheduleVal) # [0].question_id
        queslist = []
        for ques in qlist:
            choi = ques.choice_set.all()
            # print(choi[1].choice_text)
            queslist.append(
                {'question_id':ques.question_id, 'question_text':ques.question_text, 
                'op1':choi[0].choice_text, 'op2':choi[1].choice_text, 
                'op3':choi[2].choice_text, 'op4':choi[3].choice_text,
                'op1_id':choi[0].choice_id, 'op2_id':choi[1].choice_id, 
                'op3_id':choi[2].choice_id, 'op4_id':choi[3].choice_id, 
                }
            )
        # return HttpResponse(scheduleVal)
        content = {
            'queslist':queslist,
            'exam_id':scheduleVal,
        }
        return render(request, 'exampage.html', content)

    return render(request, 'defaultexam.html')

def answer(request):
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        exam_id = request.POST.get("exam_id")
        question_id = request.POST.get("question_id")
        answer_id = request.POST.get("answer_id")
        print(user_id, exam_id, question_id, answer_id)
        return HttpResponse(status=200)

    return HttpResponse("This is answer page, later this will be modified")