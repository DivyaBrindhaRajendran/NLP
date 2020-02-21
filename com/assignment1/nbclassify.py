import glob
import os
import math

def contains_digit(word):
    global words_dict
    if any(ch.isdigit() for ch in word):
        return 1


def init_word(word):
    global words_dict
    if word not in words_dict:
        words_dict[word] = [0, 0, 0, 0]


def init_extras():
    init_word("-1d")
    init_word("-2m")
    init_word("-4t")
    init_word("-5n")
    init_word("-6ac")


def get_word_count(t):
    global pw, nw, rw, fw
    if t == 0:
        return pw + 1
    if t == 1:
        return nw + 1
    if t == 2:
        return rw + 1
    return fw + 1


def process_word(word, t):
    global words_dict
    if not word:
        return 0
    found_symbol = False
    tw = get_word_count(t)
    p = 0.0
    if len(word) == 1 and not word[0].isalnum():
        return 0
    temp = ""
    if len(word) >= 2:
        for ch in word:
            if ch.isalnum():
                temp += ch
            else:
                p += process_word(temp, t)
                temp = ""
                #p += process_word("symbol", t)
                found_symbol = True
    if found_symbol:
        process_word(temp,t)
        return p
    if is_caps(word):
        p += math.log10((words_dict["-6ac"][t] + 1) / tw)

    if contains_digit(word):
        p += math.log10((words_dict["-5n"][t] + 1) / tw)
        if is_date(word):
            p += math.log10((words_dict["-1d"][t] + 1) / tw)
        if is_money(word):
            p += math.log10((words_dict["-2m"][t] + 1) / tw)
    else:
        word = word.lower()
        if word in words_dict:
             p += math.log10((words_dict[word][t] + 1) / tw)

    return p


def populate_dict(lines):
    global words_dict
    words = lines.split(" ")
    for w in words:
        process_word(w)

def get_p_class(words):
    global total_words
    classes = [0, 0, 0, 0]
    for t in range(4):
        tw = get_word_count(t)
        prior = math.log10((tw + 1) / total_words )
        p = 1.0
        for w in words:
            p += process_word(w, t)
        classes[t] = p
    return classes


def init_dictionary():
    global total_words
    global words_dict, pw, nw, rw, fw, v, intermediateFile
    f = open(intermediateFile, "r")
    content = f.read().splitlines()
    f.close()
    for line in content:
        if line and "\t" in line:
            entry = line.split("\t")
            words_dict[entry[0]] = [int(entry[1]), int(entry[2]), int(entry[3]), int(entry[4])]
        else:
            nums = line.split(":")
            pw = int(nums[0])
            nw = int(nums[1])
            rw = int(nums[2])
            fw = int(nums[3])
            total_words = int(nums[4])
    init_extras()
    v = len(words_dict) - 5


def is_date(word):
    if "th" in word.lower():
        return 1
    return 0


def is_money(word):
    if "$" in word:
        return 1
    return 0


def is_time(word):
    if "am" in word.lower() or "pm" in word.lower():
        return 1
    return 0


def is_number(word):
    if not word.isalpha():
        return 1
    return 0


def is_caps(word):
    if word.isupper():
        return 1
    return 0


def add_to_output(classes, file):
    global output
    l = ""
    if classes[2] > classes[3]:
        l += "truthful "
    else:
        l += "deceptive "

    if classes[0] > classes[1]:
        l += "positive "
    else:
        l += "negative "
    l += file
    output.append(l)


# ------------------------------------------- CODE BEGINS -------------------------------------------------------------
intermediateFile = "nbmodel.txt"
output_file = "nboutput.txt"
classes = [0, 0, 0, 0]
common_words = []
words_dict = {}
total_words = 0
v = 0
pw = 0
nw = 0
fw = 0
rw = 0
init_dictionary()
output = []
all_files = glob.glob(os.path.join("test", '*/*/*/*.txt'))
for file in all_files:
    f = open(file, "r")
    content = f.read().splitlines()
    f.close()
    lines = content[0]
    classes = get_p_class(lines.split(" "))
    add_to_output(classes, file)

f = open("nboutput.txt", "w+")
for line in output:
    f.write(line)
    f.write("\n")
f.close()

f = open("nboutput.txt","r")

pd = 0
pt = 0
nd = 0
nt = 0
pd_n =0
pt_n =0
nd_n = 0
nt_n =0
for line in f.readlines():
     if "fold1" in line:
         if "deceptive positive" in line:
                pd+=1
         pd_n+=1
     elif "fold2" in line:
         if "truthful positive" in line:
             pt+=1
         pt_n+=1
     elif "fold3" in line:
        if "truthful negative" in line:
            nt+=1
        nt_n+=1
     else:
         if "deceptive negative" in line:
             nd+=1
         nd_n+=1
f.close()

print("PD",pd, pd_n )

print("PT",pt, pt_n )

print("ND",nd, nd_n )

print("NT",nt, nt_n )
