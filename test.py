import tensorflow as tf


cluster = tf.train.ClusterSpec({"local": ["45.42.12.32:43210", "localhost:2223"]})

x = tf.constant(2)


with tf.device("/job:local/task:1"):
    y2 = x - 66

with tf.device("/job:local/task:0"):
    y1 = x + 300
    y = y1 + y2


with tf.Session("grpc://45.42.12.32:43210") as sess:
    result = sess.run(y)
    print(result)