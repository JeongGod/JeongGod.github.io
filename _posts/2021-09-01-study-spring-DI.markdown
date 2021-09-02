---
layout: post
title:  "DI란 무엇인가"
subtitle:   "Spring Boot - DI"
categories: study
tags: spring spring-boot DI
comments: true
# header-img: ""
---
## 개요
> 테스트
  
- 목차
	- [DI (Dependency Injection)](#di-dependency-injection)
    - [Spring과 DI](#spring과-di)

## DI (Dependency Injection)
DI란 무엇인가. Dependency Injection의 줄임말로 의존성 주입이라고 한다.

> 의존성    
어떤 "서비스"를 호출하려는 그 "클라이언트"는 그 "서비스"가 어떻게 구성되었는지 알지 못해야 한다.   
"클라이언트"는 대신 서비스 제공에 대한 책임을 외부 코드(주입자)로부터 위임한다.   
"클라이언트"는 주입자 코드를 호출할 수 없다.   
그 다음, 주입자는 이미 존재하거나 주입자에 의해 구성되었을 서비스를 클라이언트로 주입(전달)한다.
그러고 나서 클라이언트는 서비스를 이용한다.   
이는 클라이언트가 주입자와 서비스 구성 방식 또는 사용중인 실제 서비스에 대해 알 필요가 없음을 의미한다.   
"클라이언트" : 서비스의 사용 방식을 정의하고 있는 서비스의 고유한 인터페이스에 대해서만 알면 된다.   
`구성의 책임`으로부터 `사용의 책임`을 구분한다.

### DI 사용 X

```java
public class Coffee {...}

public class Programmer {
	private Coffee coffee = new Coffee();

	public startProgramming(){
		this.coffee.drink()
	}
}
```

여기서 Programmer객체는 Coffee객체가 필요해서 Coffee객체를 생성했다.   
Programmer객체는  Coffee객체에 의존하고 있다. 라고 설명할 수 있다.

만약, Coffee객체가 아닌 Cappuccino, Americano객체를 사용하고 싶다면 해당 코드는 수정해야 한다.   
결합도(coupling)이 높아지게 되어 코드의 재활용성등 문제가 많아진다.

### DI 사용

```java
public class Coffee {...}
public class Cappuccino extends Coffee {...}
public class Americano extends Coffee {...}

public class Programmer {
	private Coffee coffee;

	public Programmer(Coffee coffee){
		this.coffee = coffee
	}

	public startProgramming(){
		this.coffee.drink()
	}
}
```

이 코드를 보면 Programmer객체에 Coffee라는 객체를 "주입"해주는 것을 알 수 있다.   
이렇게 함으로서 Programmer객체가 Cappuccino를 마시는 중이라면, Cappuccino객체를 Programmer에 넘겨주어 생성하면 된다. Americano를 마시고 싶다면 똑같이 하면 된다! 코드를 계속해서 재사용할 수 있게 되는 것이다.

---

여기서 부터 객체지향개발론에서 배웠던 내용이 생각나 뒤적여봤다.

상속 모델들은 "is a" relationship을 가진다고 했다. 위 예시를 살펴보면

> Coffee is a Coffee   
Cappuccino is a Coffee   
Americano is a Coffee   

 그래서, Transitivity가 성립이 된다.    
 만약 Cat → Mammal, Mammal → Animal이라면, Cat → Animal이 성립된다는 말이다.

이 얘기를 왜 했냐면 저기 Coffee coffee객체에 Cappuccino, Americano객체가 들어갈 수 있다는 설명을 하려고 했다. 바로 LSP(Liskov Substitution Principle)으로 인해서 
`Coffee coffee = new Americano();` 가 성립하게 된다.

---

DI를 사용함으로서의 장점

1. Unit Test가 용이해진다. ⇒ 의존성이 낮아지니깐
2. 코드의 재활용성이 높아진다. ⇒ 하나의 객체에 의존하지 않으니깐
3. 객체 간의 의존성(종속성)을 줄이거나 없앨 수 있다.
4. 객체 간의 결합도를 낮추면서 유연한 코드를 작성할 수 있다.

## Spring과 DI

Spring 프레임워크는 DI를 사용하는데 편하게 해준다. 방법은 총 3가지가 있다.

#### 1. 생성자 주입(Constructor Injection)

```java
@Service 
public class UserServiceImpl implements UserService {   
    private UserRepository userRepository; 
    private MemberService memberService; 
    @Autowired 
    public UserServiceImpl(UserRepository userRepository, 
														MemberService memberService) { 
        this.userRepository = userRepository; 
				this.memberService = memberService; 
    } 
}

// 출처: https://mangkyu.tistory.com/125 [MangKyu's Diary]
```

생성자 주입은 생성자의 호출 시점에 "1회" 호출 되는 것이 보장된다.

그렇기 때문에 `주입받는 객체의 변화가 없거나 반드시 객체의 주입이 필요한 경우`에 강제하기 위해 사용이 가능하다.

스프링에서는 생성자가 1개만 있을 경우에는 `@Autowired` 는 생략 가능하다. 그래서 아래와 같이 변경이 가능하다.

```java
@Service 
public class UserServiceImpl implements UserService {   
    private UserRepository userRepository; 
    private MemberService memberService; 

    public UserServiceImpl(UserRepository userRepository, 
														MemberService memberService) { 
        this.userRepository = userRepository; 
				this.memberService = memberService; 
    } 
}

// 출처: https://mangkyu.tistory.com/125 [MangKyu's Diary]
```

---

#### 2. 수정자 주입(Setter Injection)

Setter를 이용하여 의존 관계를 주입하는 방법이다. `주입받는 객체가 변할 수 있는 경우`에 사용한다.

```java
@Service 
public class UserServiceImpl implements UserService { 
    private UserRepository userRepository; 
    private MemberService memberService; 
    @Autowired 
    public void setUserRepository(UserRepository userRepository) { 
        this.userRepository = userRepository; 
    } 
    @Autowired 
    public void setMemberService(MemberService memberService) { 
        this.memberService = memberService; 
    } 
}

// 출처: https://mangkyu.tistory.com/125 [MangKyu's Diary]
```

만일 `@Autowired` 로 주입할 대상이 없는 경우에는 오류가 발생한다. ⇒ 빈에 존재하지 않는 경우

주입할 대상이 없도록 하려면 `@Autowired(required = false)` 를 통해 설정이 가능하다.

---

#### 3. 필드 주입(Field Injection)

필드에 바로 의존 관계를 주입하는 방법이다.

```java
@Service 
public class UserServiceImpl implements UserService { 
		@Autowired
    private UserRepository userRepository; 
		@Autowired
    private MemberService memberService; 
}
```

코드가 간결해져서 과거에 많이 이용된 방법이다. 하지만, 위 방법은 외부에서 변경이 불가능하다.

테스트 코드에서 Mock데이터를 사용하여 주입하게되면 안된다는 말이다.

또, 필드 주입은 DI 프레임워크(스프링같은)가 존재해야지만 사용이 가능하다. 그래서 반드시 사용을 지양해야한다. ⇒ **어플리케이션의 작동과 무관한 테스트 코드나 설정을 위해서만 사용하자.**

---

위 3가지 방법중 우리는 **생성자 주입**을 권장한다. 그 이유는 다음과 같다.

1. 객체의 불변성 확보
2. 테스트 코드의 작성
3. final 키워드 작성 및 Lombok의 결합

    위 3가지 방법중 생성자 주입만이 객체의 생성과 "동시에" 의존성 주입이 이루어진다. 그래서 final변수를 할당 할 수 있다. 나머지 방법은 객체의 생성 ⇒ 의존성 주입 함수 호출로 이루어지기에 final변수를 할당 할 수 없다.

4. 순환 참조 에러 방지

    아까 말했다싶이, 객체의 생성과 "동시에" 의존성 주입이 이루어진다. 
    클라이언트 구동시, Bean에 등록하기 위해 객체를 생성하는데 이 때 순환참조를 찾으면 바로 에러를 내뱉는다. 만약 수정자 주입을 사용했다면 `해당 객체를 사용하기 위해 의존성을 주입했을 경우` 에러가 나서 처음에는 뭣도 모르다가 나중에 발견할 수도 있는 경우가 생긴다.

    이를 방지하기 위해서 생성자 참조를 사용해야 한다.

> 참고   
[https://velog.io/@wlsdud2194/what-is-di](https://velog.io/@wlsdud2194/what-is-di)    
[https://mangkyu.tistory.com/125](https://mangkyu.tistory.com/125)    
[https://keichee.tistory.com/446](https://keichee.tistory.com/446)