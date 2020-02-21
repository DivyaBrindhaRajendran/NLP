import sys

vocab_dict = dict()
it_vocab_dict = dict()
it_trans_dict = dict()
trans_dict = dict()
start_dict = dict()
it_start_dict = dict()
s = 0;


def update_emission_count(word, tag):
    vocab = vocab_dict
    if word in vocab[tag][1]:
        vocab[tag][1][word] += 1
    else:
        vocab[tag][1][word] = 1
    vocab[tag][0] += 1


def calculate_prob_update_model_file():
    global trans_dict, vocab_dict
    f = open("hmmmodel.txt", "w+", encoding='UTF-8', errors='ignore')
    f.write("*Transition*\n")
    for tag in trans_dict:
        total = trans_dict[tag][0]
        f.write(tag + "->\n")
        for follow_tag in trans_dict[tag][1]:
            f.write(follow_tag + "\t" + str(round(trans_dict[tag][1][follow_tag] / total, 5)) + "\n")
    f.write("*Emission*\n")
    for tag in vocab_dict:
        total = vocab_dict[tag][0]
        f.write(tag + "->\n")
        for word in vocab_dict[tag][1]:
            f.write(word + "\t" + str(round(vocab_dict[tag][1][word] / total, 5)) + "\n")
    f.write("*Start*\n")
    for tag in start_dict:
        f.write(tag + "\t" + str(round(start_dict[tag] / s, 3)) + "\n")
    f.close()


# Transition from tag1 -> tag2
def update_transition_count(tag1, tag2):
    global isJ, trans_dict, it_trans_dict
    trans = trans_dict
    if tag2 in trans[tag1][1]:
        trans[tag1][1][tag2] += 1
    else:
        trans[tag1][1][tag2] = 1
    trans[tag1][0] += 1


def add_new_tag_to_vocab(tag):
    global isJ, vocab_dict, it_vocab_dict
    tag_dict = dict()
    vocab = vocab_dict
    vocab[tag] = [0, tag_dict]


def add_new_tag_to_trans(tag):
    global isJ, trans_dict, it_trans_dict
    tag_dict = dict()
    trans = trans_dict
    trans[tag] = [0, tag_dict]


def contains_digit(word):
    if any(ch.isdigit() for ch in word):
        return 1
    return 0


def all_nums(word):
    for x in word:
        if not x.isdigit():
            return 0
    return 1


def get_word(word):
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


def parse_line_and_update(line):
    global isJ, start_dict, vocab_dict, trans_dict, it_s, it_start_dict, it_vocab_dict, it_trans_dict, s, unique_tags
    vocab = vocab_dict
    trans = trans_dict
    start = start_dict
    prev = None
    for w in line.split():
        splits = w.split("/")
        word = ""
        for it in range(0, len(splits) - 1):
            word += str(splits[it])
        word = get_word(word)
        # set_words.add(word)
        tag = splits[-1]
        # unique_tags.add(tag)
        if tag not in vocab:
            add_new_tag_to_vocab(tag)
        if prev:
            if prev not in trans:
                add_new_tag_to_trans(prev)
            update_transition_count(prev, tag)
        else:
            if tag not in start:
                start[tag] = 1
            else:
                start[tag] += 1
            s += 1
        update_emission_count(word, tag)
        prev = tag


# -----------------------------------------------------------
model_file = "hmmmodel.txt"
train_file = sys.argv[1]

print(train_file)

f = train_file
fp = open(f, "r", encoding='UTF-8', errors='ignore')
lines = fp.read().splitlines()
for line in lines:
    parse_line_and_update(line)
fp.close()
calculate_prob_update_model_file()

# ------------------------------------------------------------


