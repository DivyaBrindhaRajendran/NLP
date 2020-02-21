import glob
import os
import math
import random


def init_stop_words():
    global sw
    sw = ['a', 'james', 'oir', 'rooom', 'told','door','service','not','front','hour','chacago','date','hop', 'two','day','like','thing','person','open','night','heard','over','double','once','morning','evening','number','call','could','rout','sixth','thechicagocritic','bagel','small','thank','large','thirty','reach','bathtub','ole','able','room','very','stay','about','ll','river','packege', 'above','chicago', 'abst', 'room', 'hotel','arrive','accordance', 'according', 'accordingly', 'across', 'act', 'actually', 'added', 'adj', 'after', 'afterwards', 'again', 'against', 'ah', 'all', 'almost', 'alone', 'along', 'already', 'also', 'although', 'always', 'am', 'among', 'amongst', 'an', 'and', 'announce', 'another', 'any', 'anybody', 'anyhow', 'anymore', 'anyone', 'anything', 'anyway', 'anyways', 'anywhere', 'apparently', 'approximately', 'are', 'aren', 'arent', 'arise', 'around', 'as', 'aside', 'ask', 'asking', 'at', 'auth', 'available', 'away',  'b', 'back', 'be', 'became', 'because', 'become', 'becomes', 'becoming', 'been', 'before', 'beforehand', 'begin', 'beginning', 'beginnings', 'begins', 'behind', 'being', 'believe', 'below', 'beside', 'besides', 'between', 'beyond', 'biol', 'both', 'brief', 'briefly', 'but', 'by', 'c', 'ca', 'came', 'can','co', 'com', 'i.e','come', 'comes', 'contain', 'containing', 'contains', 'd', 'date', 'did', "didn't", 'different', 'do', 'does', "doesn't", 'doing', 'done', "don't", 'down', 'downwards', 'due', 'during', 'e', 'each', 'ed', 'edu', 'effect', 'eg', 'eight', 'eighty', 'either', 'else', 'elsewhere', 'end', 'ending', 'enough', 'especially', 'et', 'et-al', 'etc', 'even', 'ever', 'every', 'everybody', 'everyone', 'everything', 'everywhere', 'ex', 'except', 'f', 'far', 'few', 'ff', 'fifth', 'first', 'five', 'fix', 'followed', 'following', 'follows', 'for', 'former', 'formerly', 'forth', 'found', 'four', 'from', 'further', 'furthermore', 'g', 'gave', 'get', 'gets', 'getting', 'give', 'given', 'gives', 'giving', 'go', 'goes', 'gone', 'got', 'gotten', 'h', 'had', 'happens', 'hardly', 'has', "hasn't", 'have', "haven't", 'having', 'he', 'hed', 'hence', 'her', 'here', 'hereafter', 'hereby', 'herein', 'heres', 'hereupon', 'hers', 'herself', 'hes', 'hi', 'hid', 'him', 'himself', 'his', 'hither', 'home', 'how', 'howbeit', 'however', 'hundred', 'i', 'id', 'ie', 'if', "i'll", 'im', 'in', 'inc', 'indeed', 'index', 'information', 'instead', 'into', 'invention', 'inward', 'is', "isn't", 'it', 'itd', "it'll", 'its', 'itself', "i've", 'j', 'just', 'k', 'keep\tkeeps', 'kept', 'kg', 'km', 'know', 'known', 'knows', 'l', 'largely', 'last', 'lately', 'later', 'latter', 'latterly', 'least', 'less', 'lest', 'let', 'lets', 'line', 'little', "'ll", 'look', 'looking', 'looks', 'ltd', 'm', 'made', 'mainly', 'make', 'makes', 'many', 'may', 'maybe', 'me', 'mean', 'means', 'meantime', 'meanwhile', 'merely', 'mg', 'might', 'million', 'miss', 'ml', 'more', 'moreover', 'most', 'mostly', 'mr', 'mrs', 'much', 'mug', 'must', 'my', 'myself', 'n', 'na', 'name', 'namely', 'nay', 'nd', 'near', 'nearly', 'necessarily', 'necessary', 'need', 'needs', 'neither', 'never', 'nevertheless', 'new', 'next', 'nine', 'ninety', 'non', 'none', 'nonetheless', 'noone', 'nor', 'noted', 'nothing', 'now', 'o', 'obtain', 'obtained', 'obviously', 'of', 'off', 'oh', 'ok', 'okay', 'old',  'on', 'one', 'ones', 'only', 'onto', 'or', 'ord', 'other', 'others', 'otherwise', 'ought', 'ourselves', 'out', 'outside', 'owing', 'own', 'p', 'page', 'pages', 'part', 'particular', 'particularly', 'past', 'per', 'perhaps', 'placed', 'please', 'plus', 'poorly', 'possible', 'possibly', 'potentially', 'pp', 'predominantly', 'present', 'previously', 'primarily', 'probably', 'promptly', 'proud', 'provides', 'put', 'q', 'que', 'quickly', 'quite', 'qv', 'r', 'ran', 'rather', 'rd', 're', 'readily', 'really', 'recent', 'recently', 'ref', 'refs', 'regarding', 'regardless', 'regards', 'related', 'relatively', 'research', 'respectively', 'right', 'run', 's', 'said', 'same', 'saw', 'say', 'saying', 'says', 'sec', 'section', 'see', 'seeing', 'seem', 'seemed', 'seeming', 'seems', 'seen', 'self', 'selves', 'sent', 'seven', 'several', 'shall', 'she', 'shed', "she'll", 'shes', 'should', 'show', 'showed', 'shown', 'showns', 'shows', 'similar', 'similarly', 'since', 'six', 'slightly', 'so', 'some', 'somebody', 'somehow', 'someone', 'somethan', 'something', 'sometime', 'sometimes', 'somewhat',  'specifically', 'specified', 'specify', 'specifying', 'sub', 'successfully', 'such', 'sufficiently', 'suggest', 'sup', 'sure\tt', 'take', 'taken', 'taking', 'tell', 'tends', 'th', 'that', "that'll", 'thats', "that've", 'the', 'their', 'theirs', 'them', 'themselves', 'then', 'thence', 'there', 'thereafter', 'thereby', 'thered', 'therefore', 'therein', "there'll", 'thereof', 'therere', 'theres', 'thereto', 'thereupon', "there've", 'these', 'they', 'theyd', "they'll", 'theyre', "they've", 'think', 'this', 'those', 'thou', 'though', 'thoughh', 'thousand', 'throug', 'through', 'throughout', 'thru', 'thus', 'til',  'to', 'together', 'too', 'took', 'toward', 'towards', 'tried', 'tries','try', 'trying', 'ts', 'twice', 'two', 'u', 'un', 'under', 'unfortunately', 'unless', 'unlike', 'unlikely', 'until', 'unto', 'up', 'upon', 'ups', 'us', 'use', 'used', 'useful', 'usefully', 'usefulness', 'uses', 'using', 'usually', 'v', 'value', 'various', "'ve",  'via', 'viz', 'vol', 'vols', 'vs', 'w','was', 'wasnt', 'way', 'we', 'wed', 'welcome', "we'll", 'went', 'were', 'werent', "we've", 'what', 'whatever', "what'll", 'whats', 'when', 'whence', 'whenever', 'where', 'whereafter', 'whereas', 'whereby', 'wherein', 'wheres', 'whereupon', 'wherever', 'whether', 'which', 'while', 'whim', 'whither', 'who', 'whod', 'whoever', 'whole', "who'll", 'whom', 'whomever', 'whos', 'whose', 'why', 'widely', 'willing', 'wish', 'with', 'within', 'without', 'wont', 'words', 'world', 'would', 'www', 'x', 'y', 'yes', 'yet', 'you', 'youd', "you'll", 'your', 'youre', 'yours', 'yourself', 'yourselves', "you've", 'z', 'zero']


def contains_digit(word):
    if any(ch.isdigit() for ch in word):
        return 1
    return 0


def is_vowel(c):
    if c in ['a', 'e', 'i', 'o', 'u']:
        return 1
    return 0


def calculate_sum():
    global words, weights, bv1, bv2
    act1 = 0.0
    act2 = 0.0
    dic = weights
    for w in words:
        if w in dic:
            act1 += dic[w][0] * word_val[w][0]
            act2 += dic[w][1] * word_val[w][1]
    act1 += bv1
    act2 += bv2
    return [act1, act2]


def update_weights_pn():
    y1 = 1 if p else -1
    y2 = 1 if t else -1
    global bv1, bv2, c
    act = calculate_sum()
    a1 = y1 * act[0]
    a2 = y2 * act[1]

    if a1 <= 0 or a2 <= 0:
        for w in words:
            if a1 <= 0:
                wf = word_val[w][0]
                weights[w][0] = round(weights[w][0] + y1 * wf,2)
                cached_weights[w][0] = round(cached_weights[w][0] + (y1 * c * wf),2)
            if a2 <= 0:
                wf = word_val[w][1]
                weights[w][1] = round(weights[w][1] + y2 * wf,2)
                cached_weights[w][1] = round(cached_weights[w][1] + (y2 * c * wf),2)

        if a1 <= 0:
            bv1 += y1
            cached_bias[0] += y1 * c
        if a2 <= 0:
            bv2 += y2
            cached_bias[1] += y2 * c
    c += 1


def percep_learn():
    global words, bv1
    update_weights_pn()


def init_word(word):
    global weights, words_dict
    if word not in words_dict:
        weights[word] = [0, 0, 0, 0]
        words_dict[word] = [0, 0, 0, 0]
        word_val[word] = [0, 0]
        cached_weights[word] = [0,0]


def add_word(word):
    global sw, words
    if (not word) or (word.lower() in sw) or len(word) == 1:
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
        words.add("allcaps")
    word = word.lower()
    if contains_digit(word):
        word = "number"
    words.add(word)


def update_dict(word):
    global sw
    if (not word) or (word.lower() in sw) or len(word) == 1:
        return
    temp = ""
    found_symbol = False
    if len(word) >= 2:
        for ch in word:
            if ch.isalnum():
                temp += ch
            else:
                update_dict(temp)
                temp = ""
                found_symbol = True
    if found_symbol:
        update_dict(temp)
        return
    if word.isupper():
        update_dict("allcaps")
    word = word.lower()
    if contains_digit(word):
        word = "number"

    init_word(word)

    if p: words_dict[word][0] += 1
    else: words_dict[word][1] += 1
    if d: words_dict[word][3] += 1
    else: words_dict[word][2] += 1


def assign_word_values():
    global words_dict
    for w in words_dict:
        diff_p = math.fabs(words_dict[w][0] - words_dict[w][1])
        diff_p = 0.1 if diff_p < 5 else diff_p
        diff_d = math.fabs(words_dict[w][2] - words_dict[w][3])
        diff_d = 0.1 if diff_d < 5 else diff_d
        word_val[w][0] = round(diff_p/(words_dict[w][1]+words_dict[w][0]+1), 2)
        word_val[w][1] = round(diff_d/(words_dict[w][2]+words_dict[w][3]+1), 2)


def process_file_content(lines):
    words_temp = lines.split(" ")
    for w in words_temp:
        update_dict(w)


def update_class(fname):
    global p, n, d, t
    if "negative_" in fname: n = True
    else: p = True
    if "deceptive_" in fname: d = True
    else: t = True


def write_content():
    global vFile, aFile
    f1 = open(vFile, "w+")
    f2 = open(aFile, "w+")
    global all_files
    for w in weights:
        f1.write(w)
        f1.write("\t")
        f1.write(str(weights[w][0]))
        f1.write("\t")
        f1.write(str(weights[w][1]))
        f1.write("\t")
        f1.write(str(word_val[w][0]))
        f1.write("\t")
        f1.write(str(word_val[w][1]))
        f1.write("\n")
        f2.write(w)
        f2.write("\t")
        f2.write(str(weights[w][2]))
        f2.write("\t")
        f2.write(str(weights[w][3]))
        f2.write("\t")
        f2.write(str(word_val[w][0]))
        f2.write("\t")
        f2.write(str(word_val[w][1]))
        f2.write("\n")
    f1.write(str(bv1)+":"+ str(bv2))
    f2.write(str(ba1) + ":" + str(ba2))
    f1.close()
    f2.close()


def update_avg_weights():
    global c, ba1, ba2, bv1, bv2
    for w in weights:
        weights[w][2] = round(weights[w][0] - (1 / c) * cached_weights[w][0], 2)
        weights[w][3] = round(weights[w][1] - (1 / c) * cached_weights[w][1], 2)
    ba1 = round(bv1 - (1 / c) * cached_bias[0], 2)
    ba2 = round(bv2 - (1 / c) * cached_bias[1], 2)



# ------------------------------------------- CODE BEGINS -------------------------------------------------------------
vFile = "vanillamodel.txt"
aFile = "averagemodel.txt"
sw = []
c = 0
bv1 = 0
bv2 = 0
ba1 = 0
ba2 = 0
words_dict = {}
weights = dict()
cached_weights = dict()
cached_bias = [0,0]
total_words = 0
p = n = d = t = False
word_val = {}
words = set()
init_stop_words()
fileNames =[]
all_files = glob.glob(os.path.join("op_spam_training_data", '*/*/*/*.txt'))
all_lines = []

for file in all_files:
    p = n = d = t = False
    f = open(file, "r")
    content = f.read().splitlines()
    f.close()
    lines = content[0]
    update_class(file)
    all_lines.append([lines, p, n, t, d])
    process_file_content(lines)

assign_word_values()

for i in range(20):
    random.shuffle(all_lines)
    for line in all_lines:
        words.clear()
        p = line[1]
        n = line[2]
        t = line[3]
        d = line[4]
        for w in line[0].split(" "):
             add_word(w)
        percep_learn()

sorted_list = sorted(weights.items(), key=lambda kv: kv[1], reverse = True)
#print(sorted_list)
update_avg_weights()
write_content()
