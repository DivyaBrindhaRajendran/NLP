import glob
import os
import random


def init_stop_words():
    global sw
    sw = ["schicago","the", "was", "in", "hotel","hotels", "of", "for", "it", "with","on","stay", "that",
     "day", "is", "that", "had", "on", "from", "have", "all", "as", "there", "are", "they", "so",
     "would", "stayed", "just", "also", "which", "place", "again", "this", "chicago",
     "w", "to", "be", "if", "your", "their", "hotels","room","northwestern", "rooms", "michigan","illinois",
     "fairmont", "hyatt", "james","we","at", "museums","one", "symbol","an", "by", "and", "a","two","his","any", "ve", "have", "hilton", "fitzpatrick"]
    sw = []


def contains_digit(word):
    if any(ch.isdigit() for ch in word):
        return 1
    return 0


def is_vowel(c):
    if c in ['a', 'e', 'i', 'o', 'u']:
        return 1
    return 0


def activation():
    global words, weights, bias
    act1 = act2 = act3 = act4 = 0.0
    for w in words:
        # Vanilla Perceptron
        act1 = weights[w][0] #*words[w]
        act2 = weights[w][1] #*words[w]
        # Average Perceptron
        act3 = weights[w][2] #*words[w]
        act4 = weights[w][3] #*words[w]

    act1 += bias[0]
    act2 += bias[1]
    act3 += bias[2]
    act4 += bias[3]

    return [act1, act2, act3, act4]


def learn():
    global words, weights, isVanilla, p, n, t, d, bias
    act = activation()
    y1 = 1 if p else 0
    y2 = 1 if t else 0
    a1 = y1*act[0]
    a2 = y2*act[1]
    a3 = y1*act[2]
    a4 = y2*act[3]

    if a1 <= 0 or a2 <= 0 or a3 <= 0 or a4 <= 0:
        for w in words:
            if a1 <= 0:
                weights[w][0] += y1 #* words[w]
            if a2 <= 0:
                weights[w][1] += y2 #* words[w]
            if a3 <= 0:
                ow = weights[w][2]
                weights[w][2] = round((2 * ow + y1) / 2)
            if a4 <= 0:
                ow = weights[w][3]
                weights[w][3] = round((2 * ow + y2) / 2)

        if a1 <= 0: bias[0] += y1
        if a2 <= 0: bias[1] += y2
        if a3 <= 0: bias[2] += y1
        if a4 <= 0: bias[3] += y2


def add_word(word, isInitial):
    global sw, all_words, words
    if (not word) or (word.lower() in sw) or not word[0].isalnum():
        return
    temp = ""
    found_symbol = False
    if len(word) >= 2:
        for ch in word:
            if ch.isalnum():
                temp += ch
            else:
                add_word(temp, isInitial)
                temp = ""
                found_symbol = True
    if found_symbol:
        add_word(temp, isInitial)
        return
    if word.isupper():
        if isInitial:
            all_words.add("all_caps")
        else:
            if "all_caps" in words:
                words["all_caps"] += 1
            else:
                words["all_caps"] = 1
    if contains_digit(word):
        word = "number"
    else:
        word = word.lower()
        word = get_root(word)
    if isInitial:
        all_words.add(word)
    else:
        if word in words:
            words[word] += 1
        else:
            words[word] = 1


def get_root(word):
    l = len(word)
    if l <= 3:
        return word
    if word.endswith("viting"):
        return word[:-3]+"e"
    if word is "comming":
        return "come"
    if word.endswith("ing") and not word.endswith("ning") and not word.endswith("smoking"):
        if (word.endswith("zing") and not word[-5] == 'z') or word.endswith("ving") or word.endswith("aking") or word.endswith("cing") or word.endswith("summing") or word.endswith("uding"):
            return word[:-3]+"e"
        if (word.endswith("sing") and not word[-5]=='s') or (word.endswith("ming") and ("com" in word or "assum" in word)):
            return word[:-3] + "e"
        if word.endswith("tting") or word.endswith("mming") or word.endswith("pping") or word.endswith("dding") or word.endswith("rring"):
            return word[:-4]
        return word[:-3]
    if word.endswith("ed") and l-2>2:
        if word.endswith("ied"):
            return word[:-3]+"y"
        if word.endswith("pped") or word.endswith("tted") or word.endswith("mmed") or word.endswith("rred") or word.endswith("gged"):
            return word[:-3]
        if word.endswith("ved") or word.endswith("uired") or ( word.endswith("ired") and "pair" not in word) or word.endswith("ated") or word.endswith("zed") or word.endswith("ced") or word.endswith("named") or word.endswith("sumed") or word.endswith("ged") or word.endswith("uled"):
            return word[:-1]
        if word.endswith("sed") and not word[-4] is 's':
            return word[:-1]
        if word.endswith("med") and is_vowel(word[-4]):
            return word[:-1]

        return word[:-2]
    if word.endswith("ies"):
        return word[:-3]+"y"
    if word.endswith("s") and not (word.endswith("es") or word.endswith("ous") or word.endswith("ss") or word.endswith("ys")):
        return word[:-1]
    return word


def process_file_content(lines, type):
    global words
    words_temp = lines.split(" ")
    for w in words_temp:
        add_word(w,type)


def update_class(fname):
    global p, n, d, t
    if "negative_" in fname: n = True
    else: p = True
    if "deceptive_" in fname: d = True
    else: t = True


def init_dictionary():
    global all_words
    global weights
    # 1,2 - Vanilla P&T 3,4 - Average P&T
    for w in all_words:
        weights[w] = [0, 0, 0, 0]


def write_to_file():
    global aFile, vFile, bias
    f1 = open(vFile, "w+")
    f2 = open(aFile, "w+")
    for w in weights:
        f1.write(w)
        f1.write("\t")
        f1.write(str(weights[w][0]))
        f1.write("\t")
        f1.write(str(weights[w][1]))
        f2.write(w)
        f2.write("\t")
        f2.write(str(weights[w][2]))
        f2.write("\t")
        f2.write(str(weights[w][3]))
        f1.write("\n")
        f2.write("\n")

    f1.write(str(bias[0]) + ":" + str(bias[1]))
    f2.write(str(bias[2]) + ":" + str(bias[3]))
    f1.close()
    f2.close()

# ---------------- EXEC CODE -----------------------
vFile = "vanillamodel.txt"
aFile = "averagedmodel.txt "
sw = []
weights = dict()
n = 0
bias = [0, 0, 0, 0]
all_words = set()
words = dict()
total_words = 0
p = n = d = t = False
init_stop_words()
all_files = glob.glob(os.path.join("op_spam_training_data", '*/*/*/*.txt'))
isVanilla = False
all_lines = []
for file in all_files:
    p = n = d = t = False
    f = open(file, "r")
    content = f.read().splitlines()
    f.close()
    lines = content[0]
    update_class(file)
    all_lines.append([lines,p,n,t,d])
    process_file_content(lines,1)

n = len(all_words)
print(len(all_lines))
init_dictionary()

for i in range(50):
    random.shuffle(all_lines)
    for line in all_lines:
        p = n = d = t = False
        words.clear()
        process_file_content(line[0], 0)
        p = line[1]
        n = line[2]
        t = line[3]
        d = line[4]
        learn()

print(weights)
print(bias)
write_to_file()
