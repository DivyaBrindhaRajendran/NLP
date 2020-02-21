import glob
import os

vocab_dict = dict()
it_vocab_dict = dict()
it_trans_dict = dict()
trans_dict = dict()
start_dict = dict()
it_start_dict = dict()

def update_emission_count(word, tag):
    global isJ, ja_w, it_w, trans_dict, it_vocab_dict
    vocab = vocab_dict if isJ else it_vocab_dict
    if word in vocab[tag][1]:
        vocab[tag][1][word] += 1
    else:
        vocab[tag][1][word] = 1
    vocab[tag][0] += 1



# Transition from tag1 -> tag2
def update_transition_count(tag1, tag2):
    global isJ, trans_dict, it_trans_dict
    trans = trans_dict if isJ else it_trans_dict
    if tag2 in trans[tag1][1]:
        trans[tag1][1][tag2] += 1
    else:
        trans[tag1][1][tag2] = 1
    trans[tag1][0] += 1


def add_new_tag_to_vocab(tag):
    global isJ, vocab_dict, it_vocab_dict
    tag_dict = dict()
    vocab = vocab_dict if isJ else it_vocab_dict
    vocab[tag] = [0, tag_dict]


def add_new_tag_to_trans(tag):
    global isJ, trans_dict, it_trans_dict
    tag_dict = dict()
    trans = trans_dict if isJ else it_trans_dict
    trans[tag] =[0, tag_dict]


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

    if len(word) <= 1:
        if len(word) == 1:
            if word[0].isdigit():
                return "all_nums"
        return word
    if all_nums(word):
        return "all_nums"
    if ":" in word:
        if contains_digit(word):
            return "colon_num_word"
        else:
            return "colon_word"
    if "-" in word:
        if contains_digit(word):
            return "hyphen_num_word"
        else:
            return "hyphen"
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
            continue
        elif "*Start*" in line:
            dic = start_dict
            start = True
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

# -----------------------------------------------------------
extract_probabilities()

print(vocab_dict)
print(it_vocab_dict)
print(trans_dict)
print(it_trans_dict)