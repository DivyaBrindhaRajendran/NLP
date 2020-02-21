# use this file to learn perceptron classifier
# Expected: generate vanillamodel.txt and averagemodel.txt

import sys
import glob
import os
import random
import sys


def init_stop_words():
    global sw
    sw = ['a', 'james', 'oir', 'rooom', 'told','door','service','not','front','hour','chacago','date','hop', 'two','day','like','thing','person','open','night','heard','over','double','once','morning','evening','number','call','could','rout','sixth','thechicagocritic','bagel','small','thank','large','thirty','reach','bathtub','ole','able','room','very','stay','about','ll','river','packege', 'above','chicago', 'abst', 'room', 'hotel','arrive','accordance', 'according', 'accordingly', 'across', 'act', 'actually', 'added', 'adj', 'after', 'afterwards', 'again', 'against', 'ah', 'all', 'almost', 'alone', 'along', 'already', 'also', 'although', 'always', 'am', 'among', 'amongst', 'an', 'and', 'announce', 'another', 'any', 'anybody', 'anyhow', 'anymore', 'anyone', 'anything', 'anyway', 'anyways', 'anywhere', 'apparently', 'approximately', 'are', 'aren', 'arent', 'arise', 'around', 'as', 'aside', 'ask', 'asking', 'at', 'auth', 'available', 'away',  'b', 'back', 'be', 'became', 'because', 'become', 'becomes', 'becoming', 'been', 'before', 'beforehand', 'begin', 'beginning', 'beginnings', 'begins', 'behind', 'being', 'believe', 'below', 'beside', 'besides', 'between', 'beyond', 'biol', 'both', 'brief', 'briefly', 'but', 'by', 'c', 'ca', 'came', 'can','co', 'com', 'i.e','come', 'comes', 'contain', 'containing', 'contains', 'd', 'date', 'did', "didn't", 'different', 'do', 'does', "doesn't", 'doing', 'done', "don't", 'down', 'downwards', 'due', 'during', 'e', 'each', 'ed', 'edu', 'effect', 'eg', 'eight', 'eighty', 'either', 'else', 'elsewhere', 'end', 'ending', 'enough', 'especially', 'et', 'et-al', 'etc', 'even', 'ever', 'every', 'everybody', 'everyone', 'everything', 'everywhere', 'ex', 'except', 'f', 'far', 'few', 'ff', 'fifth', 'first', 'five', 'fix', 'followed', 'following', 'follows', 'for', 'former', 'formerly', 'forth', 'found', 'four', 'from', 'further', 'furthermore', 'g', 'gave', 'get', 'gets', 'getting', 'give', 'given', 'gives', 'giving', 'go', 'goes', 'gone', 'got', 'gotten', 'h', 'had', 'happens', 'hardly', 'has', "hasn't", 'have', "haven't", 'having', 'he', 'hed', 'hence', 'her', 'here', 'hereafter', 'hereby', 'herein', 'heres', 'hereupon', 'hers', 'herself', 'hes', 'hi', 'hid', 'him', 'himself', 'his', 'hither', 'home', 'how', 'howbeit', 'however', 'hundred', 'i', 'id', 'ie', 'if', "i'll", 'im', 'in', 'inc', 'indeed', 'index', 'information', 'instead', 'into', 'invention', 'inward', 'is', "isn't", 'it', 'itd', "it'll", 'its', 'itself', "i've", 'j', 'just', 'k', 'keep\tkeeps', 'kept', 'kg', 'km', 'know', 'known', 'knows', 'l', 'largely', 'last', 'lately', 'later', 'latter', 'latterly', 'least', 'less', 'lest', 'let', 'lets', 'line', 'little', "'ll", 'look', 'looking', 'looks', 'ltd', 'm', 'made', 'mainly', 'make', 'makes', 'many', 'may', 'maybe', 'me', 'mean', 'means', 'meantime', 'meanwhile', 'merely', 'mg', 'might', 'million', 'miss', 'ml', 'more', 'moreover', 'most', 'mostly', 'mr', 'mrs', 'much', 'mug', 'must', 'n', 'na', 'name', 'namely', 'nay', 'nd', 'near', 'nearly', 'necessarily', 'necessary', 'need', 'needs', 'neither', 'never', 'nevertheless', 'new', 'next', 'nine', 'ninety', 'non', 'none', 'nonetheless', 'noone', 'nor', 'noted', 'nothing', 'now', 'o', 'obtain', 'obtained', 'obviously', 'of', 'off', 'oh', 'ok', 'okay', 'old',  'on', 'one', 'ones', 'only', 'onto', 'or', 'ord', 'other', 'others', 'otherwise', 'ought', 'our', 'ours', 'ourselves', 'out', 'outside', 'owing', 'own', 'p', 'page', 'pages', 'part', 'particular', 'particularly', 'past', 'per', 'perhaps', 'placed', 'please', 'plus', 'poorly', 'possible', 'possibly', 'potentially', 'pp', 'predominantly', 'present', 'previously', 'primarily', 'probably', 'promptly', 'proud', 'provides', 'put', 'q', 'que', 'quickly', 'quite', 'qv', 'r', 'ran', 'rather', 'rd', 're', 'readily', 'really', 'recent', 'recently', 'ref', 'refs', 'regarding', 'regardless', 'regards', 'related', 'relatively', 'research', 'respectively', 'right', 'run', 's', 'said', 'same', 'saw', 'say', 'saying', 'says', 'sec', 'section', 'see', 'seeing', 'seem', 'seemed', 'seeming', 'seems', 'seen', 'self', 'selves', 'sent', 'seven', 'several', 'shall', 'she', 'shed', "she'll", 'shes', 'should', 'show', 'showed', 'shown', 'showns', 'shows', 'similar', 'similarly', 'since', 'six', 'slightly', 'so', 'some', 'somebody', 'somehow', 'someone', 'somethan', 'something', 'sometime', 'sometimes', 'somewhat',  'specifically', 'specified', 'specify', 'specifying', 'sub', 'successfully', 'such', 'sufficiently', 'suggest', 'sup', 'sure\tt', 'take', 'taken', 'taking', 'tell', 'tends', 'th', 'that', "that'll", 'thats', "that've", 'the', 'their', 'theirs', 'them', 'themselves', 'then', 'thence', 'there', 'thereafter', 'thereby', 'thered', 'therefore', 'therein', "there'll", 'thereof', 'therere', 'theres', 'thereto', 'thereupon', "there've", 'these', 'they', 'theyd', "they'll", 'theyre', "they've", 'think', 'this', 'those', 'thou', 'though', 'thoughh', 'thousand', 'throug', 'through', 'throughout', 'thru', 'thus', 'til',  'to', 'together', 'too', 'took', 'toward', 'towards', 'tried', 'tries','try', 'trying', 'ts', 'twice', 'two', 'u', 'un', 'under', 'unfortunately', 'unless', 'unlike', 'unlikely', 'until', 'unto', 'up', 'upon', 'ups', 'us', 'use', 'used', 'useful', 'usefully', 'usefulness', 'uses', 'using', 'usually', 'v', 'value', 'various', "'ve",  'via', 'viz', 'vol', 'vols', 'vs', 'w','was', 'wasnt', 'way', 'wed', 'welcome', "we'll", 'went', 'were', 'werent', "we've", 'what', 'whatever', "what'll", 'whats', 'when', 'whence', 'whenever', 'where', 'whereafter', 'whereas', 'whereby', 'wherein', 'wheres', 'whereupon', 'wherever', 'whether', 'which', 'while', 'whim', 'whither', 'who', 'whod', 'whoever', 'whole', "who'll", 'whom', 'whomever', 'whos', 'whose', 'why', 'widely', 'willing', 'wish', 'with', 'within', 'without', 'wont', 'words', 'world', 'would', 'www', 'x', 'y', 'yes', 'yet', 'you', 'youd', "you'll", 'your', 'youre', 'yours', 'yourself', 'yourselves', "you've", 'z', 'zero']


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
    act1 = 0
    act2 = 0
    for w in words:
        act1 = weights[w][0] * words[w]
        act2 = weights[w][1] * words[w]

    act1 += bias[0]
    act2 += bias[1]
    return [act1, act2]


def learn():
    global words, weights, isVanilla, p, n, t, d, bias, c, cached_weights, cached_bias
    act = activation()
    y1 = 1 if p else -1
    y2 = 1 if t else -1
    a1 = y1*act[0]
    a2 = y2*act[1]

    if a1 <= 0 or a2 <= 0:
        for w in words:
            if a1 <= 0:
                weights[w][0] += y1 * words[w]
                cached_weights[w][0] += y1 * c * words[w]
            if a2 <= 0:
                weights[w][1] += y2 * words[w]
                cached_weights[w][1] += y2 * c * words[w]

        if a1 <= 0:
            bias[0] += y1
            cached_bias[0] += y1*c
        if a2 <= 0:
            bias[1] += y2
            cached_bias[1] += y2*c
    c += 1


def add_word(word, isInitial):
    global sw, all_words, words
    if (not word) or (word.lower() in sw) or not word[0].isalnum() :
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
                words["all_caps"] = 1
            else:
                words["all_caps"] = 1
    if contains_digit(word):
        word = "number"
    else:
        word = word.lower()
        word = get_root(word)
    if word in sw:
        return
    if isInitial:
        all_words.add(word)
    else:
        if word in words:
            words[word] = 1
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
        if (word.endswith("zing") and not word[-5] == 'z') or word.endswith("ving") or word.endswith("iking") or word.endswith("aking") or word.endswith("cing") or word.endswith("summing") or word.endswith("uding"):
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
        if word.endswith("ved") or word.endswith("uired") or word.endswith("iked") or ( word.endswith("ired") and "pair" not in word) or word.endswith("ated") or word.endswith("zed") or word.endswith("ced") or word.endswith("named") or word.endswith("sumed") or word.endswith("ged") or word.endswith("uled"):
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
        cached_weights[w] = [0, 0]


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


def update_avg_weights():
    global c
    for w in weights:
        weights[w][2] = round(weights[w][0] - (1 / c) * cached_weights[w][0], 2)
        weights[w][3] = round(weights[w][1] - (1 / c) * cached_weights[w][1], 2)
    bias[2] = round(bias[0] - (1 / c) * cached_bias[0], 2)
    bias[3] = round(bias[1] - (1 / c) * cached_bias[1], 2)




# ---------------- EXEC CODE -----------------------
vFile = "vanillamodel.txt"
aFile = "averagemodel.txt"
input_path = str(sys.argv[1])
sw = []
weights = dict()
n = 0
bias = [0, 0, 0, 0]
all_words = set()
words = dict()
total_words = 0
avg_w = dict()
p = n = d = t = False
init_stop_words()
all_files = glob.glob(os.path.join(input_path, '*/*/*/*.txt'))
cached_weights = dict()
cached_bias = [0,0]
c =0
all_lines = []
for file in all_files:
    p = False
    n = False
    d = False
    t = False
    f = open(file, "r")
    content = f.read().splitlines()
    f.close()
    lines = content[0]
    update_class(file)
    all_lines.append([lines, p, n, t, d])
    process_file_content(lines, 1)

n = len(all_words)
print(len(all_lines))
init_dictionary()


for i in range(1):
    random.shuffle(all_lines)
    for line in all_lines:
        words.clear()
        process_file_content(line[0], 0)
        p = line[1]
        n = line[2]
        t = line[3]
        d = line[4]
        learn()

update_avg_weights()
sorted_w = sorted(weights.items(), key=lambda kv: kv[1], reverse = True)

for w in sorted_w:
    print(w)

write_to_file()