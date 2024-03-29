---
layout: post
title:  "IoC란 무엇인가"
subtitle:   "Spring Boot - IoC"
categories: study
tags: spring spring-boot IoC
comments: true
# header-img: ""
---

- 목차
	- [IoC](#ioc)
    - [컨테이너](#컨테이너)
    - [스프링 컨테이너의 종류](#스프링-컨테이너의-종류)
    - [IoC와 DI의 관계](#ioc와-di의-관계)

## IoC

IoC를 알아보자. DI와 IoC는 아주 밀접한 관계를 맺고 있기 때문에 하나만 알아서는 안된다! DI도 같이 꼭 세트로 알아두자.

제어의 역전. 프로그램을 제어하는게 원래는 누군지 생각해보자. 바로 프로그래밍을 하는 개발자들이다.

이러한 프로그램의 모든 것들을 개발자가 관리해야한다면? 얼마나 힘들까. 개발자는 **개발**만을 하고싶은 존재다. 프로그램에 대한 모든것을 제어하고 싶지 않다.

이러한 점을 타파하기 위해 제어권을 제 3자에게 위임하는 것이다. 이것이 바로 IoC다.

## 컨테이너

스프링에서는 컨테이너라는 용어가 등장한다. Servlet 컨테이너, EJB 컨테이너등.. 많은 컨테이너들이 있다.

이 컨테이너들은 뭐하는 녀석들인가? 바로 **인스턴스의 생명주기를 관리, 생성된 인스턴스들에게 추가적인 기능을 제공하도록 하는 것**이라고 한다.

 즉, 당신이 작성한 처리과정을 위임받은 독립적인 존재라고 생각하면 된다. 알아서 코드를 참조하여 객체의 생성과 소멸을 컨트롤해주는 것이다.

## 스프링 컨테이너의 종류

### BeanFactory

객체를 생성하고, DI를 처리해주는 기능만을 제공하는 것이다. Bean 등록,생성,조회,반환을 관리한다.
빈 자체가 필요하게 되기 전까지는 인스턴스화를 하지 않는다.
`getBean()`메서드로 Bean을 조회할 수 있지만 잘 사용하지 않는다고 한다.

- 처음으로 getBean()이 호출된 시점에서야 해당 빈을 생성한다. (Lazy Loading)

### ApplicationContext

스프링이 제공하는 다양한 부가 기능을 담고있다. BeanFactory와 유사하지만 좀 더 많은 기능을 제공한다.

BeanFactory에서 추가되는 기능

1. 국제화가 지원되는 텍스트 메시지를 관리해 준다.
2. 이미지같은 파일 자원을 로드할 수 있는 포괄적인 방법을 알려준다.
3. 리스너로 등록된 빈에게 이벤트 발생을 알려준다.
- 컨텍스트 초기화 시점에 모든 싱글톤 빈을 미리 로드한 후 애플리케이션 가동 후에는 Bean을 지연없이 얻을 수 있다. ⇒ 미리 Bean을 생성해 놓아 빈이 필요할 때 즉시 사용할 수 있도록 보장한다.

정리하자면, 컨테이너는 우리의 코드를 읽어서 객체에 대한 정보를 알아둔다. 그리고 이용자가 호출을 하게 된다면 그 때 그에 맞는 객체를 할당해주는 것이다.

 이로 인해 프로그래머는 `프레임워크에 필요한 부품을 개발,조립하는 방식의 개발`만 하면된다. 나머지는 알아서 컨테이너에서 처리해주니깐 말이다.

## IoC와 DI의 관계
![image](https://user-images.githubusercontent.com/22341452/132048110-3213d740-3a3d-46c9-b2e6-b59e25857b59.png)   
스프링 프레임워크의 큰 장점은 IoC컨테이너의 기능이였다. 하지만, IoC는 스프링이 탄생하기 이전부터 사용되던 개념이였다.   
그래서 스프링에서 사용하는 경량 컨테이너들이 이야기하는 IoC를 DI라는 용어로 사용하는 것이 바람직하다고 "마틴 파울러"가 얘기하였다. 개발자마다 다양한 방식으로 분류하고 있으니 이와같이 구분하는 것이 일반적이다.

> 참고   
[https://biggwang.github.io/2019/08/31/Spring/IoC, DI란 무엇일까/](https://biggwang.github.io/2019/08/31/Spring/IoC,%20DI%EB%9E%80%20%EB%AC%B4%EC%97%87%EC%9D%BC%EA%B9%8C/)   
[https://jjunii486.tistory.com/84](https://jjunii486.tistory.com/84)