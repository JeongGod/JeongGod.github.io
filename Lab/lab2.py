from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets('./samples/MNIST_data', one_hot=True)
#mnist는 NumPy 배열의 형태로 훈련, 검증 및 테스트를 저장하는 가벼운 클래스입니다. 또한 아래에서 사용할, 데이터 미니배치들을 따라가며 반복하는 함수를 제공합니다.
import tensorflow as tf

sess = tf.InteractiveSession() #당신이 TensorFlow로 코드를 설계하는 방법을 훨씬 유연하게 만들어 줍니다.
x = tf.placeholder(tf.float32, shape=[None, 784])
y_ = tf.placeholder(tf.float32, shape=[None, 10])
#x 와 y_는 특정한 값이 아닙니다. 실은 그것들은 placeholder -- 우리가 TensorFlow 에게 계산을 실행할 때 입력할 값들 — 입니다. placeholder의 형태 인수는 선택 사항입니다만, TensorFlow가 자동으로 잘못된 텐서 형태에 대한 오류를 잡을 수 있도록 해줍니다.
W = tf.Variable(tf.zeros([784,10]))
b = tf.Variable(tf.zeros([10]))
#W와 b 둘 모두 0으로 채워진 텐서로 초기화했습니다. W는 784x10 행렬 (우리가 784개의 입력 특징(이미지의 픽셀수)과 10개의 출력이 있으므로) 이며, b는 10차원 벡터입니다. (10개의 클래스가 있으니까요)

sess.run(tf.initialize_all_variables()) #Variables가 세션 안에서 사용되기 전에 반드시 그 세션을 사용하여 초기화되어야 합니다.
y = tf.nn.softmax(tf.matmul(x,W) + b)
#벡터화된 입력 이미지 x를 가중치 행렬 W로 곱하고, 편향(bias) b를 더한 다음 각 클래스에 지정된 소프트맥스 확률들을 계산합니다.
def weight_variable(shape): #가중치 초기화
  initial = tf.truncated_normal(shape, stddev=0.1)
  return tf.Variable(initial)

def bias_variable(shape): #가중치 초기화
  initial = tf.constant(0.1, shape=shape)
  return tf.Variable(initial)

def conv2d(x, W): #합성곱과 풀링
  return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')

def max_pool_2x2(x): #합성곱과 풀링
  return tf.nn.max_pool(x, ksize=[1, 2, 2, 1],
                        strides=[1, 2, 2, 1], padding='SAME')

W_conv1 = weight_variable([5, 5, 1, 32])
b_conv1 = bias_variable([32])
#첫 합성곱 레이어

x_image = tf.reshape(x, [-1,28,28,1])
#x_image를 가중치 텐서와 합성곱
h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1)
h_pool1 = max_pool_2x2(h_conv1)
#편향을 더한 후, ReLU 함수를 적용한 후, 마지막으로 max pool
# Second layer
W_conv2 = weight_variable([5, 5, 32, 64])
b_conv2 = bias_variable([64])

h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)
h_pool2 = max_pool_2x2(h_conv2)

# Densely Connected Layer

W_fc1 = weight_variable([7 * 7 * 64, 1024])
b_fc1 = bias_variable([1024])

h_pool2_flat = tf.reshape(h_pool2, [-1, 7*7*64])
h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)
#전체 이미지를 처리할 수 있도록 1024개 뉴런이 있는 전부 연결된 레이어를 추가합니다. 풀링 레이어로부터의 텐서를 벡터들의 배치로 형태를 바꾸고, 가중치 행렬을 곱하고, 편향을 더하고, ReLU를 적용합니다.
# Dropout
keep_prob = tf.placeholder(tf.float32)
h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)
#탈락
# Readout layer
W_fc2 = weight_variable([1024, 10])
b_fc2 = bias_variable([10])

y_conv=tf.nn.softmax(tf.matmul(h_fc1_drop, W_fc2) + b_fc2)
#판독 레이어
# Train and Evaluate the Model

cross_entropy = -tf.reduce_sum(y_*tf.log(y_conv)) #tf.reduce_sum 는 미니배치 안의 모든 이미지들에 걸쳐 합을 구할 뿐 아니라 클래스에 대해 수행됩니다. 우리는 교차 엔트로피를 전체 미니배치에 대해 계산하고 있습니다.
train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy) #이 한 줄에서 TensorFlow가 진짜로 하는 일은 계산 그래프에 새 작업을 추가하는 일입니다.
correct_prediction = tf.equal(tf.argmax(y_conv,1), tf.argmax(y_,1)) #우리가 맞는 라벨을 예측했는지를 확인할 것입니다. tf.argmax는 특정한 축을 따라 가장 큰 원소의 색인을 알려주는 함수입니다.
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32)) #부울 리스트를 줍니다. 얼마나 많은 비율로 맞았는지 확인하려면, 부정소숫점으로 캐스팅한 후 평균값을 구하면 됩니다.
sess.run(tf.initialize_all_variables())
for i in range(20000): #각 훈련 반복에서 우리는 50개의 훈련 예제를 불러옵니다. 그 다음 feed_dict 를 사용하여 placeholder 텐서 x 와 y_ 를 훈련 예제로 변경한 후 train_step 작업을 실행합니다.
  batch = mnist.train.next_batch(50)
  if i%100 == 0:
    train_accuracy = accuracy.eval(feed_dict={
        x:batch[0], y_: batch[1], keep_prob: 1.0})
    print("step %d, training accuracy %g"%(i, train_accuracy))
  train_step.run(feed_dict={x: batch[0], y_: batch[1], keep_prob: 0.5})

print("test accuracy %g"%accuracy.eval(feed_dict={ #마지막으로, 테스트 데이터를 대상으로 정확도를 확인해 볼 수 있습니다
    x: mnist.test.images, y_: mnist.test.labels, keep_prob: 1.0}))
