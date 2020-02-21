import tensorflow as tf
import numpy as np

data = np.arange(1, 100 + 1)
data_input = tf.convert_to_tensor(data)
batch_shuffle = tf.train.shuffle_batch([data_input], enqueue_many=True, batch_size=10, capacity=100, min_after_dequeue=10, allow_smaller_final_batch=True)
batch_no_shuffle = tf.train.batch([data_input], enqueue_many=True, batch_size=10, capacity=100, allow_smaller_final_batch=True)

"""
        fw_pass= tf.contrib.rnn.LSTMCell(50)
        bw_pass= tf.contrib.rnn.LSTMCell(50)

        (output_fw, output_bw), _ = tf.nn.bidirectional_dynamic_rnn(cell_fw,
                                                                    cell_bw,
                                                                    tf.cast(tf.reshape(self.x, (tf.shape(self.x)[0],
                                                                                                tf.shape(self.x)[1],
                                                                                                1)), dtype=tf.float32),
                                                                    sequence_length=self.lengths,
                                                                    dtype=tf.float32,
                                                                    )
        context_rep = tf.concat([output_fw, output_bw], axis=-1)
        W = tf.get_variable("W", shape=[2 * 50, self.num_tags],
                            dtype=tf.float32)

        b = tf.get_variable("b", shape=[self.num_tags], dtype=tf.float32,
                            initializer=tf.zeros_initializer())

        ntime_steps = tf.shape(context_rep)[1]
        context_rep_flat = tf.reshape(context_rep, [-1, 2 * 50])
        self.logits = tf.matmul(context_rep_flat, W) + b
        self.logits = tf.reshape(self.logits, [-1, ntime_steps, self.num_tags])
        """
with tf.Session() as sess:
    coord = tf.train.Coordinator()
    threads = tf.train.start_queue_runners(coord=coord)
    for i in range(10):
        print(i, sess.run([batch_shuffle, batch_no_shuffle]))
    coord.request_stop()
    coord.join(threads)