from django.shortcuts import render, HttpResponse, redirect
import json, time
from .models import Question, UserData
from django.db import transaction

# Create your views here.

def index(request):
	if request.user.is_anonymous:
		return redirect("login")
	allexams = [
		{'title': '30-05-2021_Sr.Super-60 &amp; All_Jee-Main_GTM-26',
			'stime': '10:15 AM', 'etime': '01:15 PM', 'ttime': '180 Mins', 'examid': 5054},
		{'title': '30-05-2021_Sr.Super-60 &amp; All_Jee-Adv_GTA-6',
			'stime': '9:00 AM', 'etime': '12:00 PM', 'ttime': '180 Mins', 'examid': 5055},
		{'title': '30-05-2021_Sr.Super-60 &amp; All_Jee-Main_GTM-1',
			'stime': '10:15 AM', 'etime': '01:15 PM', 'ttime': '180 Mins', 'examid': 5056},
	]
	content = {
		'allexams': allexams
	}
	return render(request, 'exam.html', content)

@transaction.atomic
def examInstructions(request):
	if request.user.is_anonymous:
		return redirect("login")
	if request.method == "POST":
		scheduleVal = request.POST.get("scheduleVal")
		ourExam = request.POST.get("ourExam")
		test = Question
		qlist = test.objects.filter(exam_id=scheduleVal).order_by("question_id")  # [0].question_id
		queslist = []
		for ques in qlist:
			choi = ques.choice_set.all().order_by("choice_id")
			y=5
			current_ans_status = ""
			if UserData.objects.filter(user_id=request.user.username)[0].questionanswer_set.filter(question_id=ques.question_id).exists():
				current_ans = UserData.objects.filter(user_id=request.user.username)[0].questionanswer_set.filter(
					question_id=ques.question_id)[0].answer_id
				current_ans_status = UserData.objects.filter(user_id=request.user.username)[0].questionanswer_set.filter(
					question_id=ques.question_id)[0].ans_status
				for x in range(4):
					if current_ans == choi[x].choice_id:
						y = x
			op_choi = ["", "", "", ""]
			try:
				op_choi[y] = "checked"
			except:
				pass
			
			queslist.append(
				{'question_id': ques.question_id, 'question_text': ques.question_text,
				 'op1': choi[0].choice_text, 'op2': choi[1].choice_text,
				 'op3': choi[2].choice_text, 'op4': choi[3].choice_text,
				 'op1_id': choi[0].choice_id, 'op2_id': choi[1].choice_id,
				 'op3_id': choi[2].choice_id, 'op4_id': choi[3].choice_id,
				 'op1_choi': op_choi[0], 'op2_choi': op_choi[1],
				 'op3_choi': op_choi[2], 'op4_choi': op_choi[3],
				 'ans_status': current_ans_status,
				 }
			)
		subList = [{"name":"Maths","length":"7","start":"1","end":"7"},{"name":"Physics","length":"7","start":"8","end":"14"},{"name":"Chemistry","length":"7","start":"15","end":"21"}]
		# return HttpResponse(scheduleVal)
		content = {
			'queslist': queslist,
			'exam_id': scheduleVal,
			'ourExam': json.loads(ourExam),
			'subList': subList
		}
		return render(request, 'exampage.html', content)

	return render(request, 'defaultexam.html')

@transaction.atomic
def answer(request):
	if request.user.is_anonymous:
		return redirect("login")
	if request.method == "POST":
		user_id = request.user.username
		exam_id = request.POST.get("exam_id")
		question_id = request.POST.get("question_id")
		answer_id = request.POST.get("answer_id")
		ans_status = request.POST.get("ans_status")
		print(user_id, exam_id, question_id, answer_id, ans_status)

		if answer_id == None:
			return HttpResponse(status=400)

		if not UserData.objects.filter(user_id=user_id)[0].questionanswer_set.filter(question_id=question_id).exists():
			UserData.objects.filter(user_id=user_id)[0].questionanswer_set.create(
				question_id=question_id, exam_id=exam_id, answer_id=answer_id, ans_status=ans_status)
		else:
			question_details = UserData.objects.filter(
				user_id=user_id)[0].questionanswer_set.filter(question_id=question_id)
			for x in range(0, len(question_details)):
				question_details[0].delete()
			UserData.objects.filter(user_id=user_id)[0].questionanswer_set.create(
				question_id=question_id, exam_id=exam_id, answer_id=answer_id, ans_status=ans_status)
			# update(question_id=question_id,exam_id=exam_id,answer_id=answer_id)
		return HttpResponse(status=200)

	return HttpResponse("This is answer page, later this will be modified")

@transaction.atomic
def delete(request):
	if request.user.is_anonymous:
		return redirect("login")
	if request.method == "POST":
		user_id = request.user.username
		exam_id = request.POST.get("exam_id")
		question_id = request.POST.get("question_id")

		if UserData.objects.filter(user_id=user_id)[0].questionanswer_set.filter(question_id=question_id).exists():
			UserData.objects.filter(user_id=user_id)[0].questionanswer_set.filter(question_id=question_id).delete()
		
		return HttpResponse(status=200)
	
	return HttpResponse("This is answer page, later this will be modified")

@transaction.atomic
def results(request, exam_id):
	if request.user.is_anonymous:
		return redirect("login")
	user_id = request.user.username
	exam_list = UserData.objects.filter(user_id=user_id)[
		0].questionanswer_set.filter(exam_id=exam_id).all()
	y = 0
	for x in range(0, len(exam_list)):
		qid = exam_list[x].question_id
		aid = exam_list[x].answer_id
		correct_id = Question.objects.filter(question_id=qid)[0].answer_id
		if int(aid) == int(correct_id):
			y += 1
		x += 1
	#print("The no. of correct options is: ", y)
	return HttpResponse("<meta name='viewport' content='width=device-width, initial-scale=1.0'><h1>The no. of correct answers is: "+str(y)+"</h1>")

def create(request):
	if not request.user.is_staff:
		return HttpResponse("<meta name='viewport' content='width=device-width, initial-scale=1.0'><h2>You are not permitted to access this page. Login as a Staff or SuperUser to access this page.</h2><br><a href='/login'>Click Here</a> to redirect to Login page.")
	if request.method=="POST":
			print(request.FILES)
			start=time.time()
			question_paper = request.FILES['qpaperFile'].read().decode('UTF-8')
			question_set = question_paper.split("\n__________\n")
			exam_id = request.POST.get("examId")
			choice_id_inc = str(exam_id)+'000'
			choice_id_inc = int(choice_id_inc)
			question_id_inc = str(exam_id)+'000'
			question_id_inc = int(question_id_inc)
			with transaction.atomic():
				if Question.objects.filter(exam_id=exam_id).exists():
					return HttpResponse(f"<meta name='viewport' content='width=device-width, initial-scale=1.0'>The given Exam ID {exam_id} already exists. Please choose other ID.")
				for x in range(0,len(question_set)):
					question_id_inc += 1
					queset = question_set[x].split("\n")
					Question.objects.create(exam_id=exam_id, question_id=question_id_inc, question_text=queset[0],answer_id=int(str(exam_id)+'000')+x*4+int(queset[5]))
					for y in range(1,5):
						choice_id_inc += 1
						Question.objects.filter(question_id=question_id_inc)[0].choice_set.create(choice_text=queset[y],choice_id=choice_id_inc)
			end=time.time()
			return HttpResponse(f"<meta name='viewport' content='width=device-width, initial-scale=1.0'><h1>Done 👍 in {end-start} seconds.</h1>The Exam ID is {exam_id}")
	return render(request, "create.html")

def matheditor(request):
	if request.user.is_staff:
		return render(request, "maths.html")
	else:
		return HttpResponse("<meta name='viewport' content='width=device-width, initial-scale=1.0'><h2>You are not permitted to access this page. Login as a Staff or SuperUser to access this page.</h2><br><a href='/login'>Click Here</a> to redirect to Login page.")