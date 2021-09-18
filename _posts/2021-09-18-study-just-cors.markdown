---
layout: post
title:  "CORS에 대해서"
subtitle:   "CORS"
categories: study
tags: 그냥저냥 cors, 통신
comments: true
# header-img: ""
---
- 목차
	- [CORS](#cors)
    - [Origin이란?](#origin이란)
    - [CORS 정책 위반은 어디서 판단할까?](#cors-정책-위반은-어디서-판단할까)
    - [CORS는 어떻게 동작할까?](#cors는-어떻게-동작할까)
    - [CORS 정책 위반 확인의 시나리오들](#cors-정책-위반-확인의-시나리오들)

## CORS

Cross-Origin Resource Sharing의 약자이다.

브라우저는 모든 요청 시 Origin Header를 포함하게 된다.

서버는 Origin Header를 보고, 해당 요청이 원하는 도메인에서부터 출발한 것인지를 판단한다.

다른 Origin에서 온 요청은 서버에서 기본적으로 거부한다.

CORS정책은 서버를 보호하기 위한 정책이다.

## Origin이란?

Origin이란 출처를 의미한다. 출처는 URL에서 뜯어볼 수 있다.

```
https://www.naver.com:80/users?name="jeongGyu"#foo
```

|이름|값|
|---|---|
|**Protocol**| https://
|**Host**|www.naver.com
|**Port**| :80
|**Path**| /users
|**Query String**| ?name="jeongGyu"
|**Fragment**| #foo

여기서 출처는 `Protocol + Host + Port` 를 뜻한다.

포트번호는 http, https에서는 정해져있기 때문에 생략가능하다. 하지만 포트번호가 명시적으로 포함되어 있다면 포트번호까지 일치해야 같은 출처로 인정이 된다.

⇒ 포트번호까지 일치여부는 각 브라우저마다 다르다. Internet Explorer는 포트번호를 무시한다.

## CORS 정책 위반은 어디서 판단할까?

CORS 정책은 "브라우저"에서 판단한다. 서버에서는 판단하지 않는다.

⇒ 그러면 데이터를 요청하는 것을 할 수 있다는 얘기 아닌가? 그렇게 되면 서버에 과부하가 걸리는게 아닌가?   
 밑에 통신 시나리오에 대해서 서술할때 보자.

## CORS는 어떻게 동작할까?

1.  웹 클라이언트 어플리케이션이 다른 출처의 리소스를 요청할 때는 HTTP 프로토콜을 사용하여 요청을 보내게 된다. 이 때 브라우저는 `요청 Header`에 `Origin` 이라는 필드에 요청을 보내는 "출처"를 함께 담아보낸다.
2.  서버에서는 해당 요청을 받고 `응답 Header`에 `Access-Control-Allow-Origin` 이라는 필드에 "이 리소스에 접근 가능한 출처들"을 내려준다.
3.  응답을 받은 브라우저는 자신이 보냈던 `요청 Header`의 `Origin`필드 값과 `응답 Header`의 `Access-Control-Allow-Origin`의 값을 비교하여 유효한지 판단한다.

## CORS 정책 위반 확인의 시나리오들

### 1. Preflight Request

- 동작 과정
    1. 브라우저가 서버에게 "본 요청"을 보내기 전에 "예비 요청"을 보낸다. 이를 preflight라고 부른다.   
    이 예비 요청에는 HTTP 메소드중 `OPTIONS` 메소드가 사용된다.
    2. 서버에서 `Access-Control-Allow-Origin` 을 응답한다.
    3. 비교한 뒤, 가능하다면 본 요청을 진행한다. 아니라면 CORS 정책 위반으로 끝을 낸다.

### 2. Simple Request

- 동작 과정
    1. 브라우저는 서버에게 "본 요청"에 해당하는 걸 바로 보낸다.
    2. 서버에서 그에 대한 리소스와 `Access-Control-Allow-Origin` 을 응답한다.
    3. 비교한 뒤, 가능하다면 본 요청을 진행한다. 아니라면 CORS 정책 위반으로 끝을 낸다.

    특수한 조건을 만족해야만 위 과정이 가능하다. 예비 요청을 생락할 수 있는 조건들은 다음과 같다.

    - Request Method는 `GET, HEAD, POST`중 하나여야 한다.
    - `Accept`, `Accept-Language`, `Content-Language`, `Content-Type`, `DPR`, `Downlink`, `Save-Data`,`ViewPort-Width`, `Width`를 제외한 헤더를 사용하면 안된다.
    - 만약 `Content-Type`을 사용하는 경우에는 `application/x-www-form-urlencoded`, `multipart/form-data`, `text/plain`만 허용된다.

### 3. Credentialed Request

- 동작 과정   
    Preflight Request과정과 같다. 
- 추가된 부분

    `Credentials`라는 속성을 같이 보낸다. 보낼 때, `Access-Control-Allow-Origin: *` 을 서버에서 설정해주면 안되고, 응답 헤더에는 `Access-Control-Allow-Credentials: true` 가 존재해야한다.

    `Credentials` 에는 3가지 옵션이 존재한다.

    |옵션명|설명|
    |---|---|
    |same-origin| 같은 출처 간 요청에만 인증 정보를 담을 수 있다.
    |include| 모든 요청에 인증 정보를 담을 수 있다.
    |omit| 모든 요청에 인증 정보를 담지 않는다.

     `Credentials: 'include'`이 값을 설정한 뒤 브라우저가 서버에게 요청을 한다면, 브라우저는 인증 정보들이 담겨져 있는 "쿠키 정보"를 함께 담아서 보낸다.

    그러면 서버에서 허용된 인증정보를 브라우저에게 보내고, 브라우저는 이를 판단하고 통신하게 된다.

> 출처   
[https://evan-moon.github.io/2020/05/21/about-cors/](https://evan-moon.github.io/2020/05/21/about-cors/)