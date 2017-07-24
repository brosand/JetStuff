# from vis.losses import ActivationMaximization
# from vis.regularizers import TotalVariation
# from vis.input_modifiers import Jitter
# from vis.optimizer import Optimizer

# from vis.callbacks import GifGenerator

# from keras.utils import plot_model



# plot_model(model, to_file='cnnmodelfile.png')

# # layer_name = 'predictions'
# # output_class=[2]

# # losses = [
# #     (ActivationMaximization(layer_dict[layer_name], output_class),2),
# #     (LPNorm(model.input),10),
# #     (TotalVariation(model.input),10)
# # ]

# # opt = Optimizer(model.input,losses)
# # opt.minimize(max_iter=500,verbose=True,image_modifiers=[Jitter()],callbacks=[GifGenerator('opt_progress')])

from keras.models import load_model
from keras import backend as K
import numpy as np
from scipy.misc import imsave


img_width = 5
img_height = 5

model = load_model('CNNModel.h5')
print('Model loaded.')
layer_dict=dict([(layer.name, layer) for layer in model.layers[1:]])

layer_name='conv2d_3'
filter_index = 2

# build a loss function that maximizes the activation
# of the nth filter of the layer considered

layer_output = layer_dict[layer_name].output
loss = K.mean(layer_output[:,:,:,filter_index])

# we start from a gray image with some noise
input_img_data = np.random.random((1,3,img_width,img_height))*20+128.

#compute the gradient of the input picture wrt this loss
grads = K.gradients(loss,input_img_data)[0]

# normalization trick: we normalize the gradient
a = K.square(grads)
print 'a'
b = K.mean(a)
print 'b'
c = K.sqrt(b)
print 'c'
d /= c
print 'd'
grads /= (K.sqrt(K.mean(K.square(grads))) + 1e-5)


# this function returns the loss and grads given the input picture
iterate = K.function([input_img_data], [loss,grads])


# run gradient ascent for 20 steps
for i in range(20):
    loss_value, grads_value = iterate([input_img_data])
    input_img_data += grads_value * step

def deprocess_image(x):
    # normalize tensor: center on 0., ensure std is 0.1
    x -= x.mean()
    x /= (x.std() + 1e-5)
    x *= 0.1

    # clip to [0, 1]
    x += 0.5
    x = np.clip(x, 0, 1)

    # convert to RGB array
    x *= 255
    x = x.transpose((1, 2, 0))
    x = np.clip(x, 0, 255).astype('uint8')
    return x

img = input_img_data[0]
img = deprocess_image(img)
imsave('%s_filter_%d.png' % (layer_name, filter_index), img)