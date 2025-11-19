# NMIXX FANS (엔믹스 팬즈)

## 📋 프로젝트 개요

JYP 엔터테인먼트의 자회사 Blue Garage에서 개발·운영하는 **FANS** 서비스를 바탕으로 제작한 **NMIXX FANS** 서비스입니다. **React Native**로 앱을 개발했으며, 백엔드 서버는 **Django**와 **GraphQL**을 이용하여 구축했습니다.

<br />

## ⏱️ 개발 기간
2025년 8월 10일 ~ 2025년 8월 30일

<br />

## ⚡️ 주요 기능

- "아티스트" 와 "팬"으로 분류된 커뮤니티 게시판을 통해 아티스트와 팬들 간의 교류를 활성화합니다.
- 개인 프로필을 설정하고 관리할 수 있습니다.
- 전날 인기 게시글을 "팬" 게시판에 노출하여 아티스트와 팬의 소통을 강화합니다.
- AWS S3 버킷을 활용한 이미지 업로드 기능을 제공합니다.
- Django + GraphQL을 이용한 API 서버를 개발했습니다.
- React Native를 이용한 모바일(크로스 플랫폼) 앱을 개발했습니다.

<br />

## ⚙️ 사용 기술
<div style="display: flex; gap: 5px;">
  <img src="https://img.shields.io/badge/React_Native-61DAFB?style=flat-square&logo=react&logoColor=white" />
  <img src="https://img.shields.io/badge/Django-092E20?style=flat-square&logo=django&logoColor=white" />
  <img src="https://img.shields.io/badge/GraphQL-E10098?style=flat-square&logo=graphql&logoColor=white" />
  <img src="https://img.shields.io/badge/Redux-764ABC?style=flat-square&logo=redux&logoColor=white" />
  <img src="https://img.shields.io/badge/StyledComponents-DB7093?style=flat-square&logo=styledcomponents&logoColor=white" />
  <img src="https://img.shields.io/badge/Typescript-3178C6?style=flat-square&logo=typescript&logoColor=white" />
</div>

<br />

-   **React Native**: 모바일(크로스 플랫폼) 애플리케이션 개발을 위해 사용하였습니다.
-   **Django**: 안정적인 ORM, 보안 기능을 갖춘 Python 웹 프레임워크로, 빠른 서버 개발을 위해 사용하였습니다.
-   **GraphQL**: 클라이언트 중심의 유연한 API 통신을 위해 사용하였습니다.
-   **Redux Toolkit**: 전역 상태 관리를 위해 사용하였습니다.
-   **Styled-components**: JavaScript 파일 내에서 CSS를 작성하고, 스타일 충돌 방지를 위해 사용하였습니다.
-   **TypeScript**: 정적 타입 명시를 통해 코드의 안정성과 유지보수성을 향상시키기 위해 사용하였습니다.

<br />

## 🗂️ 프로젝트 구조

```
app/
├── features/ # 재사용 가능한 UI 컴포넌트
├── pages/ # 애플리케이션의 각 화면을 정의하는 최상위 컴포넌트
├── shared/ # 앱 전체에서 사용되는 공통 컴포넌트
└── widgets/ # 재사용될 수 있는 더 큰 UI 컴포넌트
```

<br />

## 🗺 서비스 화면

### 6-1. 메인스크린/탭구성
<img width="1920" height="1080" alt="nmixxfans_home" src="https://github.com/user-attachments/assets/d34a98f8-d158-4ac3-a23b-f9e5e29b0173" />

### 6-2. 게시판
<img width="1920" height="1080" alt="nmixxfans_board" src="https://github.com/user-attachments/assets/e529383a-1de3-4b59-836d-c68d1ac62707" />

### 6-3. 글쓰기/이미지업로드
<img width="1920" height="1080" alt="nmixxfans_write" src="https://github.com/user-attachments/assets/e31e8add-66d7-4223-b2be-1fee14958fab" />

### 6-4. 로그인/회원가입
<img width="1920" height="1080" alt="nmixxfans_login" src="https://github.com/user-attachments/assets/e4a2db6d-1d4a-44d0-b553-6c3e41e66803" />

## 7. 앱 사용 시연 영상
### 7-1. 회원가입/로그인/로그아웃
<a href="https://youtu.be/ynX9DmGF_gU" target="_blank">
  <img src="http://img.youtube.com/vi/ynX9DmGF_gU/maxresdefault.jpg" alt="Video Label" />
</a>

### 7-2. 게시판 게시글 보기/댓글 작성/좋아요
<a href="https://youtu.be/zXaokIdoMc0" target="_blank">
  <img src="http://img.youtube.com/vi/zXaokIdoMc0/maxresdefault.jpg" alt="Video Label" />
</a>

### 7-3. 게시글 작성/이미지 업로드
<a href="https://youtu.be/58W6WkwfIas" target="_blank">
  <img src="http://img.youtube.com/vi/58W6WkwfIas/maxresdefault.jpg" alt="Video Label" />
</a>

### 7-4. 어제의 인기글
<a href="https://youtu.be/8lR5xPqHpIc" target="_blank">
  <img src="http://img.youtube.com/vi/8lR5xPqHpIc/maxresdefault.jpg" alt="Video Label" />
</a>
