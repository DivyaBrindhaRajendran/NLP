f = open("stop_words", "r")
stop = []
for r in f.readlines():
    stop.append(r.split("\n")[0])
f.close()
print(stop)
