---
layout: post
title:  "API와 REST API에 대해서"
subtitle:   "API와 REST API"
categories: study
tags: 그냥저냥 api rest-api, restful
comments: true
# header-img: ""
---
- 목차
    - [API란](#api란)
    - [REST API](#rest-api)
        - [REST API설계 가이드](#rest-api설계-가이드)
            1. [URL Rules](#1-url-rules)
            2. [Set HTTP Headers](#2-set-http-headers)
            3. [HTTP Methods](#3-http-methods)
            4. [HTTP Status](#4-http-status)
            5. [Correct Status Code](#5-correct-status-code)
            6. [Use HATEOAS](#6-use-hateoas)
            7. [Sort, Filter](#7-sort-filter)
            8. [Versioning](#8-versioning)


# API란

API(Application Programming Interface)의 약자이다.

> 응용 프로그램에서 사용할 수 있도록, 운영 체제나 프로그래밍 언어 제공하는 기능을 제어할 수 있게 만든 인터페이스를 뜻한다. - 위키백과

응용 프로그램끼리 데이터를 주고 받기 위한 방법인 것이다. 

식당(응용 프로그램), 식당 메뉴판(식당의 API), 고객(응용 프로그램)   
고객이 식당에게 무슨 데이터를 요청하기 위해서는 API를 통해 요청해야지 원하는 데이터를 얻을 수 있다. 만약 API에 존재하지 않는 요청을 한다면 식당은 데이터를 줄 수 없다.

# REST API

REST(REpresentational State Transfer)의 약자로 웹상에서 사용되는 여러 리소스를 HTTP URI로 표현하고, 해당 리소스에 대한 행위를 HTTP Method로 정의하는 방식을 말한다.

## REST API 설계 가이드

### 1. URL Rules

1. 리소스에 대한 행위는 HTTP Method(POST, GET, PUT, DELETE)등을 이용한다.
2. /(슬래시)는 계층 관계를 나타낸다.
3. URI에 _(underbar)를 사용하지 않는다. 영어 대문자보다는 소문자를 사용한다.
4. URI에 동사는 사용하지 않는다. 명사를 사용한다
5. URI에 파일의 확장자(.json, jpeg)등을 포함하지 않는다.

### 2. Set HTTP Headers

1. Content-Location   
GET, PUT등 요청의 응답값은 idempotent(멱등 법칙 즉, input값이 같다면 output도 무조건 같다.)하다.    
POST 요청의 응답값은 매번 다르다. 그래서 새로 생성한 리소스를 식별하기 위해  `Content-Location`을 사용한다.
2. Content-Type   
`application/json` 을 사용한다! 되도록이면 포맷을 통일시킨다. 응답 포맷이 여러개면 요청 포맷도 나눠야 하기 때문이다.
3. Retry-After   
비정상적인 방법으로 API에게 많은 요청을 보내는 경우 `429 Too Many Requests` 라는 오류 응답으로 일정 시간 뒤에 요청하도록 한다
    1. 인증일 경우(로그인등)
        - n시간 동안 n회만 요청 가능    
        ⇒ Retry-After를 사용하여 `429` 에러를 내뱉는다.
        - n회만 요청 가능    
        ⇒ `401` 응답과 함께 다시 요청하려면 특수한 절차가 필요하다고 한다.
        (Retry-After X)
    2. 의도적으로 서버 과부하를 목적으로 반복 요청하는 경우
        - n시간 동안 n회 이상 요청한 경우    
    ⇒ Retry-After를 사용하여 `429` 에러를 내뱉는다.

### 3. HTTP Methods

1. POST, GET, PUT, DELETE(CRUD) 는 반드시!! 제공해야한다.
2. OPTIONS, HEAD, PATCH를 사용해 완성도 높은 API를 만든다.
    1. OPTIONS   
    현재 End-Point로 제공 가능한 API method를 응답한다.
    2. HEAD   
    요청에 대한 Header정보만 응답한다. **body**가 없다.
    3. PATCH   
    PUT : 모든 리소스를 교체한다. 보내지지 않는 리소스들은 null값으로 업데이트한다.   
    PATCH : 일부 리소스를 교체한다. 기존 데이터는 유지된다.

### 4. HTTP Status

1. `200` 으로 status를 응답하면서 body값은 실패했다는 메시지를 응답하는건 안 좋은 방식이다.
`400` 으로 status를 응답하면서 실패한 메시지를 보내는게 좋은 방식이다.
2. 세부 에러사항을 body에 담아 해당 에러를 확인할 수 있는 link를 표시한다.

### 5. Correct Status Code

1. 2XX (성공)
    1. 200 ⇒ OK
    2. 201 ⇒ Created (PUT, POST에 사용된다.)
    3. 202 ⇒ Accepted (비동기 작업에 사용된다.)
    4. 204 ⇒ No Content (응답 body가 없는 경우 ex) DELETE)
2. 4XX (실패)
    1. 400 ⇒ Bad Request   
    클라이언트의 요청이 정의된 요구사항을 위반한 경우   
    파라미터의 위치, 사용자 입력 값, 에러 이유등을 **반드시** 알린다.
    2. 401 ⇒ Unauthorized
    3. 403 ⇒ Forbidden (요청은 유효하나, 접근이 허용되지 않는 경우)
    4. 404 ⇒ Not Found
    5. 405 ⇒ Method Not Allowed   
    404와 헷갈리지 말 것. 룰을 잘 정해야 한다.   
    ex) 해당 URL로 데이터는 찾았으니, Method가 허용되지 않는 경우이다.
    6. 409 ⇒ Conflict   
    해당 요청을 처리하는데 모순이 생긴 경우   
    ex) DELETE하는데 만약 사용자 테이블에 아무것도 없는 경우이다.
    7. 429 ⇒ Too Many Requests   
    Retry-After을 사용한다.
3. 5XX (서비스 장애)
해당 경우는 API Server Level에서 나타나는 경우이다. 그래서 절대 사용자에게 나타내면 안된다.   
즉, API서버는 모든 발생 가능한 에러를 핸들링해야 한다는 말이 된다.
API 서버를 서빙하는 웹서버(apache, nginx)가 오류일 때는 가능하다.

### 6. Use HATEOAS

요청 - 응답으로 이루어지는데 응답은 되게 간단하게 응답한다.

여기서 문제는, 이 간단한 응답만으로는 사용자 리소스의 상태가 전이되기에는 정보가 부족하다.
HTML환경에서 보이는 환경이 있기 때문에 추후에 사용자의 상태가 전이될 수 있는 link를 화면에서 제공해줄 수 있다.

ex) 게시글을 만들고 해당 게시글을 바로 보려고 하려면, 클라이언트는 POST를 보내고 그에 대한 응답으로 게시글의 정보를 가져올 수 있는 link를 서버는 응답 본문에 같이 보내준다. 그러면 클라이언트는 URI를 하드코딩 하지 않고도 해당 link로 바로 서버에 요청을 보낼 수 있다.   
자세한 내용은 [https://pjh3749.tistory.com/260](https://pjh3749.tistory.com/260) 참조하면 HATEOAS에 대한 내용을 알 수 있다.
### 7. Sort, Filter
#### 7-1 Ordering

Collections(리스트)에 대한 GET 요청의 경우 `order` 라는 key를 이용해 정렬해서 응답한다.

#### 7-2. Filtering

Collections(리스트)에 대한 GET 요청의 경우 `AND` `OR` `=`  `>` `<`  등등.. 의 조건을 달 수 있다.

#### 7-3. Field-Selecting

Collections(리스트)에 대한 GET 요청의 경우 일부분만 선택해서 응답받을 수 있다.   
ex)   
include : ?fields=id, name
exclude : ?-fields=level
만약에 Field에서 요구하는 `Key`가 없다면 존재하는 `Key` 로만 응답해서 보내준다.

### 8. Versioning

- URI Versioning(이것을 사용한다.)   
Version 정보는 host레벨이 아닌 path레벨에 사용한다.   
`ex) http://api.test.com/v1`
- Accept Header   
`ex) Accept: application/vnd.example.v1+json`   
`ex) Accept: application/vnd.example+json;version=1.0`
- 개발 코드에서는 관리하지 않는다!!   
웹 서버의 reverse-proxy 기능을 활용한다.

> 출처   
> [https://velog.io/@taeha7b/api-restapi-restfulapi](https://velog.io/@taeha7b/api-restapi-restfulapi)