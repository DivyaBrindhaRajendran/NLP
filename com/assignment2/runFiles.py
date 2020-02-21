import os
var = 0
while 1:

    os.system("python perceplearn.py")
    os.system("python percep_classify.py")
    f = open("output.txt", "r")
    lines = f.readline()
    avg = int(lines[0])
    print(avg)
    if avg > 80:
        break

