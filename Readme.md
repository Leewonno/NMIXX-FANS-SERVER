# NMIXX FANS (엔믹스 팬즈)

## 1. 소개

JYP 엔터테인먼트의 자회사 Blue Garage에서 개발·운영하는 **FANS** 서비스를 기반으로 제작한 **NMIXX FANS** 서비스입니다. **React Native**로 앱을 개발했으며, 백엔드 서버는 **Django**와 **GraphQL**을 이용하여 구축했습니다.

## 2. 개발기간
2025년 8월 10일 ~ 2025년 8월 30일

## 3. 주요 기능

*   **커뮤니티 게시판**: "아티스트" 와 "팬"으로 분류된 게시판을 통해 아티스트와 팬들 간의 교류를 활성화합니다.
*   **게시글 상세 보기 및 댓글**: 게시물의 내용을 확인하고 댓글을 작성하여 소통할 수 있습니다.
*   **개인 프로필 관리**: 개인 프로필을 설정하고 관리할 수 있습니다.
*   **인기글 보기**: 전날 인기 게시글을 확인하며 소통을 강화합니다.

## 4. 사용 기술
*   **React Native**: 모바일(크로스 플랫폼) 애플리케이션 개발을 위한 프레임워크
*   **TypeScript**: JavaScript 정적 타입 체크
*   **Styled-components**: React Native 컴포넌트 스타일 적용
*   **Redux Toolkit**: 전역 상태 관리
*   **Django**: Python 웹 프레임워크
*   **GraphQL**: API 통신을 위한 쿼리 언어

## 5. 폴더 및 파일 구조

`app/` 디렉토리는 애플리케이션의 핵심 로직을 포함하며, 다음 세 가지 주요 폴더로 구성됩니다:

*   `features/`: 재사용 가능한 UI 컴포넌트와 비즈니스 로직을 포함하는 기능별 모듈입니다.
*   `pages/`: 애플리케이션의 각 화면을 정의하는 최상위 컴포넌트입니다
*   `shared/`: 앱 전체에서 사용되는 공통 컴포넌트, 유틸리티 함수, API 서비스 및 타입 정의를 포함합니다.
*   `widgets/`: 특정 페이지나 기능에 속하지만, 재사용될 수 있는 더 큰 UI 컴포넌트들을 모아둔 곳입니다.

## 6. 화면 구성
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
