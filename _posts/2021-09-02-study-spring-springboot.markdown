---
layout: post
title:  "Spring과 Spring Boot의 차이"
subtitle:   "Spring Boot"
categories: study
tags: spring spring boot
comments: true
# header-img: ""
---

- 목차
	- [Spring이란 무엇인가](#spring이란-무엇인가)
    - [SpringBoot는 뭐하는 친구?](#springboot는-뭐하는-친구)

## Spring이란 무엇인가.

스프링의 주요한 특징으로는 **DI(Dependency Injection)**, **IOC(Inversion Of Control)** 이 있다.

위 두가지의 특징으로 인해서 **결합도가 낮은 어플리케이션**을 개발할 수 있다.

⇒ 결합도가 낮으면 기능 추가 및 삭제, 유지보수 단위테스트등 용이하기 때문에 퀄리티 높은 프로그램을 개발할 수 있다.

```java
@RestController
public class MyController {
    private MyService service = new MyService();

    @RequestMapping("/welcome")
    public String welcome() {
        return service.retrieveWelcomeMessage();
    }
}
```

 위의 예제를 보자. MyController는 MyService라는 클래스에 의존한다고 설계를 했다면, 인스턴스를 얻기위해서는 다음과 같이 코드를 작성해야 한다.

 추후에 MyController에 대한 단위 테스트를 진행하기 위해, Mock객체를 생성한다면, 어떻게 MyController가 Mock객체를 이용할 수 있을까?

```java
@Component
public class MyService {
    public String retrieveWelcomeMessage(){
       return "Welcome to Innovation";
    }
}

@RestController
public class MyController {
    @Autowired
    private MyService service;

    @GetMapping("/welcome")
    public String welcome() {
        return service.retrieveWelcomeMessage();
    }
}
```
결합도를 낮추기 위해서는 객체를 분리하고 DI를 사용해야 한다.   
스프링은 위처럼 두 개의 어노테이션(@Component, @Autowired)으로 MyService객체의 인스턴스를 쉽게 얻을 수 있다.

스프링 프레임워크는 이렇게 일을 단순하게 만들기 위한 방법을 제공한다.

> @Component   
스프링의 BeanFactory라는 팩토리 패턴의 구현체에서 bean이라는 스프링프레임워크가 관리하는 객체가 있다. 해당 클래스를 그러한 bean객체로 두어 스프링 관리하에 두겠다는 어노테이션이다.

> @Autowired   
스프링 프레임워크에서 관리하는 Bean객체와 같은 타입의 객체를 찾아서 자동으로 주입해주는 것이다. 해당 객체를 Bean으로 등록하지 않으면 주입해줄 수 없다.

## SpringBoot는 뭐하는 친구?

Transaction Manager, Hibernate Datasource, Entity Manager, Session Factory와 같은 설정을 하는데 많은 어려움이 있다. Spring MVC를 사용하여 기본 프로젝트를 셋팅하는데 개발자에게 너무 많은 시간이 걸렸다.

⇒ 스프링 부트가 나와서 해결해줬다. 자동설정(AutoConfiguration)을 이용하였고, 모든 내부 디펜던시를 관리한다. 개발자가 해야하는건 어플리케이션을 실행할 뿐이다. 미리 설정된 스타터 프로젝트를 제공하는 것이다.

(react create app이랑 비슷한 느낌인가)

저 위에 설정들이 호환되게끔 하기 위해서 우리가 "직접" 버전을 선택해주고 설정해줘야 했다. 하지만 "SpringBoot Starter"라는 것을 도입하여 해결했다.

⇒ 개발자가 Dependency 관리와 호환버전에 대하여 관리할 필요가 없어졌다.

```java
// Web, Restful 응용프로그램
implementation('org.springframework.boot:spring-boot-starter-web')
// Spring Data JPA with Hibernate
implementation('org.springframework.boot:spring-boot-starter-data-jpa')
// Unit Testing, Integration Testing
testImplementation('org.springframework.boot:spring-boot-starter-test')
```

> 참고   
[https://sas-study.tistory.com/274](https://sas-study.tistory.com/274)