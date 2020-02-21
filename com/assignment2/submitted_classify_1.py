# use this file to classify using perceptron classifier
# Expected: generate percepoutput.txt

import sys
import glob
import os


def contains_digit(word):
    if any(ch.isdigit() for ch in word):
        return 1
    return 0


def is_vowel(c):
    if c in ['a', 'e', 'i', 'o', 'u']:
        return 1
    return 0


def init_dictionary():
    global total_words, weights, bias
    global model
    file = open(model, "r")
    content = file.read().splitlines()
    file.close()
    for line in content:
        if '\t' in line:
            entry = line.split("\t")
            weights[entry[0]] = [float(entry[1]), float(entry[2])]
        else:
            nums = line.split(":")
            bias[0] = float(nums[0])
            bias[1] = float(nums[1])


def add_word(word):
    global sw, words
    if (not word) or (word.lower() in sw) or not word[0].isalnum():
        return
    temp = ""
    found_symbol = False
    if len(word) >= 2:
        for ch in word:
            if ch.isalnum():
                temp += ch
            else:
                add_word(temp)
                temp = ""
                found_symbol = True
    if found_symbol:
        add_word(temp)
        return
    if word.isupper():
        if "all_caps" in words:
            words["all_caps"] += 1
        else:
            words["all_caps"] = 1
    if contains_digit(word):
        word = "number"
    else:
        word = get_root(word)
    if word in words:
        words[word] += 1
    else:
        words[word] = 1


def get_root(word):
    l = len(word)
    if l <= 3:
        return word
    if word.endswith("viting"):
        return word[:-3] + "e"
    if word is "comming":
        return "come"
    if word.endswith("ly"):
        if word.endswith("ily"):
            return word[:-3] + "y"
        return word[:-2]
    if word.endswith("ing") and not word.endswith("ning") and not word.endswith("smoking"):
        if (word.endswith("zing") and not word[-5] == 'z') or word.endswith("ving") or word.endswith(
                "aking") or word.endswith("cing") or word.endswith("summing") or word.endswith("uding"):
            return word[:-3] + "e"
        if (word.endswith("sing") and not word[-5] == 's') or (
                word.endswith("ming") and ("com" in word or "assum" in word)):
            return word[:-3] + "e"
        if word.endswith("tting") or word.endswith("mming") or word.endswith("pping") or word.endswith(
                "dding") or word.endswith("rring") or word.endswith("lling"):
            return word[:-4]
        return word[:-3]
    if word.endswith("ed") and l - 2 > 2:
        if word.endswith("ied"):
            return word[:-3] + "y"
        if word.endswith("pped") or word.endswith("tted") or word.endswith("mmed") or word.endswith(
                "rred") or word.endswith("gged"):
            return word[:-3]
        if word.endswith("ved") or word.endswith("ated") or word.endswith("zed") or word.endswith(
                "ced") or word.endswith("named") or word.endswith("sumed") or word.endswith("ged") or word.endswith(
                "uled"):
            return word[:-1]
        if word.endswith("sed") and not word[-4] is 's':
            return word[:-1]
        if word.endswith("med") and is_vowel(word[-4]):
            return word[:-1]

        return word[:-2]
    if word.endswith("ies"):
        return word[:-3] + "y"
    if word.endswith("s") and not (
            word.endswith("es") or word.endswith("ous") or word.endswith("ss") or word.endswith("ys")):
        return word[:-1]
    return word


def process_file_content(lines):
    words_temp = lines.split(" ")
    for w in words_temp:
        add_word(w)


def classify():
    global p, n, d, t, words, weights, file
    p = n = d = t = False
    a1 = 0.0
    a2 = 0.0
    for w in words:
        if w in weights:
            a1 += weights[w][0]  # * words[w]
            a2 += weights[w][1]  # * words[w]
    a1 += bias[0]
    a2 += bias[1]

    if a1 >= 0:
        p = True
    else:
        n = True
    if a2 >= 0:
        t = True
    else:
        d = True


# -----------------------------------------------------------------------------------------------------------------
words = dict()
model_file = str(sys.argv[1])
output_file = "percepoutput.txt"
input_path = str(sys.argv[2])
model = model_file
weights = dict()
bias = [0, 0]
sw = []
init_dictionary()
all_files = glob.glob(os.path.join(input_path, '*/*/*/*.txt'))
pd = 0
pt = 0
nd = 0
nt = 0
pd_n = 0
pt_n = 0
nd_n = 0
nt_n = 0
f1 = open(output_file, "w+")

for file in all_files:
    p = n = d = t = False
    f = open(file, 'r')
    content = f.read().splitlines()
    f.close()
    lines = content[0]
    words.clear()
    process_file_content(lines)
    classify()
    print(file, p, n, d, t)
    if "N_D" in file:
        nd_n += 1
        if n == True and d == True:
            nd += 1
    elif "N_T" in file:
        nt_n += 1
        if n and t:
            nt += 1
    elif "P_D" in file:
        pd_n += 1
        if p and d:
            pd += 1
    else:
        pt_n += 1
        if p and t:
            pt += 1
    if t:
        f1.write("truthful ")
    else:
        f1.write("deceptive ")
    if p:
        f1.write("positive ")
    else:
        f1.write("negative ")
    f1.write(file + "\n")

f1.close()






