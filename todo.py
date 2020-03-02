courses = [
	"EDUC-X158", 
	"MATH-M212", 
	"EALC-E111", 
	"CSCI-C200"  
]

with open ("TODO.txt", "r") as todo:
	rawTodo = todo.read().strip()

lines = rawTodo.splitlines()

for c in courses:
	for l in lines:
		if c in l:
			print(c)

for l in lines:
	for i in l:
		# Assignment Detected
		if i == "-":
			print(l.strip())
		# Assignment Part
		elif i == ".":
			print(l.strip())
