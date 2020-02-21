import os
import glob
import numpy
import tensorflow as tf
import random

class SequenceModel(object):

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
        self.max_length = max_length
        self.num_terms = num_terms
        self.num_tags = num_tags
        self.x = tf.placeholder(tf.int64, [None, self.max_length], 'X')
        self.lengths = tf.placeholder(tf.int32, [None], 'lengths')
        self.sess = None
        self.embedding_dimension = 30
        self.n_hidden = 60
        self.is_training = tf.placeholder(tf.bool, shape=[], name="is_training")
        self.learning_rate = tf.placeholder(tf.float32, name="learning_rate")
        self.POS_tags = tf.placeholder(tf.int32, shape=[None, None], name="POS_Tags")

    # TODO(student): You must implement this.
    def lengths_vector_to_binary_matrix(self, length_vector):
        """Returns a binary mask (as float32 tensor) from (vector) int64 tensor.

        Specifically, the return matrix B will have the following:
            B[i, :lengths[i]] = 1 and B[i, lengths[i]:] = 0 for each i.
        However, since we are using tensorflow rather than numpy in this function,
        you cannot set the range as described.
        """
        return tf.cast(tf.range(self.max_length) < tf.reshape(length_vector, (-1, 1)), tf.float32)

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

        xemb = tf.get_variable(name="word_embedding", dtype=tf.float32, trainable=True,
                               shape=[self.num_terms, self.embedding_dimension])
        xemb = tf.nn.embedding_lookup(xemb, self.x, name="word_embedding")
        rnn_cell = tf.keras.layers.SimpleRNNCell(self.n_hidden)
        states = []
        curr_state = tf.zeros(shape=(1, self.n_hidden))
        for i in range(self.max_length):
            curr_state = rnn_cell(xemb[:, i, :], [curr_state])[0]
            states.append(curr_state)
        stacked_states = tf.stack(states, axis=1)
        self.logits = tf.layers.dense(stacked_states, units=self.num_tags, use_bias=True)

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
        logits, _ = self.sess.run([self.logits, self.lengths],
                                  {self.x: terms, self.lengths: lengths, self.is_training: False})
        return numpy.argmax(logits, axis=2)

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
        loss = tf.contrib.seq2seq.sequence_loss(self.logits, self.POS_tags,
                                                self.lengths_vector_to_binary_matrix(self.lengths))
        optimized = tf.train.AdamOptimizer(learning_rate=self.learning_rate)
        self.train_op = optimized.minimize(loss)

        self.sess = tf.Session()
        self.sess.run(tf.global_variables_initializer())

    def train_epoch(self, terms, tags, lengths, batch_size=10, lr=0.001):
        """Performs updates on the model given training training data.

        This will be called with numpy arrays similar to the ones created in
        Args:
            terms: int64 numpy array of size (# sentences, max sentence length)
            tags: zint64 numpy array of size (# sentences, max sentence length)
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

        # <-- Your implementation goes here.
        # Finally, make sure you uncomment the `return True` below.
        # return True

        def batch_step(batch_x, batch_y, batch_lengths, lr):
            self.sess.run(self.train_op, {
                self.x: batch_x,
                self.POS_tags: batch_y,
                self.lengths: batch_lengths,
                self.is_training: True,
                self.learning_rate: lr,
            })

        def step(lr, batch_size):

            random_indices = numpy.random.permutation(terms.shape[0])

            for si in range(0, terms.shape[0], batch_size):
                se = min(si + batch_size, terms.shape[0])
                slice_x = terms[random_indices[si:se]] + 0
                slice_tags = tags[random_indices[si:se]]
                slice_lengths = lengths[si:se]
                batch_step(slice_x, slice_tags, slice_lengths, lr)

        step(lr, batch_size)
        for iteration, current_learning_rate in [(2, lr)]:
            for _ in range(iteration):
                step(current_learning_rate, batch_size)

        return True

    # TODO(student): You can implement this to help you, but we will not call it.
    def evaluate(self, terms, tags, lengths):
        pass