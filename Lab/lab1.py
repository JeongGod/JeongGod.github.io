import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
# Dataset loading
mnist = input_data.read_data_sets("./samples/MNIST_data/", one_hot=True) #55000개의 학습데이터, 10000개의 테스트데이터, 5000개의 검증데이터 다운


# Set up model
x = tf.placeholder(tf.float32, [None, 784]) #심볼릭 변수들을 사용하여 상호작용하는 작업들을 기술합니다.
W = tf.Variable(tf.zeros([784, 10]))
b = tf.Variable(tf.zeros([10])) #리는 MNIST 이미지들의 어떤 숫자들이든 입력할 수 있기를 원하는데, 각 이미지들은 784차원의 벡터로 단조화되어 있습니다. 우리는 이걸 [None, 784] 형태의 부정소숫점으로 이루어진 2차원 텐서로 표현합니다. 그러나 TensorFlow는 더 나은 방법을 갖고 있습니다: Variable이죠. Variable은 TensorFlow의 상호작용하는 작업 그래프들간에 유지되는 변경 가능한 텐서입니다.
y = tf.nn.softmax(tf.matmul(x, W) + b) #W의 형태가 [784, 10] 임을 주의합시다. 우리는 784차원의 이미지 벡터를 곱하여 10차원 벡터의 증거를 만들것이기 때문입니다. bb는 [10]의 형태이므로 출력에 더할 수 있습니다

y_ = tf.placeholder(tf.float32, [None, 10]) #교차 엔트로피를 구현하기 위해 우리는 우선적으로 정답을 입력하기 위한 새 placeholder를 추가해야 합니다:

cross_entropy = -tf.reduce_sum(y_*tf.log(y)) #그 다음 교차 엔트로피 −∑y′log(y)−∑y′log⁡(y) 를 구현할 수 있습니다.
train_step = tf.train.GradientDescentOptimizer(0.01).minimize(cross_entropy) #TensorFlow는 당신 계산 과정의 전체 그래프를 알고 있기 때문에, 자동적으로 역전파(backpropagation) 알고리즘을 이용하여 비용 최소화에 어떤 변수가 얼마나 영향을 주는지를 효율적으로 계산합니다. 그리고 당신이 선택한 최적화 알고리즘을 적용하여 변수들을 수정하고 비용을 최소화할 수 있습니다.

# Session
init = tf.initialize_all_variables() #실행 전 마지막으로 우리가 만든 변수들을 초기화하는 작업을 추가해야 합니다

sess = tf.Session()
sess.run(init) #이제 세션에서 모델을 시작하고 변수들을 초기화하는 작업을 실행할 수 있습니다.

# Learning
for i in range(1000):
  batch_xs, batch_ys = mnist.train.next_batch(100)
  sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys})

# Validation
correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(y_,1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

# Result should be approximately 91%.
print(sess.run(accuracy, feed_dict={x: mnist.test.images, y_: mnist.test.labels}))
