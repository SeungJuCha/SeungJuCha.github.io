# SeungJu Cha — Academic Homepage

첨부 CV와 프로필 사진을 기반으로 만든 개인 학술 홈페이지입니다. [Kevin Lu의 개인 홈페이지](https://kevinlu4588.github.io/)와 비슷한 미니멀한 구성을 참고하되, **About / Quotes 섹션은 제외**했습니다. 별도의 프론트엔드 프레임워크 없이 GitHub Pages에서 실행됩니다.

## 포함된 내용

- 프로필 사진, 소속 및 연구 관심사, 이메일 2개, Google Scholar, GitHub, LinkedIn, CV PDF
- News, Publications(총 12편, CV의 두 카테고리와 순서 유지), Education, Academic Service, Technical Skills
- 첨부 CV PDF에 실제로 포함된 논문 링크 연결. URL이 없던 논문에는 임의 링크를 추가하지 않음
- 데스크톱 / 태블릿 / 모바일 반응형 디자인

## 파일 구성

| 파일 | 설명 |
| --- | --- |
| `content.json` | **주로 수정할 파일**: 소개, 링크, News, 논문, 학력, 리뷰 활동, 기술 역량 |
| `build.py` | `content.json`의 데이터를 정적 `index.html`로 생성 |
| `index.html` | 배포되는 웹페이지. 자동 생성 파일이므로 보통 직접 수정하지 않아도 됨 |
| `styles.css` | 색상, 폰트, 간격, 레이아웃 |
| `script.js` | 스크롤 시 상단 메뉴에서 현재 섹션 표시 |
| `assets/profile.webp`, `assets/profile.jpg` | 최적화된 프로필 사진 |
| `assets/SeungJu_Cha_CV.pdf` | 방문자가 다운로드할 CV |
| `.github/workflows/pages.yml` | 변경 내용을 GitHub Pages에 자동 빌드/배포 |

## GitHub Pages 배포 방법

1. 본인 GitHub 계정에 로그인합니다. CV에 기재된 GitHub는 `https://github.com/SeungJuCha`입니다. 다른 계정으로 배포할 예정이면 아래 리포지토리 이름을 변경하세요.
2. 새로운 **Public** 리포지토리를 만듭니다. 이름은 **`SeungJuCha.github.io`**로 지정합니다. (다른 GitHub 아이디라면 `<아이디>.github.io`.)
3. ZIP 파일을 압축 해제한 뒤, **내부의 모든 파일과 폴더**를 리포지토리 `main` 브랜치의 최상위에 업로드합니다. 숨김 폴더인 **`.github`**도 포함해야 합니다. ZIP 파일 자체만 올리면 안 됩니다.
4. 리포지토리의 **Settings → Pages → Build and deployment → Source**에서 **GitHub Actions**를 선택합니다.
5. **Actions** 탭에서 **Deploy academic website** 작업이 성공할 때까지 기다립니다. 해당 아이디라면 주소는 `https://seungjucha.github.io/`가 됩니다. 첫 게시가 반영되기까지 몇 분 걸릴 수 있습니다.

이미 같은 이름의 리포지토리가 있다면 기존 파일을 덮어쓰기 전에 내용을 확인하세요. 이 파일들은 **아직 실제 GitHub에 업로드되지 않았습니다.**

## 추후 내용 수정하기

가장 간단한 방법은 GitHub 웹페이지에서 **`content.json`만 수정하고 `main` 브랜치에 커밋**하는 것입니다. 포함된 GitHub Actions 워크플로가 자동으로 HTML을 재생성하고 사이트를 배포합니다.

- **논문 추가:** `publications` 배열에 `category`, `title`, `authors`, `venue`, `year`를 입력합니다. 링크가 있다면 `url`, 특별 표기가 있다면 `award`를 선택적으로 추가합니다.
- **News 추가:** `news` 배열 맨 앞에 `year`, `headline`, `detail`, 선택적 `url` 항목을 추가합니다.
- **자기소개 / 소속 / 이메일 / Scholar / LinkedIn 변경:** `content.json` 앞부분의 해당 필드를 바꿉니다.
- **CV 업데이트:** `assets/SeungJu_Cha_CV.pdf`를 새로운 PDF로 교체하고 파일명을 유지합니다. **CV PDF를 바꾸는 것만으로 웹페이지의 논문 목록이 자동으로 바뀌지는 않습니다.** 웹 내용은 `content.json`도 수정해야 합니다.
- **사진 변경:** `assets/profile.jpg`, `assets/profile.webp`를 교체합니다.
- **디자인 변경:** `styles.css` 처음 부분의 색상 및 글꼴 변수를 수정합니다.

### 로컬 미리보기

PC에 Python이 설치되어 있다면 아래 명령으로 실행할 수 있습니다.

```bash
python3 build.py
python3 -m http.server 8000
```

그다음 브라우저에서 `http://localhost:8000`을 엽니다. `content.json`을 로컬에서 수정할 때마다 `python3 build.py`를 다시 실행하면 됩니다. 별도 Python 패키지는 필요 없습니다.

## 자료 기준

2026년 내용이 포함된 첨부 CV와 제공받은 프로필 사진만을 기본 자료로 사용했습니다. News는 CV에 기재된 학회 발표를 연도 단위로 정리한 요약이며, CV에 발표 월이 없다면 월을 임의로 채우지 않았습니다. 공식 논문 링크가 없던 일부 ACCV 논문은 링크 없이 표시했습니다. 공개 전 최신 정보로 점검해 주세요.
