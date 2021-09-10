---
layout: post
title:  "HTTP에 대해서"
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

## HTTP란
HTTP(Hyper Text Transfer Protocol)는 인터넷에서 데이터를 주고받을 수 있는 프로토콜이다.

### HTTP의 동작은?

Client → Server 로 요청을 보내면 Server → Client로 요청에 대한 응답을 보내는 방식으로 진행된다.

응답의 형태로는 HTML문서도 있고 JSON형식등 다양한 형태가 존재한다. 이는 Client에서 어떤 정보의 형태로 받고싶은지 명시해놓는다.

## HTTP의 특징

- HTTP 메시지는 HTTP Client와 HTTP Server에 의해서 해석이 된다.
- TCP/IP를 이용하는 응용 프로토콜이다. 
⇒ HTTP/1.1, 2는 TCP/IP지만 HTTP/3은 UDP방식을 이용한다. HTTP/3에 대한 내용은 [링크](https://evan-moon.github.io/2019/10/08/what-is-http3/)를 참조하자
- HTTP는 연결 상태를 유지하지 않는 비연결성 프로토콜이다. ⇒ Cookie, Session으로 보완
- HTTP는 연결 상태를 유지하지 않기 때문에 "요청"과 "응답"으로 통신이 이루어진다.

## TCP/IP를 이용한 통신

TCP/IP는 3-way-handshake, 4-way-handshake를 이용해 통신의 시작과 끝을 맺는다. 앞서 말했듯이 HTTP는 비연결성 프로토콜이다. 그렇기 때문에 통신을 할 때마다 새롭게 연결을 해줘야 하는 번거로움이 있다.   
통신을 할 때마다 handshake과정을 반복하는 것이다. 이는 매우 비효율적이다. 그렇기 때문에 HTTP/1.1에서는 `keep-alive` 라는 것을 사용하였다.

## Keep-alive

keep-alive에는 timeout, max가 존재한다. timeout은 이 시간동안 연결을 유지시키겠다는 것이고, max는 한 번 연결시에 최대 요청의 갯수를 나타낸다. 

### 단점

서버가 한적하다면 keep-alive를 이용해 약 50%의 성능 향상까지 보일 수 있다는 장점이 있다.   
하지만 서버가 바빠진다면, 모든 요청마다 연결을 유지해야하기 때문에 프로세스 수가 기하급수적으로 늘어나게 된다. 따라서 메모리를 많이 사용하게 되어 곧 성능 저하까지 이루어지게 된다.

### 문제점

설계상 이미 문제가 있다. 바로 프록시 서버나 캐시 서버등 중개서버를 이용하게 되면 생기는 문제이다.   

중개 서버가 Connection: keep-alive를 이해하지 못한다면, 어떻게 될까?

1. 클라이언트는 keep-alive를 붙여서 "프록시 서버"에게 "우리 연결을 유지하자!" 라고 요청한다.
2. 프록시 서버는 이 헤더를 읽지 못한다. 그냥 바로 서버에게 전달한다.
3. 서버는 이 keep-alive를 읽고 "프록시 서버"가 "연결을 유지하자!" 라고 요청을 보낸 줄 안다. 
그래서 "그래! 연결을 유지하자! 프록시 서버야!" 라고 응답한다.
4. 프록시 서버는 이 응답을 곧이 곧대로 클라이언트에게 전달한다.
5. 클라이언트는 "프록시 서버"가 나에게 연결을 유지하자라고 응답을 준 줄 안다.
6. 그리고 "기존에 연결했던 커넥션"으로 클라이언트가 프록시 서버에게 요청을 보내면, 프록시 서버는 이를 예상하지 못한다. 같은 커넥션상에서 다른 요청이 오는 경우는 프록시 서버가 응답할 줄 모르기 때문이다. 그래서 해당 요청을 무시한다.
7. 클라이언트는 프록시 서버에게 요청했던 응답을 한없이 기다린다. 하지만 프록시 서버는 이를 무시했기 때문에 응답은 돌아오지 않는다. 그렇게 타임아웃이 나고 커넥션이 끊긴다.

### 차선책

프록시 서버가 keep-alive를 읽을 수 있게끔 한다.    
`Proxy-Connection: Keep-Alive`라고 보내면 이제 프록시 서버는 이를 해석하고, 클라이언트가 "우리 연결을 유지하자!" 라고 하는 거구나. 깨닫는다. 서버와 프록시 서버사이의 연결은 프록시 서버가 연결할지 말지 정한다. 서버에게 keep-alive를 보낼지 말지를 말이다.

### 차선책의 문제점

하지만 이도 문제가 있다.

프록시 서버가 `Proxy-Connection: Keep-Alive` 이거를 읽지 못한다고 해보자. 그러면 프록시 서버는 이를 곧이 곧대로 서버에게 전달할 것이고, 서버는 이 헤더를 읽지 못한다. 그래서 해당 요청을 무시해버린다. 그러면 클라이언트는 keep-alive되었다는 응답을 받지 못하고 커넥션을 유지시키지 못한다.

만약 프록시 서버를 2대 사용해도 문제가 있다.

클라이언트 - 멍청한 프록시 - 영리한 프록시 - 서버 로 묶여 있어도 아까 처음에 말했던 문제점이 그대로 발생한다.

⇒ Event-driven 구조여서 non-blocking을 사용하는 Ngnix등은 Keep Alive를 사용하면서도 Thread를 점유하지 않기 때문에 동시 처리에 유리하다.

> 참고   
[https://velog.io/@surim014/HTTP란-무엇인가](https://velog.io/@surim014/HTTP%EB%9E%80-%EB%AC%B4%EC%97%87%EC%9D%B8%EA%B0%80)    
[https://goodgid.github.io/HTTP-Keep-Alive/](https://goodgid.github.io/HTTP-Keep-Alive/)