---
layout: post
title:  "클라우드란 무엇인가"
subtitle:   "cloud"
categories: study
tags: 그냥저냥 cloud, vm
comments: true
# header-img: ""
---
- 목차
	- [클라우드 컴퓨팅이란?](#클라우드-컴퓨팅이란)
    - [클라우드 컴퓨팅 유형](#클라우드-컴퓨팅-유형)
    - [클라우드 용어](#클라우드-용어)
    - [가상화 기술 - Hypervisor](#가상화-기술---hypervisor)

## 클라우드 컴퓨팅이란?

Cloud(구름)이라는 단어가 말해주듯, 사용자의 직접적인 관리 없이 인터넷 통신망을 통해 구름 뒤편에 보이지 않는 데이터 스토리지, CPU등 컴퓨터 시스템 리소스를 제공받는것을 말한다.

클라우드 서비스에는 많은 종류가 있다. AWS, Azure, GCP(Google Cloud Platform)등 ...

이 클라우드 서비스들은 어떻게 사용자들에게 원하는 CPU, 스토리지등을 할당해 줄 수 있을까? 바로 **서버 가상화** 작업이다.

하나의 서버는 20TB의 저장공간, RAM 256GB라고 해보자. 이 어마어마한 서버의 용량을 여러명에게 최적화로 나눠주고 싶다. 그렇게 하려면 하나의 서버에 여러대의 **가상 서버**를 띄우면 된다. 그 가상 서버를 사용자에게 전해주면 되는것이다.

![image](https://user-images.githubusercontent.com/22341452/134683317-91fd6789-6505-4ecc-a8de-b91f54446925.png)

### 클라우드의 이점
- 초기 구축 비용이 낮다.
- 확장성이 좋다.
- 관리성이 좋다.
- 서버 세팅등을 신경쓰지 않아도 된다.

### 클라우드의 단점
- 인터넷 속도에 의존해야한다.
- 중앙에서 모든 데이터를 스토리지에 관리한다.
- 추가적인 비용 지출에 대한 고려가 필요하다.

## 클라우드 컴퓨팅 유형

### 1. IaaS (Infrastructure as a Service)

![image](https://user-images.githubusercontent.com/22341452/134683375-ed49f7c3-f073-453c-b05c-9ab1afdc9114.png)

해당 서버를 열 수 있는 자원만 제공해주고 나머지는 사용자가 선택하는 방식이다. 제일 확장성이 높다.

ex) AWS의 EC2, GCP의 GCE등

### 2. PaaS (Platform as a Service)

![image](https://user-images.githubusercontent.com/22341452/134685629-488a2705-f57e-4639-9843-eae82b6da509.png)

사용자가 원하는 서비스를 개발할 수 있도록 개발 환경을 미리 구축해 서비스 형태로 제공하는 것이다.

서비스 외적인 부분에 신경쓰지 않고 오직 개발과 비즈니스에만 집중이 가능하다.

ex) Salesforce의 Heroku, Redhat의 OpenShift

### 3. SaaS (Software as a Service)

![image](https://user-images.githubusercontent.com/22341452/134683459-b1f6ff74-3d88-45ba-833f-98f95ed1a17f.png)

소프트웨어까지 탑재해서 제공하는 형태이다. 업데이트, 버그개선등의 서비스를 업체가 도맡아 제공한다.

ex) Slack, Microsoft 365, Dropbox, Salesforce, Netflix

## 클라우드 용어
### Public Cloud
모든 사용자를 위한 클라우드 서비스이다. 인터넷이 가능하다면 언제든지 접속이 가능하다.

ex) AWS, GCP, Azure등

### Private Cloud
제한된 네트워크에서 사용되는 클라우드 서비스이다. 주로 기업내 네트워크에서 사용되고, 보안성이 매우 뛰어나며 클라우드 기능을 커스터마이징 할 수 있다.

ex) vmware, citrix, openstack

### Hybrid Cloud
Public Cloud + Private Cloud이다. 최근에는 가상서버 + 물리서버를 결합한 형태를 뜻하기도 한다.

기업내의 주요 데이터들은 Private Cloud에 넣어두고, 다른 부분들은 Public Cloud를 사용하여 Public Cloud의 장점과 Private Cloud의 장점을 모두 사용할 수 있다.

## 가상화 기술 - Hypervisor

가상 머신 모니터라고도 하는 하이퍼바이저(Hypervisor)는 가상 머신을 생성하고 실행하는 프로세스이다.   
하이퍼바이저에는 2가지 유형이 있다. `"Native" or "Bare-Metal" 하이퍼바이저`와 `"Hosted" 하이퍼바이저`가 있다.

### "Native" or "Bare-Metal" Hypervisor

![image](https://user-images.githubusercontent.com/22341452/134683478-8df07d5f-4d5e-4064-9c11-0da89fa67590.png)

호스트 하드웨어에서 **직접** 실행되어 하드웨어를 제어하고 게스트 가상머신들을 관리한다.   

게스트 운영 체제가 다른 게스트 운영 체제에 영향을 끼칠 수 없다는 것이 장점이다.

ex) Xen, Oracle VM Server for SPARC, Microsoft Hyper-V등

### Hosted Hypervisor

![image](https://user-images.githubusercontent.com/22341452/134683489-28c041f5-16ce-44fe-b5cb-9c91967845d7.png)

위 시스템은 호스트에서 게스트 OS들을 **프로세스**로 실행되어진다. 그래서 호스트 운영 체제에 전적으로 의존할 수 밖에 없다.

ex) VMware WorkStation, VirtualBox, Parallels Desktop for Mac등

> 참조   
Elice AI Track   
[https://library.gabia.com/contents/infrahosting/9114/](https://library.gabia.com/contents/infrahosting/9114/)   
[https://dora-guide.com/하이퍼바이저/](https://dora-guide.com/%ED%95%98%EC%9D%B4%ED%8D%BC%EB%B0%94%EC%9D%B4%EC%A0%80/)