def __init__(self, max_length=310, num_terms=1000, num_tags=40):
    """Constructor. You can add code but do not remove any code.

    The arguments are arbitrary: when you are training on your own, PLEASE set
    them to the correct values (e.g. from main()).

    Args:
        max_lengths: maximum possible sentence length.
        num_terms: the vocabulary size (number of terms).
        num_tags: the size of the output space (number of tags).

    You will be passed these arguments by the grader script.
    """
    self.hidden_LSTM = 40

    self.max_length = max_length
    self.num_terms = num_terms
    self.num_tags = num_tags
    self.x = tf.placeholder(tf.int64, [None, self.max_length], 'X')
    self.lengths = tf.placeholder(tf.int32, [None], 'lengths')

    self.y = tf.placeholder(tf.int32, [None, self.max_length], 'Tags')
    self.session = tf.Session()

    # TODO(student): You must implement this.


def lengths_vector_to_binary_matrix(self, length_vector):
    """Returns a binary mask (as float32 tensor) from (vector) int64 tensor.

    Specifically, the return matrix B will have the following:
        B[i, :lengths[i]] = 1 and B[i, lengths[i]:] = 0 for each i.
    However, since we are using tensorflow rather than numpy in this function,
    you cannot set the range as described.
    """
    x = tf.sequence_mask(length_vector, maxlen=self.max_length)
    return tf.dtypes.cast(x, dtype=tf.float32)

    # TODO(student): You must implement this.


def save_model(self, filename):
    """Saves model to a file."""
    pass

    # TODO(student): You must implement this.


def load_model(self, filename):
    """Loads model from a file."""
    pass

    # TODO(student): You must implement this.


def build_inference(self):
    """Build the expression from (self.x, self.lengths) to (self.logits).

    Please do not change or override self.x nor self.lengths in this function.

    Hint:
        - Use lengths_vector_to_binary_matrix
        - You might use tf.reshape, tf.cast, and/or tensor broadcasting.
    """

    # TODO(student): make logits an RNN on x.
    # len_bm = self.lengths_vector_to_binary_matrix(self.lengths)
    # tf.concat ([self.x,len_bm],0)

    # I am using bi directional LSTM

    embedding = tf.get_variable('embeddings', [self.num_terms, self.hidden_LSTM])

    x_embedding = tf.nn.embedding_lookup(embedding, self.x)

    LSTM_bw = tf.contrib.rnn.LSTMCell(self.hidden_LSTM)

    LSTM_fw = tf.contrib.rnn.LSTMCell(self.hidden_LSTM)

    (f_out, b_out), temp = tf.nn.bidirectional_dynamic_rnn(LSTM_fw, LSTM_bw,
                                                                              x_embedding,
                                                                              sequence_length=self.lengths,
                                                                              dtype=tf.float32)

    out = tf.concat([f_out, b_out], axis=-1)

    W = tf.get_variable("Weight", dtype=tf.float32, shape=[2 * self.hidden_LSTM, self.num_tags])

    b = tf.get_variable("bias", shape=[self.num_tags], dtype=tf.float32, initializer=tf.zeros_initializer())

    n_steps = tf.shape(out)[1]

    out = tf.reshape(out, [-1, 2 * self.hidden_LSTM])

    predict = tf.matmul(out, W) + b

    self.logits = tf.reshape(predict, [-1, n_steps, self.num_tags])

    # self.logits = tf.zeros([tf.shape(self.x)[0], self.max_length, self.num_tags])

    # TODO(student): You must implement this.


def run_inference(self, terms, lengths):
    """Evaluates self.logits given self.x and self.lengths.

    Hint: This function is straight forward and you might find this code useful:
    # logits = session.run(self.logits, {self.x: terms, self.lengths: lengths})
    # return numpy.argmax(logits, axis=2)

    Args:
        terms: numpy int matrix, like terms_matrix made by BuildMatrices.
        lengths: numpy int vector, like lengths made by BuildMatrices.

    Returns:
        numpy int matrix of the predicted tags, with shape identical to the int
        matrix tags i.e. each term must have its associated tag. The caller will
        *not* process the output tags beyond the sentence length i.e. you can have
        arbitrary values beyond length.
    """

    logits = self.session.run(self.logits, {self.x: terms, self.lengths: lengths})
    return numpy.argmax(logits, axis=2)

    # return numpy.zeros_like(terms)

    # TODO(student): You must implement this.


def build_training(self):
    """Prepares the class for training.

    It is up to you how you implement this function, as long as train_on_batch
    works.

    Hint:
        - Lookup tf.contrib.seq2seq.sequence_loss
        - tf.losses.get_total_loss() should return a valid tensor (without raising
            an exception). Equivalently, tf.losses.get_losses() should return a
            non-empty list.
    """

    step = tf.Variable(0, trainable=False)
    val = 1e-2
    lr = tf.train.exponential_decay(val, step, 1000, 0.9, staircase=False)
    loss_val = tf.contrib.seq2seq.sequence_loss(self.logits, self.t,
                                                self.lengths_vector_to_binary_matrix(self.lengths))
    loss = tf.reduce_mean(loss_val)
    self.train_op = tf.train.AdamOptimizer(learning_rate=lr).minimize(loss)
    self.session.run(tf.global_variables_initializer())


def train_epoch(self, terms, tags, lengths, batch_size=32, lr=1e-7):
    """Performs updates on the model given training training data.

    This will be called with numpy arrays similar to the ones created in
    Args:
        terms: int64 numpy array of size (# sentences, max sentence length)
        tags: int64 numpy array of size (# sentences, max sentence length)
        lengths:
        batch_size: int indicating batch size. Grader script will not pass this,
            but it is only here so that you can experiment with a "good batch size"
            from your main block.
        lr: float for learning rate. Grader script will not pass this,
            but it is only here so that you can experiment with a "good learn rate"
            from your main block.

    Return:
        boolean. You should return True iff you want the training to continue. If
        you return False (or do not return anyhting) then training will stop after
        the first iteration!
    """

    len = terms.shape[0]

    indices = numpy.random.permutation(len)

    for start in range(0, len, batch_size):
        last = min(len, start + batch_size)

        bat_x = terms[indices[start:last]] + 0
        bat_y = tags[indices[start:last]] + 0
        bat_z = lengths[indices[start:last]] + 0

        self.session.run(self.train_op, {self.x: bat_x, self.y: bat_y, self.lengths: bat_z})

    return True

    # <-- Your implementation goes here.

    # Finally, make sure you uncomment the `return True` below.
    # return True

    # TODO(student): You can implement this to help you, but we will not call it.


def evaluate(self, terms, tags, lengths):
    pass