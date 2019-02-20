#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 17 15:36:08 2019

@author: zhenhao
"""

#import tensorflow as tf
from storer import pickleStorer
#import squadProcessor
import numpy as np
from sklearn.model_selection import train_test_split

store=pickleStorer()

data, longQA=store.loadSquadEncoding('dev')
print(len(data))

#x=[]
#y=[]
#for entry in data:
#    for word in entry:
#        x.append(word['values'])
#        y.append([int(word['start']), int(word['end'])])
#
#X=np.asarray(x)
#Y=np.asarray(y)
#
#X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2)
#
##inputs
#input_size=X_train.shape[1]
#output_size=y_train.shape[1]
#inputs = tf.placeholder(tf.float32, shape=(None, input_size), name='inputs')
#label = tf.placeholder(tf.float32, shape=(None, output_size), name='labels')
#
##output layer
#wo = tf.Variable(tf.random_normal([output_size, input_size], stddev=0.01), name='wo')
#bo = tf.Variable(tf.random_normal([output_size, 1]), name='bo')
#yo = tf.transpose(tf.add(tf.matmul(wo, tf.transpose(inputs)), bo))
#
## Loss function and optimizer
#lr = tf.placeholder(tf.float32, shape=(), name='learning_rate')
#loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=yo, labels=label))
#optimizer = tf.train.GradientDescentOptimizer(lr).minimize(loss)
#
##prediction
#pred = tf.nn.softmax(yo)
#pred_label = tf.argmax(pred, 1)
#correct_prediction = tf.equal(tf.argmax(pred, 1), tf.argmax(label, 1))
#accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
#
## Create operation which will initialize all variables
#init = tf.global_variables_initializer()
#
## Configure GPU not to use all memory
#config = tf.ConfigProto()
#config.gpu_options.allow_growth = True
#
#saver = tf.train.Saver()
#
## Start a new tensorflow session and initialize variables
##sess = tf.InteractiveSession(config=config)
#with tf.Session(config=config) as sess:
#    sess.run(init)
#    
#    # This is the main training loop: we train for 50 epochs with a learning rate of 0.05 and another 
#    # 50 epochs with a smaller learning rate of 0.01
#    for learning_rate in [0.05, 0.01]:
#        for epoch in range(50):
#            avg_cost = 0.0
#    
#            # For each epoch, we go through all the samples we have.
#            for i in range(X_train.shape[0]):
#                # Finally, this is where the magic happens: run our optimizer, feed the current example into X and the current target into Y
#                _, c = sess.run([optimizer, loss], feed_dict={lr:learning_rate, 
#                                                              inputs: X_train[i, None],
#                                                              label: y_train[i, None]})
#                avg_cost += c
#            avg_cost /= X_train.shape[0]    
#    
#            # Print the cost in this epcho to the console.
#            if epoch % 10 == 0:
#                print("Epoch: {:3d}    Train Cost: {:.4f}".format(epoch, avg_cost))
#                
#    
#    
#    acc_train = accuracy.eval(feed_dict={inputs: X_train, label: y_train})
#    print("Train accuracy: {:3.2f}%".format(acc_train*100.0))
#    
#    acc_train = accuracy.eval(feed_dict={inputs: X_test, label: y_test})
#    print("Test accuracy: {:3.2f}%".format(acc_train*100.0))
#    
#    save_path = saver.save(sess, "/models/squad/bertqa.ckpt")
#    print("Model saved in path: %s" % save_path)
