#this is to follow along with tutorial

import tensorflow as tf

x1 = tf.constant(5)
x2 = tf.constant(6)

#result = x1*x2
result = tf.mul(x1, x2) 
#use matmul for matrix
print(result)

"""sess = tf.Session() #gives session variable
print(sess.run(result)) #runs session
sess.close()"""
 #this way you don't have to remember to close the session
with tf.Session() as sess:
    output = sess.run(result)
    print(output)
    #print(sess.run(result))
