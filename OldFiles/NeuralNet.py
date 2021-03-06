import os
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)
from Configuration import *

class NeuralNetwork:

    w = []
    b = []
    x = []
    y = []
    yPrime = []

    sess = None
    trainStep = None

    #Disable Warning
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

    def __init__(self, config, ticker):

        #Variables
        self.w = tf.Variable(tf.ones([config.numInputNodes, config.numOutputNodes]))
        self.b = tf.Variable(tf.ones([config.numOutputNodes]))
        self.x = tf.placeholder(tf.float32, shape=[None, config.numInputNodes])
        self.yPrime = tf.placeholder(tf.float32, shape=[None, config.numOutputNodes])
        self.y = tf.matmul(self.x, self.w) + self.b

        #Start Session
        self.sess = tf.InteractiveSession()
        self.sess.run(tf.global_variables_initializer())

        #Set up Trainer
        crossEntropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=self.yPrime, logits=self.y))
        self.trainStep = tf.train.GradientDescentOptimizer(0.5).minimize(crossEntropy)



    def train(self, inputData, outputData):

        self.trainStep.run(feed_dict={self.x: inputData, self.yPrime: outputData})

    def accuracy(self, inputTest, outputTest):

        correctPrediction = tf.equal(tf.argmax(self.y, 1), tf.argmax(self.yPrime, 1))
        accuracy = tf.reduce_mean(tf.cast(correctPrediction, tf.float32))
        return accuracy.eval(feed_dict={self.x: inputTest, self.yPrime: outputTest})

    def predict(self, inputData):

        output = tf.matmul(inputData, self.w) + self.b
        return output.eval()[0][0]

    def save(self, filename):

        saver = tf.train.Saver()
        saver.save(self.sess, "/tmp/" + filename + "/test.ckpt")

    def load(self, filename):

        saver = tf.train.Saver()
        saver.restore(self.sess, "/tmp/" + filename + "/test.ckpt")

config = Configuration()
model = NeuralNetwork(config,"temp")


# for _ in range(1000):
#   batch_xs, batch_ys = mnist.train.next_batch(1)
#   model.train(batch_xs[0], batch_ys[0])
