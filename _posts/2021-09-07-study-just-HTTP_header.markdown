---
layout: post
title:  "HTTP Header와 Cache, Cookie"
subtitle:   "HTTP와 http header"
categories: study
tags: 그냥저냥 http header
comments: true
# header-img: ""
---
- 목차
	- [HTTP란](#http란)
    - [HTTP의 특징](#http의-특징)
    - [TCP/IP를 이용한 통신](#tcpip를-이용한-통신)
    - [Keep-alive](#keep-alive)

# Header의 종류

## Request HTTP Message

- **GET** **/api/user-info HTTP/1.1**   
GET : HTTP method   
/api/user-info : 요청보낸 주소   
HTTP/1.1 : HTTP의 버전
- **Host**  
 → 서버의 도메인이 나타나는 부분이다. 반드시 하나가 존재해야 한다.
- **Connection**  
 → [keep-alive](#https://jeonggod.github.io/study/2021/09/06/study-just-HTTP/#keep-alive) 위에 설명을 참조하자. HTTP/2에서는 없어진 헤더이다.
- **Accept**  
 → 서버는 이러한 타입의 데이터로 보내달라는 요청이다.
text/html 이라고 보내면 html형식인 데이터만 처리하겠다는 것이다.
- **Authorization**  
 → 인증 토큰을 보내기 위해서 사용되는 헤더이다. `Basic` `Bearer` 를 앞에 붙여 토큰의 종류를 알리고 보낸다.
- **User-Agent**
현재 사용자가 어떤 클라이언트를 이용해 요청을 보냈는지 나온다.
물론 임의로 조작할 수도 있기에 믿어서는 안된다. 접속자 통계를 내기 위해서 사용된다.
- **Referer**  
 → 해당 페이지 이전의 페이지 주소가 담겨져있다. 이 헤더를 이용하여 어떤 페이지에서 접속했는지 확인이 가능하다. (여담이지만, Referrer가 표준어이지만 오타라고 한다.)
- **Origin**  
 → POST같은 요청을 보낼 때, 요청이 어느 주소에서 시작되었는지를 나타내는 것이다. 요청을 보낸 주소와 받는 주소가 다르다면 CORS에러를 내뱉는다.

## Status Code

- **1XX (조건부 응답)**  
 → 요청을 받았으며 작업을 계속한다.
- **2XX (성공)**  
 → 클라이언트가 요청한 동작을 수신하여 이해했고 승낙했으며 성공적으로 처리했음을 가리킨다.
- **3XX (리다이렉션 완료)**  
 → 클라이언트는 요청을 마치기 위해 추가 동작을 취해야 한다.
- **4XX (요청 오류)**  
 → 클라이언트에 오류가 있음을 나타낸다.
- **5XX (서버 오류)**  
 → 서버가 유효한 요청을 명백하게 수행하지 못했음을 나타낸다.

## Response HTTP Message

- **Access-Control-Allow-Origin**  
 → 요청을 보내는 Client주소와 Server의 주소가 다르면 CORS에러를 내뱉는다.
CORS요청시에는 OPTIONS 주소로 현재 서버가 CORS를 허용하는지 물어본다. 이렇게 물어본 뒤 가능하다면 본요청을 진행한다.
- **Allow**  
 → 이 주소로는 해당 메소드만 허용하겠다는 표시이다. 만약 
`GET http://jeong.com` 요청을 했지만 `POST` 만 허용한다면 405 Method Not Allowed 에러와 함께 헤더로 `Allow : POST` 을 보내면 된다.
- **Content-Disposition**  
 → 응답 본문을 브라우저가 어떻게 표시해야 할 지 알려주는 헤더이다.
`inline` : 브라우저에 표시, `attachment` : 파일 다운로드 ⇒ filename옵션으로 다운로드시 파일명도 지정해줄 수 있다.
- **Location**  
 → 300번대 응답코드나, 200번대 응답코드가 왔다면 어느 페이지로 이동할지 알려주는 헤더다.
- **Content-Security-Policy**  
 → 다른 외부 파일들을 불러오는 경우, 차단할 소스와 불러올 소스를 명시한다.
 하나의 웹페이지는 다양한 외부 소스들을 불러온다. 폰트나 이미지등.. 그 때 악성코드가 심어진 파일을 불러오게 된다면 치명적인 오류가 생길 수 있다. XSS 공격이 바로 그 일종이다. 그러한 점을 방지하기 위해서 해당 헤더로 허용한 외부 소스만 불러올 수 있게 설정한다.   
다양한 옵션이 존재하기에 자세한 내용은 [해당 링크](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy)를 참조하자.

## Cache & Cookie

 개인 캐시를 뜻한다. 브라우저에 응답으로 온 데이터를 캐시로 저장하여 추후에 서버에게 요청을 보내지 않고 저장된 캐시를 사용할 수 있다.

### Cache

- Cache-Control  
no-store : 아무것도 캐싱하지 않겠다.  
no-cache : 모든 캐시를 쓰기 전, 서버에게 이 캐시를 써도 되냐고 물어보라는 뜻.
must-revalidate : 만료된 캐시만 서버에 확인을 받겠다.  
public : 공유 캐시로 저장해도 무방하다. private : 브라우저같은 특정 사용자 환경에서만 저장해라.  
max-age : 캐시의 유효시간을 줄 수 있다. 초단위로 이루어져있다. 응답 헤더로만 쓰이는게 아니라 요청 헤더로도 쓰일 수 있다.
- Age  
캐시 응답시에 나타난다. max-age시간 내에서 얼마나 흘렀는지 알려준다.
- Expires  
응답 컨텐츠가 언제 만료되는지를 나타낸다. Cache-control에 max-age가 있는 경우 무시된다.
- ETag  
HTTP 컨텐츠가 바뀌었는지 검사할 수 있는 태그이다. 같은 주소의 자원이라도 컨텐츠가 달라졌다면 ETag가 달라진다. 
만약 `GET http://jeong.com` 의 응답 본문이 `"정규"` 일 때 ETag가 12345라고 해보자. 그 때 나중에 같은 주소로 GET요청을 보내면 항상 ETag는 12345이다. 하지만  응답 본문이 `"동규"` 로 바뀐다면 ETag는 34567 로 바뀐다. 이를 활용하여 응답 내용이 달라졌구나를 클라이언트가 깨닫고 캐쉬를 지우고 새로 받는 작업을 할 수 있다.
- If-None-Match  
ETag가 달라졌는지 검사하여 다를 경우에만 컨텐츠를 새로 내려받으라는 의미이다.

### Cookie

- Set-Cookie  
Server → Client에게 이러한 쿠키를 저장하라는 헤더이다.
- Expires  
→ 쿠키 만료 날짜를 알려준다.
- Max-Age  
→ 쿠키 수명을 알려준다. Expires는 무시된다.
- Secure  
→ https에서만 쿠키가 전송이 된다.
- HttpOnly  
→ 자바스크립트에서 쿠키에 접근할 수 없다. XSS요청을 막으려면 활성화하는것이 좋다.
- Domain  
→ 도메인을 적어두면 도메인이 일치하는 요청에서만 쿠키가 전송된다.
- Path  
→ 패스를 적어주면 이 패스와 일치하는 요청에서만 쿠키가 전송된다.
- Cookie   
Client → Server로 쿠키를 보내줄 때에는 해당 헤더를 사용한다.
CSRF공격을 피하기 위해서는 서버에서 쿠키가 제대로 된 클라이언트에서 온 것인지 확인하는 로직을 거쳐야 한다.

> 출처   
[https://www.zerocho.com/category/HTTP/post/5b4c4e3efc5052001b4f519b](https://www.zerocho.com/category/HTTP/post/5b4c4e3efc5052001b4f519b) Header   
[https://www.zerocho.com/category/HTTP/post/5b594dd3c06fa2001b89feb9](https://www.zerocho.com/category/HTTP/post/5b594dd3c06fa2001b89feb9) Cookie & Cache