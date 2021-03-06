"""
This file is to build a one layer CNN neural network

Created by Zexi Chen(zchen22)
Date: Oct 2, 2016
"""

import numpy as np
import tensorflow as tf
#import matplotlib.pyplot as plt
import math

class ConvLayer(object):
    """
    build a one layer of the CNN network
    """
    def __init__(
        self,
        w_shape,
        b_shape,
        input,
        weight_scale = 1e-2,
        activation = tf.nn.relu,        
        n_visible = 46,
        n_hidden =  10, 
        num_series = 2, 
        dropout = 0.5
    ):

        # input dimension
        self.n_visible = n_visible
        # output dimension
        self.n_hidden = n_hidden

        # Weight matrix shape
        if w_shape is None:
            self.w_shape = [n_visible/num_series, 1, 1, n_hidden]
        else:
            self.w_shape = w_shape

        #bias shape
        if b_shape is None:
            self.b_shape = [n_hidden]
        else:
            self.b_shape = b_shape

        if input is None:
            self.input = tf.placeholder(tf.float32, shape=[None, n_visible])
        else:
            self.input = input
            
        self.weight_scale = weight_scale
        self.num_series = num_series
        self.dropout = dropout

        # initialize Weight matrix and bias vector
        self.W = self.weight_variable(self.w_shape)
        self.b = self.bias_variable(self.b_shape)

        # nonlinear transformation function
        self.activation = activation
        self.output = self.forward_prop()

    # define the weight matrix, initialize randomly 
    # truncated_normal: output random values from a truncated normal distribution with value out of 2 sd dropped 
    def weight_variable(self, shape):
        initial = tf.truncated_normal(shape, stddev=self.weight_scale)
        return tf.Variable(initial)

    # define the bias
    def bias_variable(self, shape):
        initial = tf.constant(0.1, shape=shape)
        return tf.Variable(initial)

    # specify the model we use and set up the paratemers
    def conv2d(self, x, W):
        return tf.nn.conv2d(x, W, strides=[1,self.n_visible/2,1,1], padding='SAME')

    # activation(W'x+b)
    def forward_prop(self):
        x_ts = tf.reshape(self.input, [-1, self.n_visible, 1, 1])
        h_conv = self.activation(self.conv2d(x_ts, self.W) + self.b)
        if self.dropout > 0:
            h_conv = tf.nn.dropout(h_conv, self.dropout)
        h_conv_reshape = tf.reshape(h_conv, [-1, 2 * self.n_hidden])

        return h_conv_reshape

    # define the cost function
    def cost_function(self, dtw_dists):
        h_conv_reshape = self.forward_prop()
        hidden_feature_diff = tf.sub(h_conv_reshape[:,:self.n_hidden], h_conv_reshape[:,self.n_hidden:])

        square_euclidean = tf.reduce_sum(tf.square(hidden_feature_diff), 1, keep_dims=True)

        cost = tf.reduce_mean(tf.square(tf.sub(dtw_dists, square_euclidean)))

        return cost


