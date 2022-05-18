This repository is where we keep a record of our Instagram-clone-project progress.

## Table of Contents
- [Project Introduction](#Project-Introduction)
- [Team](#Team)
- [Project-Rules](#Project-Rules)
- [Development](#Development)
- [Structure](#Structure)

## Project-Introduction
- 주제 : 인스타그램 Clone 프로젝트
- 기간 : 22.05.03(화) ~ 22.05.11(수)

<hr>

## Team
- 김선민 [Git-hub](https://github.com/SeonminKim1)
- 김민기 [Git-hub](https://github.com/kmingky)
- 박재현 [Git-hub](https://github.com/Aeius)
- 황신혜 [Git-hub](https://github.com/hwanghye00)

<hr>

## Project-Rules
- Figma Mock-up : [Figma Link](https://www.figma.com/file/mAAgNkm5xXXMtmUD3qGpyA/7%EC%A1%B0-%EC%9D%B8%EC%8A%A4%ED%83%80%EA%B7%B8%EB%9E%A8-%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8)
- Schedule Management : [Git Project Link](https://github.com/SeonminKim1/7Instagram/projects/1), [간트차트 Link](https://docs.google.com/spreadsheets/d/1_1Sx46dnKnI8_DLJQzAASMSr7u525RFjm2Iat0beU14/edit#gid=1115838130)
- Git Issue : [Git Issue Link](https://github.com/SeonminKim1/7Instagram/issues)
- API Design : [Notion Link](https://www.notion.so/c1bcd82a87284af2a31417eb05f91bbe?v=af9524e1b4424fc1ab878849998a052d)
- Tool : FE : HTML, CSS, JS / BE : Flask / DB : MongoDB (Atlas)
- DB Design
![그림1](https://user-images.githubusercontent.com/33525798/168956345-cc4e7a7d-1198-481e-85f4-68dbaea2f721.png)

<hr>

## Development
#### Login / Register
- Register(회원가입) : User 정보 검증 및 DB 저장
  - 아이디 중복 체크 (이메일형식, 4~30자)
  - 닉네임 중복 체크 (영대소문자, 숫자, (_ . @ !) 특수문자, 4~12자)
  - 이름 체크 (영대소문자, 한글 2-20자)
  - 비밀번호 체크 (영대소문자, 숫자, (!@#$%^) 특수문자, 8~20자)

- Login(로그인) : 입력 정보 DB 검증 및 Token 부여
  - JWT(Json Wep Token) 생성 (ID 값 저장)
  - 페이지 로드시 Token 체크 유지 시간(30분) 초과시 토큰 삭제 및 로그아웃
 
#### Feed Page
- 게시물 조회 : 로그인 유저 정보 조회
  - User가 Follow 한 사람의 Feed 출력
- 게시물 헤더 : 유저 프로필 페이지 이동
- 게시물 본문
  - 게시글 조회
  - 게시물 좋아요/해제 
  - 북마크 등록/해제
- 게시물 모달 (위 기능과 동일)
- 게시물 댓글
  - 댓글 조회
  - 댓글 작성
- 친구 추천 기능
  - 추천 유저 Follow / Unfollow 가능
  - 추천 알고리즘 : 전체 유저 - 내가 팔로우한 유저 리스트
- (다음 기회에) 게시물 편집 (수정, 삭제) Option ( ··· )
 
#### Mypage
- Follow , Following (모달)
  - 팔로우/언팔로우 기능
  - 팔로우/팔로잉 수
- 포스트 출력 (유저가 작성한)
  - 포스트 Hover (좋아요/댓글 정보)
  - 포스트 Click (게시글 모달)
- 프로필 이미지 변경
  - 이미지 업로드 및 서버 저장
- (다음 기회에) 포스트 북마크 탭 (저장됨) 출력

#### Nav bar
- 홈, 마이페이지 : 페이지 이동
- 새 게시물 작성 (모달)
  - 이미지 업로드 후 서버 저장
- (다음 기회에) 게시물 최근 활동
 
<hr>

### Structure
```
├── services // 기능 함수들
│   ├── a.py
│   └── ...
│
├── static 
│   ├── css
│   ├── imgs
│   └── ...
│
├── templates 
│   ├── Login // 로그인
│   │   ├── index.html
│   │   └── ...
│   │
│   ├── Feed // 피드페이지
│   │   ├── index.html
│   │   └── ...
│   │
│   └── Profilepage // 프로필페이지
│       ├── index.html
│       └── ...
│
└── app.py // 메인
``` 
