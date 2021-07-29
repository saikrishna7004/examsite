from exam.models import Question

question_paper = open("examtest.txt",'r').read()
question_set = question_paper.split("\n__________\n")
exam_id = 5056
choice_id_inc = str(exam_id)+'000'
choice_id_inc = int(choice_id_inc)
print(choice_id_inc,"\n")
for x in range(0,len(question_set)):
	print(Question.objects.create(exam_id=exam_id))
	for y in range(0,6):
		if y>0 and y<5:	
			choice_id_inc += 1
			print(choice_id_inc)
		print(question_set[x].split("\n")[y])
		
    