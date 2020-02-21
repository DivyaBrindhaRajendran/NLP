import sys
import glob
import os
import collections


def increment_word(word, t):
    global words_dict
    x = words_dict[word][t]
    x += 1
    words_dict[word][t] = x


def contains_digit(word):
    global words_dict
    if any(ch.isdigit() for ch in word):
        return 1


def init_word(word):
    global words_dict
    if word not in words_dict:
        words_dict[word] = [0, 0, 0, 0]


def add_date(i):
    increment_word("-1d",i)


def add_money(i):
    increment_word("-2m", i)


def add_temperature(i):
    increment_word("-3temp", i)


def add_time(i):
    increment_word("-4t", i)


def add_num(i):
    increment_word("-5n", i)


def add_caps(i):
    increment_word("-6ac", i)


def init_extras():
    init_word("-1d")
    init_word("-2m")
    init_word("-3temp")
    init_word("-4t")
    init_word("-5n")
    init_word("-6ac")


def handle_digits(word, ):
    global words_dict
    global classes
    word = word.lower()
    for t in range(4):
        if classes[t]:
            if "am" in word or "pm" in word:
                add_date(t)
            elif "$" in word:
                add_money(t)
            elif "th" in word:
                add_date(t)
            add_num(t)


def handle_symbol(word, symbol):
    global words_dict
    process_word(symbol)
    words = word.split(symbol)
    for w in words:
        if w:
            process_word(w)


def write_content_in_file():
    global total_words
    global fw, nw, rw, pw
    f = open(intermediateFile, "w")
    for x in words_dict:
        f.write(x)
        f.write("\t")
        f.write(str(words_dict[x][0]))
        f.write("\t")
        f.write(str(words_dict[x][1]))
        f.write("\t")
        f.write(str(words_dict[x][2]))
        f.write("\t")
        f.write(str(words_dict[x][3]))
        f.write("\n")
    f.write(str(pw))
    f.write(":")
    f.write(str(nw))
    f.write(":")
    f.write(str(rw))
    f.write(":")
    f.write(str(fw))
    f.write(":")
    f.write(str(total_words))
    f.close()


def process_word(word):
    global classes
    global pw
    global nw
    global fw
    global rw, sw

    if (not word) or (word.lower() in sw):
        return
    global total_words
    global words_dict
    found_symbol = False
    if len(word) >= 2:
        temp = ""
        for ch in word:
            if ch.isalnum():
                temp += ch
            else:
                process_word(temp)
                temp = ""
                process_word(""+ch)
                found_symbol = True

    if found_symbol:
        return
    if word.isalnum():
        #print(word)
        if classes[0]:
            pw += 1
        else:
            nw += 1
        if classes[2]:
            rw += 1
        else:
            fw += 1
        total_words += 1
    if word.isupper() and word != "I" and word != "A":
        for t in range(4):
            if classes[t]:
                add_caps(t)

    word = word.lower()

    if contains_digit(word) == 1:
        handle_digits(word)
    else:
        init_word(word)
        for t in range(4):
            if classes[t]:
                words_dict[word][t] += 1
    return


def populate_dict(lines):
    global words_dict
    words = lines.split(" ")
    for w in words:
        process_word(w)


def init_dictionary():
    global total_words
    global words_dict, pw, nw, rw, fw
    f = open(intermediateFile, "r")
    content = f.read().splitlines()
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

    f.close()


def update_classes(file):
    global classes
    # Determine Classes From File
    if "negative_" in file:
        classes[1] = 1
    if "positive_" in file:
        classes[0] = 1
    if "deceptive_" in file:
        classes[3] = 1
    if "truthful_" in file:
        classes[2] = 1


def init_stop_words():
    global sw
    sw = ['.','hotel','hotels','restaurant','stayed',',','i', "s","t",'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]


# ------------------------------------------- CODE BEGINS -------------------------------------------------------------
input_path = str(sys.argv[1])
intermediateFile = "nbmodel.txt"
f = open(intermediateFile, "a")
f.close()
sw = []
classes = [0, 0, 0, 0]
common_words = []
words_dict = {}
total_words = 0
pw = 0
nw = 0
fw = 0
rw = 0
#init_stop_words()
init_dictionary()
init_extras()
all_files = glob.glob(os.path.join(input_path, '*/*/*/*.txt'))
for file in all_files:
    classes = [0, 0, 0, 0]
    update_classes(file)
    #init_dictionary()
    # Read Contents of the file
    f = open(file,"r")
    content = f.read().splitlines()
    f.close()
    lines = content[0]
    populate_dict(lines)

write_content_in_file()