import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
import time as tm

mnist = input_data.read_data_sets("/tmp/data", one_hot=True)

hm_epochs = 3
batch_size = 128
n_classes = 10 # MNIST total classes (0-9 digits)

#height by width
x = tf.placeholder('float', [None, 784])
y = tf.placeholder('float', [None, n_classes])     

def conv2d(x, W):
    return tf.nn.conv2d(x,W, strides = [1,1,1,1], padding='SAME')

def maxpool2d(x):
    return tf.nn.max_pool(x, ksize=[1,2,2,1], strides=[1,2,2,1], padding='SAME')

def neural_network_model(x):
    weights = {
        # 5 x 5 convolution, 1 input image, 32 outputs
        'W_conv1':tf.Variable(tf.random_normal([5, 5, 1, 32])),
        # 5x5 conv, 32 inputs, 64 outputs
        'W_conv2':tf.Variable(tf.random_normal([5,5,32,64])),
        #fully connected, 7*7*64 inputs, 1024 outputs
        'W_fc':tf.Variable(tf.random_normal([7*7*64, 1024])),
        #1024 inputs, 10 outputs (class prediction)
        'out':tf.Variable(tf.random_normal([1024,n_classes]))
     }

    biases = {
        'b_conv1': tf.Variable(tf.random_normal([32])),
        'b_conv2': tf.Variable(tf.random_normal([64])),
        'b_fc': tf.Variable(tf.random_normal([1024])),
        'out': tf.Variable(tf.random_normal([n_classes]))

     }

    #Reshape input to a 4D tensor
    x = tf.reshape(x, shape=[-1,28,28,1])
    #Convolution Layer, using our funciton
    conv1 = tf.nn.relu(conv2d(x, weights['W_conv1'])+biases['b_conv1'])
    #Max Pooling (down-sampling)
    conv1 = maxpool2d(conv1)
    #Convolution Layer
    conv2 = tf.nn.relu(conv2d(conv1, weights['W_conv2'])+biases['b_conv2'])
    #Max Pooling (down-sampling)
    conv2 = maxpool2d(conv2)

    #Fully connected layer
    #Reshape conv2 output to fit fully connected layer
    fc = tf.reshape(conv2, [-1, 7*7*64])
    fc = tf.nn.relu(tf.matmul(fc, weights['W_fc']) + biases['b_fc'])

    output = tf.matmul(fc, weights['out']) + biases['out']
    return output


def train_neural_network(x):
    start = tm.time()
    print('Starting...')
    prediction = neural_network_model(x)
    a = tf.nn.softmax_cross_entropy_with_logits(logits = prediction, labels = y)
    cost = tf.reduce_mean(a)
    #                          learning rate = 0.001
    optimizer = tf.train.AdamOptimizer().minimize(cost)

    # cycles of feed forward +backdrops

    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())

        for epoch in range(hm_epochs):
            epoch_loss = 0
            for _ in range(int(mnist.train.num_examples/batch_size)):
                epoch_x, epoch_y = mnist.train.next_batch(batch_size)
                _, c = sess.run([optimizer, cost], feed_dict = {x: epoch_x, y: epoch_y})
                epoch_loss += c
            print('Epoch', epoch, 'completed out of', hm_epochs, 'loss:', epoch_loss)

        correct = tf.equal(tf.argmax(prediction,1), tf.argmax(y,1))

        accuracy = tf.reduce_mean(tf.cast(correct, 'float'))
        end = tm.time()
        print('Time elapsed:')
        print(end - start)
        print('\n')
        print('Accuracy:', accuracy.eval({x:mnist.test.images, y:mnist.test.labels}))


train_neural_network(x)