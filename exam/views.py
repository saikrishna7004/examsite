from django.shortcuts import render, HttpResponse, redirect
import json, time, calendar
from .models import ExamStatus, Question, UserData, ExamData, PaperModel
from django.db import transaction
from django.utils.timezone import localdate

# Create your views here.

@transaction.atomic
def index(request):
	if request.user.is_anonymous:
		return redirect("login")
	allexams = []
	examlist = ExamData.objects.filter(date=localdate(), status=True).order_by("exam_id")
	for exam in examlist:
		status = ExamStatus.objects.filter(user_id=request.user.username, exam_id=exam.exam_id)
		st = "ns"
		if status.exists():
			st = status[0].status
			print("Status ", status[0].status)
		print(st)
		allexams.append({
			'title': exam.title, 'stime': exam.start_time, 'etime': exam.end_time, 
			'ttime': exam.total_time, 'examid': int(exam.exam_id), 'type': exam.type,
			'day': exam.date.day, 'month': calendar.month_name[exam.date.month], 'year': exam.date.year,
			'status': str(st)
		})
	
	content = {
		'allexams': allexams,
		'active': 'exam'
	}
	return render(request, 'exam.html', content)

@transaction.atomic
def examInstructions(request):
	if request.user.is_anonymous:
		return redirect("login")
	if request.method == "POST":
		scheduleVal = request.POST.get("scheduleVal")
		if not ExamStatus.objects.filter(user_id=request.user.username, exam_id=scheduleVal).exists():
			e = ExamStatus.objects.create(user_id=request.user.username, exam_id=scheduleVal, status='started', time_left="180")
			print(e)
		else:
			if ExamStatus.objects.filter(user_id=request.user.username, exam_id=scheduleVal)[0].status=="completed":
				return HttpResponse(content="Exam Completed") 	
		ourExam = request.POST.get("ourExam")
		test = Question
		qlist = test.objects.filter(exam_id=scheduleVal).order_by("question_id")  # [0].question_id
		queslist = []
		for ques in qlist:
			choi = ques.choice_set.all().order_by("choice_id")
			y=5
			current_ans_status = "na"
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
		
		paperList = PaperModel.objects.filter(type=json.loads(ourExam)["type"])[0].subject_set.order_by("start")
		subList=[]
		i=0
		for tempSub in paperList:
			if tempSub.length!=0:
				subList.append({
					"name":tempSub.name, "length":tempSub.length, "start": tempSub.start, "end": tempSub.end, "iter": i
				})
				i+=1
		# return HttpResponse(scheduleVal)
		count = 0
		for x in subList:
			if x["length"]!=0:
				count+=1
		content = {
			'queslist': queslist,
			'exam_id': scheduleVal,
			'ourExam': json.loads(ourExam),
			'subList': subList,
			'count': count,
			'countrange': range(i),
			'countrange1': range(i)
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
def results(request):
	if request.user.is_anonymous:
		return redirect("login")
	allexams = []
	examlist = ExamData.objects.all()
	for exam in examlist:
		allexams.append({
			'title': exam.title, 'examid': int(exam.exam_id), 
			'day': exam.date.day, 'month': calendar.month_name[exam.date.month], 'year': exam.date.year
		})
	content = {
		'allexams': allexams,
		'active': 'results'
	}
	return render(request, "results.html", content)

@transaction.atomic
def resultView(request, exam_id):
	if request.user.is_anonymous:
		return redirect("login")
	user_id = request.user.username
	exam_list = UserData.objects.filter(user_id=user_id)[0].questionanswer_set.filter(exam_id=exam_id).all()
	total = Question.objects.filter(exam_id=exam_id).count()
	unatt = 0
	correct = wrong = 0
	for x in range(0, len(exam_list)):
		qid = exam_list[x].question_id
		aid = exam_list[x].answer_id
		correct_id = Question.objects.filter(question_id=qid)[0].answer_id
		print(aid, correct_id)
		if int(aid) == int(correct_id):
			correct += 1
		else:
			wrong += 1
	unatt = total - wrong - correct
	print(correct, wrong, total, unatt)
	context = {
		"wrong": wrong, "correct": correct, "unatt": unatt, "total": total, "exam_id": exam_id
	}
	return render(request, "resultview.html", context=context)

@transaction.atomic
def resultdetails(request, exam_id):
	qlist = Question.objects.filter(exam_id=exam_id).order_by("question_id")  # [0].question_id
	queslist = []
	i = 0
	for ques in qlist:
		choi = ques.choice_set.all().order_by("choice_id")
		y=5
		current_ans_status = "na"
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
		i = i + 1
		queslist.append(
			{'question_id': ques.question_id, 'question_text': ques.question_text.replace("\\\\", "\\"),
				'op1': choi[0].choice_text.replace("\\\\", "\\"), 'op2': choi[1].choice_text.replace("\\\\", "\\"),
				'op3': choi[2].choice_text.replace("\\\\", "\\"), 'op4': choi[3].choice_text.replace("\\\\", "\\"),
				'op1_id': choi[0].choice_id, 'op2_id': choi[1].choice_id,
				'op3_id': choi[2].choice_id, 'op4_id': choi[3].choice_id,
				'op1_choi': op_choi[0], 'op2_choi': op_choi[1],
				'op3_choi': op_choi[2], 'op4_choi': op_choi[3],
				'ans_status': current_ans_status, 'i': i, "answer": ques.answer_id%4 if ques.answer_id%4!=0 else 4
			}
		)
	
	subList=[]
	i=0
	# return HttpResponse(scheduleVal)
	count = 0
	for x in subList:
		if x["length"]!=0:
			count+=1
	content = {
		'queslist': queslist,
		'exam_id': exam_id,
		'subList': subList
	}
	return render(request, 'resultdetails.html', content)

def generateResults(request):
	pass

def upload(request):
	if not request.user.is_staff:
		return HttpResponse("<meta name='viewport' content='width=device-width, initial-scale=1.0'><h2>You are not permitted to access this page. Login as a Staff or Super User to access this page.</h2><br><a href='/login'>Click Here</a> to redirect to the Login page.")
	if request.method=="POST":
			print(request.FILES)
			start = time.time()
			question_paper = request.FILES['qpaperFile'].read().decode('UTF-8')
			question_set = question_paper.split("\r\n__________\r\n")
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
	return render(request, "upload.html")

def submit(request):
	if request.method == "POST":
		exam_id = request.POST.get("exam_id")
		ex = ExamStatus.objects.filter(user_id=request.user.username, exam_id=exam_id)[0]
		ex.status = "completed"
		ex.save()
		print(ex)
		return HttpResponse(status=200)
	return HttpResponse(status=400)

def create(request):
	if not request.user.is_staff:
		return HttpResponse("<meta name='viewport' content='width=device-width, initial-scale=1.0'><h2>You are not permitted to access this page. Login as a Staff or SuperUser to access this page.</h2><br><a href='/login'>Click Here</a> to redirect to Login page.")
	return render(request, "create.html")

def matheditor(request):
	if request.user.is_staff:
		return render(request, "maths.html")
	else:
		return HttpResponse("<meta name='viewport' content='width=device-width, initial-scale=1.0'><h2>You are not permitted to access this page. Login as a Staff or SuperUser to access this page.</h2><br><a href='/login'>Click Here</a> to redirect to Login page.")

def test(request):
	return render(request, "test.html")