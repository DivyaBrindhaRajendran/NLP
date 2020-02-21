
vocab_dict = dict()
trans_dict = dict()
start_dict = dict()
states = []
set_words = set()


def contains_digit(word):
    if any(ch.isdigit() for ch in word):
        return 1
    return 0


def all_nums(word):
    for x in word:
        if x.isalpha():
            return 0
    return 1


def get_word(word):
    return word
    word = word.lower()
    if len(word) <= 1:
        if len(word) == 1:
            if word[0].isdigit():
                return "all_nums"
            elif not word[0].isalnum():
                return "my_symbol"
        return word
    if all_nums(word):
        return "all_nums"
    if ":" in word:
        if contains_digit(word):
            return "colon_num_word"
    if "-" in word:
        if contains_digit(word):
            return "hyphen_num_word"
    if contains_digit(word):
        return "num_word"
    return word


def extract_probabilities():
    global trans_dict, vocab_dict, it_trans_dict, it_vocab_dict
    f = open("hmmmodel.txt", "r", encoding = 'UTF-8')
    lines = f.read().splitlines()
    tag = ''
    start = False
    for line in lines:
        if not line:
            continue
        if "*Emission*" in line:
            dic = vocab_dict
            start = False
            continue
        elif "*Transition*" in line:
            dic = trans_dict
            start = False
            continue
        elif "*Start*" in line:
            dic = start_dict
            start = True
            continue
        elif "*Words*:" in line:
            line = line[8:]
            ws = line.split("-")
            for w1 in ws:
                if not w1:
                    continue
                set_words.add(w1)
            continue
        if not start:
            if "->" in line and line.endswith("->"):
                tag = line.split("->")[0]
                continue
            tag2 = line.split("\t")
            if tag not in dic:
                dic[tag] = dict()
            dic[tag][tag2[0]] = float(tag2[1])
        else:
            tags = line.split("\t")
            dic[tags[0]] = float(tags[1])

    f.close()


def update_states():
    global states, trans_dict
    for key in trans_dict:
        states.append(key)


def get_dict():
    dic = dict()
    for key in states:
        dic[key] = [0, None]
    return dic


def init_prob_matrix(words):
    global matrix
    for w in words:
        dic = get_dict()
        matrix.append(dic)


def get_list_words(line):
    return line.split()


def initialize(word):
    global states, matrix
    word = get_word(word)
    for s in states:
        if word not in set_words:
            obs = 1
        elif word not in vocab_dict[s]:
            obs = 0
        else:
            obs = vocab_dict[s][word]
        trans = start_dict[s]
        matrix[0][s][0] = trans * obs


def find_max(index, curState, word1):
    word = get_word(word1)
    if word not in set_words:
        obs = 1
    elif word not in vocab_dict[curState]:
        obs = 0
    else:
        obs = vocab_dict[curState][word]
    max = 0.0
    prev_state = curState
    for s in states:
        trans = trans_dict[s][curState]
        p = matrix[index-1][s][0] * trans * obs
        if p > max:
            max = p
            prev_state = s
    return [max, prev_state]


def get_tagged_line(words, max_state, n):
    global matrix
    updated = []
    i = n-1
    while i >= 0:
        updated.append(words[i]+"/"+max_state)
        max_state = matrix[i][max_state][1]
        i -= 1
    updated.reverse()
    return updated


def HMM(line):
    global matrix
    words = get_list_words(line)
    init_prob_matrix(words)
    initialize(get_word(words[0]))
    n = len(words)
    for i in range(1,n):
        for s in states:
            max = find_max(i, s, words[i])
            matrix[i][s][0] = max[0]
            matrix[i][s][1] = max[1]

    max_state = None
    max = 0
    for s in states:
        if matrix[n-1][s][0] > max:
            max = matrix[n-1][s][0]
            max_state = s
    return get_tagged_line(words, max_state, n)


# -----------------------------------------------------------
extract_probabilities()
inputFile = "ja_gsd_dev_raw.txt"
outputFile = "hmmoutput.txt"
update_states()
matrix = []
f = open(inputFile, 'r', encoding="UTF-8")
fw = open(outputFile, 'w+', encoding="UTF-8")
lines = f.read().splitlines()
for l in lines:
    tagged = HMM(l)
    updated_line = ""
    for w in tagged:
        updated_line += w+" "
    updated_line = updated_line[:-1]+"\n"
    fw.write(updated_line)
f.close()
fw.close()
