---
layout: post
title:  "Tim Sort는 무엇인가"
subtitle:   "Tim Sort"
categories: study
tags: algorithm, sort, tim sort
comments: true
# header-img: ""
---

- 목차
    - [Tim Sort란](#tim-sort)
        - [Insertion Sort](#insertion-sort)
        - [Merge Sort](#merge-sort)
    - [Tim Sort의 최적화](#tim-sort의-최적화)
    - [정리](#정리)

최근 알고리즘 스터디를 진행하다가 python에서 sorted함수에 인자로 `cmp_to_key` 라는 것이 있다는 것을 알았다.

매번 `key` 인자로 sort를 커스텀하다가, 좀 더 세분화하게 커스텀을 할 수 있는 함수를 보고 공식문서를 참조하여 공부해봤다.

> [https://docs.python.org/3/howto/sorting.html](https://docs.python.org/3/howto/sorting.html)

이 공식문서를 보면 두 개의 인자가 들어간다. 인자는 다음과 같이 쓰면 정렬을 할 수 있다.

```python
def mycmp(x, y):
	return x-y # 오름차순

def mycmp(x,y):
	return y-x # 내림차순

sorted(_list, key=cmp_to_key(mycmp))
```

하지만 저 두 개의 인자는 어떻게 쓰이나.. 대체 뭐길래 정렬을 해주는 인자로 쓰이는지 궁금했다.

그래서 x, y를 프린트해봤다.

```python
def mycmp2(a, b):
    print("comparing ", a, " and ", b)
    return a - b
print(sorted([10, 13, 9, 15, 18, 21, 13, 8, 5, 11, 3], key=functools.cmp_to_key(mycmp2)))
```

![image](https://user-images.githubusercontent.com/22341452/132838129-885435d1-d028-4b8d-aab9-47ce7f3e40ab.png)

 다음과 같이 나오는 것을 볼 수  있다. 

하나하나 리스트에 담으면서 직접 비교해보면 binary search형태로 비교하는 것을 알 수 있다. 왠 갑자기 binary search인지는 Python에서 제공하는 `sort` , `sorted` 함수가 무슨 알고리즘을 사용하는지 알아봐야 한다.

바로 `Tim Sort`다.

## Tim Sort

Tim Sort란 Merge Sort + Insertion Sort를 최적화한 sorting 알고리즘이다.

먼저, Insertion Sort에 대해서 알아보자.

### Insertion Sort

```python
def insertionSort(arr):
    for i in range(0, len(arr)-1):
        j = i
        while j > left and arr[j] < arr[j - 1]:
            arr[j], arr[j - 1] = arr[j - 1], arr[j]
            j -= 1
```

다음과 같이 작동하는 알고리즘이다. sort를 할 시에 "주변에 인접한" 값을 비교하여 sort하는 방식으로 **참조 지역성**이 좋다는 것을 알게 된다.

> 참조 지역성이란
CPU가 캐시 메모리에 현재 리스트에 인접한 데이터들을 담아놓는다. 그 이유는 대부분 리스트를 참조할 경우 순서대로 읽어오는 경우가 많다. 그래서 CPU는 사용자가 다음에 이 메모리들을 읽겠지? 하고 미리 캐시 메모리에 인접한 데이터를 담아놓고 좀 더 빠른 속도를 제공한다.
하지만, 리스트에서 무작위로 데이터를 읽을 경우에는 캐시 메모리에 없으므로, 읽어오는데 속도 차이가 난다.

 이 참조 지역성원리에 따라서, Insertion Sort는 arr의 크기가 작은 경우에는 O(n^2)임에도 불구하고 빠른 속도를 보여준다. 
 Insertion Sort는 완전 역순일 경우(Worst case)에만 O(n^2)의 시간복잡도가 걸리지만 완전 정렬된 데이터에서는 O(n)으로 준수한 속도를 보여준다. ⇒ 이 점은 실생활 데이터에서 유용하다. 실생활 데이터는 어느정도 정렬되어 있는 확률이 높기 때문이다.

### Merge Sort

Merge Sort는 모든 arr를 하나의 단위로 쪼갠 뒤, 점점 합쳐나가면서 정렬하는 방식이다. 또, 합쳐나가면서 정렬된 데이터를 담을 arr가 필요하기 때문에 공간복잡도는 O(n)이다.
정렬된 데이터가 들어온다 하더라도 앞서 말한 방식을 진행한다. 그렇기 때문에 worst든 best든 O(nlogn)을 만족한다.

 정렬되어있는 데이터를 쪼갤 필요가 있을까? 아니다. 정렬된 데이터는 냅두는게 최적화된 방식이다. 

## Tim Sort의 최적화

Tim Sort는 어떻게 최적화 했을까?

### **1. Run**

Tim sort는 Merge sort처럼 하나의 단위로 쪼개지 않고, Run단위로 쪼갠다. Run의 길이는 대체로 2^5 ~ 2^6 사이의 값이다.

해당 Run단위의 배열들은 **정렬**되어 있는 상태여야한다. 정렬은 어떻게 진행하냐? 바로 `Insertion Sort` 방식이다. 앞서 말했듯이 길이가 작다면 `Insertion Sort` 가 효율적이라고 말했다.

그런데, 오름차순으로만 Run을 정렬해야 하는가? 그건 또 아니다.

Run단위로 자를때, arr[0] 와 arr[1]을 먼저 비교한다.

- arr[0] > arr[1]이라면, 내림차순으로 정렬한다.
arr[0] > arr[1] > arr[2] > ... > arr[n]
- arr[0] ≤ arr[1]이라면, 오름차순으로 정렬한다.
arr[0] ≤ arr[1] ≤ arr[2] ≤ ... ≤ arr[n]

그런 다음에 내림차순으로 되어있는 Run들을 오름차순으로 만들어준다.

왜 앞 선 2개를 비교한 뒤에 진행할까.. 그게 궁금했다. 아마 나의 생각으로는 이제 말 할 `Binary Insertion Sort`와 관계가 있어보인다.

### **2. Binary Insertion Sort**

`Binary Insertion Sort`란, Binary Search를 이용해 Insertion할 위치를 찾는 것이다. Binary Search를 하기 위해서는 "정렬된 데이터"에서만 가능하다. 

그렇기 때문에 앞서 말한 arr[0]와 arr[1]를 무조건 정렬된 데이터라고 생각하고 정렬을 진행한다.

위 생각으로 미리 앞 선 2개를 비교한다고 생각했다.. 아니라면 말씀부탁드립니다!

여튼, `Binary Insertion Sort`는 하나의 데이터를 집어넣을 때 마다 O(logn)으로 위치를 찾고, O(n)으로 쉬프트 연산을 통해 데이터를 shift합니다. 

⇒ 그러면 결국 O(n^2)가 걸리는게 아니냐? 하겠지만 쉬프트 연산은 그렇게 오래 걸리지 않기 때문에 더 빠르다.

### **3. Merge Sort**

Merge Sort하는데 위에서 말한 최적화가 가능한 부분이 2가지가 있었다.

1. 하나의 단위로 merge를 하는게 아닌 Run단위로 merge를 진행한다.
2. 공간복잡도 O(n)을 줄인다

먼저 **하나의 단위로 merge를 하는게 아닌 Run단위로 merge를 진행한다.** 의 최적화 방법을 보자.

#### **1. Run단위로 Merge**

비슷한 길이의 배열 두 개를 merge하는 것이 최적의 효율이다. 그 이유는 다음과 같다.

만약 길이가 다음과 같이 주어진 데이터를 merge하려고 한다면

- 길이를 비교하지 않고 하는 경우
(1,50) (2,100) ⇒ 최대 50번, 100번 비교
- 비슷한 길이와 하는 경우
worst case인 경우 
(1,2) (50,100) ⇒ 최대 2번, 100번 비교

이 처럼 비슷한 길이끼리 merge하는것이 이득이다. 그러면 어떻게 비슷한 길이의 Run을 합칠 수 있을까?

바로 `stack` 을 이용한다.

stack에다가 Run 하나를 집어넣을 때 마다 아래와 같은 식을 만족하는지 판단한다. 만족한다면 그대로 `stack`에 쌓고 아니라면 merge한다.

- stack[i] < stack[i+1]
- stack[i] + stack[i+1] < stack[i+2]

이러한 궁금증이 생길 수도 있다. stack을 사용한다면 공간 복잡도가 커지는게 아닌가? 답은 아니다. 이유는 2번식을 보면 알 수 있다. 2번 식은 피보나치 수열과 비슷하다.
stack의 크기는 결국 위의 식들이 만족하지 않고 계속 쌓이는 경우에 커지는 것인데 그렇다는 것은 stack의 맨 밑바닥 부분이 2번 식을 만족한다는 것이다.

그렇다면 맨 마지막의 크기는 스택의 크기가 m이라면 Run의 길이는 2^m이 될것이다. 결국 Run의 길이가 N이라면 스택의 크기는 최대 logN이 되기 때문에  걱정할 필요가 없다.

#### **2. 공간복잡도 줄이기**

Tim Sort에서는 모든 arr와 똑같은 크기를 복사하지 않고 Merge할 Run중에서 길이가 작은 Run만 복사를 하는 방식을 선택했다.

[2,6,11], [1,5,8,9,10]  의 Run 2개가 있다고 해보자.

여기서 Run의 크기가 작은 [2,6,11]의 배열을 복사한다. 그런 다음

[2,6,11 | 1,5,8,9,10 ] 에서 각각의 원소와 비교하는 것이다. 
아래는 비교하는 형식이다.

[2, 6, 11, ~~`1`~~, 5, 8, 9, 10]  [`2`, 6, 11]   

[`1`, 6, 11, 1, `5`, 8, 9, 10] [~~`2`~~, 6, 11]

[1, `2`, 11, 1, ~~`5`~~, 8, 9, 10] [2, `6`, 11]

[1, 2, `5` ,1, 5, `8`, 9, 10] [2, ~~`6`~~, 11]

[1, 2, 5, `6`, 5, ~~`8`~~, 9, 10] [2, 6, `11`]

[1, 2, 5, 6, `8`, 8, ~~`9`~~, 10] [2, 6, `11`]

...

로 진행이 된다. 

그래서 Run이 작은 부분만 복사하여 사용하므로 n개 대신, 2/n 개로 줄어든다.

#### **3. Merge하는 부분 줄이기.**

Run과 Run끼리 Merge할 시에 모든 Run과 Run을 다 비교하는것은 비효율적이여서 최적화를 한 것이다.

[2,6,7], [5,8,9,10]  을 merge한다고 해보자. 

[2,6,7]에서 `7` 보다 큰 부분은 볼 필요가 없다. 그래서 오른쪽 [`5`]와 비교만 하면 된다.

[5,8,9,10] 에선 `5` 보다 작은 부분은 볼 필요가 없다. 그래서 왼쪽 [`6`, `7`]와 비교만 하면된다.

그렇다면 [~~2~~, 6 ; 7, 5, ~~8~~, ~~9~~, ~~10~~] 이렇게 비교만 한다면 비교횟수를 줄일 수 있다. 이 부분을 찾는 과정은 Binary Search로 찾게된다.

#### **4. Galloping Search**

이제 Run과 Run을 비교한다고 해보자. 이 때, 원소의 크기차이가 커서 하나하나 비교하기엔 불필요한 비교라고 생각하는 것이다. 이 때 "질주 모드"라고 해서 1칸씩 비교하는 것이 아닌 2^n만큼 건너뛰면서 비교하게 된다.

이 때, 시간복잡도는 O(logn)으로 된다. 그렇다면 Binary Search로 찾으면 되지 굳이 Galloping Search로 찾을까?

Galloping Search를 사용함으로써 이득은 바로 Best Case일 경우가 있다. 만약 비교적 앞에 현재 target이 있다면 Galloping Search로 찾는게 낫다. Binary Search는 "항상" logn을 사용하여 위치를 찾기 때문에 좀 더 효율적인 Galloping Search를 하는 것이다.

Tim Sort에서는 처음부터 Galloping Search로 찾지 않고, 처음 3개의 원소와 비교했을 때 찾지 못 했다면 Galloping Mode로 들어가서 찾게 된다.

## 정리

이렇게 Tim Sort는 Merge Sort + Insertion Sort를 통해 best case : O(n), Worst Case : O(nlogn)으로 최적화를 시켰다. 

이 알고리즘은 실생활 데이터에 쓰이는데 매우 효율적이다. 우리의 실생활 데이터들은 무작위 랜덤 데이터들도 있겠지만 약간의 정렬은 되어있는 상태가 많다. 이럴때 Tim Sort는 힘을 발휘한다.

Python, Java SE 7, Android, Google chrome (V8), Swift언어가 이러한 Tim sort알고리즘을 통해 구현이 되어있다. 알아두면 좋을 알고리즘인 것 같다.

> 참고
[https://d2.naver.com/helloworld/0315536](https://d2.naver.com/helloworld/0315536)
[https://orchistro.tistory.com/175](https://orchistro.tistory.com/175)
[https://www.youtube.com/watch?v=2pjUsuHTqHc&list=LL&index=1&ab_channel=Chan-SuShin](https://www.youtube.com/watch?v=2pjUsuHTqHc&list=LL&index=1&ab_channel=Chan-SuShin)
[https://thedevmatt.wordpress.com/2016/08/09/should-i-use-binary-or-galloping-search/](https://thedevmatt.wordpress.com/2016/08/09/should-i-use-binary-or-galloping-search/)