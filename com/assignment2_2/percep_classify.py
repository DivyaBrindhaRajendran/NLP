import glob
import os
import math


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


def init_dictionary_v():
    global total_words
    global words_dict_v, model, vb1, vb2
    f = open(model, "r")
    content = f.read().splitlines()
    f.close()
    for line in content:
        if line and "\t" in line:
            entry = line.split("\t")
            words_dict_v[entry[0]] = [float(entry[1]), float(entry[2]), float(entry[3]), float(entry[4])]
        elif "[" not in line:
            nums = line.split(":")
            vb1 = float(nums[0])
            vb2 = float(nums[1])


def add_word(word):
    global sw, words
    if (not word) or (word.lower() in sw):
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
    word = word.lower()
    if contains_digit(word):
        word = "number"
    words.append(word)

def assign_word_values():
    global words_dict
    for w in words_dict:
        diff_p = math.fabs(words_dict[w][0] - words_dict[w][1])
        diff_p = 0.01 if diff_p < 5 else diff_p
        diff_d = math.fabs(words_dict[w][2] - words_dict[w][3])
        diff_d = 0.01 if diff_d < 5 else diff_d
        word_val[w][0] = math.ceil(diff_p*100 / (words_dict[w][1]+words_dict[w][0]+1))
        word_val[w][1] = math.ceil(diff_d*100 / (words_dict[w][2]+words_dict[w][3]+1))


def process_file_content(lines):
    global words
    words_temp = lines.split(" ")
    words = []
    for w in words_temp:
        add_word(w)


def classify():
        global p,n,d,t,words
        a1 = 0.0
        a2 = 0.0
        for w in words:
            if w in words_dict_v:
                a1 += words_dict_v[w][0]*words_dict_v[w][2]
                a2 += words_dict_v[w][1]*words_dict_v[w][3]
        a1 += vb1
        a2 += vb2

        if a1 > 0:
            p = True
        else: n = True

        if a2 > 0:
            t = True
        else: d = True


# -----------------------------------------------------------------------------------------------------------------
words_dict_v = {}
model = "averagemodel.txt"
#str(sys.argv[1])
output_file = "percepoutput.txt"
#str(sys.argv[2])
vb1 = 0
vb2 = 0
words_dict_v = {}
words_dict_a = {}
total_words = 0
word_val = {}
init_dictionary_v()
fileNames =[]
sw =[]
all_files = glob.glob(os.path.join("test", '*/*/*/*.txt'))
pd = 0
pt = 0
nd = 0
nt = 0
pd_n = 0
pt_n = 0
nd_n = 0
nt_n = 0
f1 = open(output_file,"w+")
for file in all_files:
    p = n = d = t = False
    f = open(file, 'r')
    content = f.read().splitlines()
    f.close()
    lines = content[0]
    process_file_content(lines)
    classify()
    if "N_D" in file:
        nd_n+=1
        if n and d:
            nd+=1
    elif "N_T" in file:
        nt_n+=1
        if n and t:
            nt+=1
    elif "P_D" in file:
        pd_n+=1
        if p and d:
            pd+=1
    else:
        pt_n+=1
        if p and t:
            pt+=1
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

print(nd, nd_n)
print(nt, nt_n)
print(pd, pd_n)
print(pt, pt_n)


avg = (nt+nd+pd+pt) / 320
print(str(avg))