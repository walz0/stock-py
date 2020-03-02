courses = [
	"EDUC-X158", 
	"MATH-M212", 
	"EALC-E111", 
	"CSCI-C200"  
]

def containsCourse(str):
	for c in courses:
		if c in str:
			return True
	return False
	

with open ("TODO.txt", "r") as todo:
	rawTodo = todo.read().strip()

lines = rawTodo.splitlines()

assignment = []
sub = []
complete = []

for l in lines:
	if len(l) > 0:
		# Complete Assignment Detected
		if l.strip()[0] == "/":
			complete.append(l.strip())
		# Assignment Detected
		elif l.strip()[0] == "-" and not containsCourse(l):
			assignment.append(l.strip())
		# Assignment Part
		elif l.strip()[0] == ".":
			sub.append(l.strip())

print('Assignments:')
for a in assignment:
	print(a)
print('Sub:')
for s in sub:
	print(s)
print('Completed:')
for c in complete:
	print(c)
