# P:dback 코딩 컨벤션

팀원 전원이 지켜야 할 코딩 규칙입니다.

---

## Python (백엔드)

### 네이밍
- 함수 / 변수: `snake_case`
- 클래스: `PascalCase`
- 상수: `UPPER_SNAKE_CASE`

### 타입 힌트
- 모든 함수의 파라미터와 리턴 타입 필수
- Optional은 `float | None` 형식 사용 (`Optional[float]` 사용 금지)

```python
# Good
async def start_interview(request: InterviewStartRequest) -> InterviewStartResponse:

# Bad
async def start_interview(request):
```

### Docstring
- 한글로 작성, 함수 첫 줄에 한 줄 설명

```python
async def start_interview(request: InterviewStartRequest) -> InterviewStartResponse:
    """면접 세션을 생성하고 첫 질문을 반환합니다."""
```

### Import 순서
1. 표준 라이브러리
2. 서드파티 패키지
3. 로컬 모듈

그룹 사이에 빈 줄을 넣습니다.

```python
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config import settings
```

### 비동기
- 엔드포인트와 서비스 함수는 모두 `async def`

### 에러 처리
- `HTTPException`으로 통일, 상태 코드와 한글 메시지 포함

```python
raise HTTPException(status_code=404, detail="면접 세션을 찾을 수 없습니다.")
```

### 린터
- **Ruff** 사용, `ruff check app/` 으로 검사
- 한 줄 최대 100자

---

## JavaScript (프론트엔드)

### 네이밍
- 함수 / 변수: `camelCase`
- 클래스: `PascalCase`
- 상수: `UPPER_SNAKE_CASE`

### 스타일
- 문자열: 작은따옴표(`'`) 사용
- 세미콜론: 사용
- 들여쓰기: 스페이스 2칸

### 비동기
- `async/await` 사용 (`.then()` 체이닝 금지)

```javascript
// Good
const data = await fetchInterview(sessionId);

// Bad
fetchInterview(sessionId).then(data => { ... });
```

### DOM
- `document.querySelector` / `querySelectorAll` 통일
- `getElementById` 등 혼용 금지

### API 호출
- `fetch` 사용, 공통 헬퍼 함수로 래핑

---

## Git 규칙

### 커밋 메시지
`[파트] 작업내용` 형식

```
[interview] Gemini 꼬리질문 생성 구현
[feedback] 종합 피드백 점수 산출 로직 추가
[frontend] 면접 진행 화면 레이아웃 완성
[infra] GitHub Actions 배포 파이프라인 수정
```

### 브랜치
- 자기 브랜치에서만 작업
- **main 직접 push 금지**
- PR을 통해서만 main에 머지

### PR
- 최소 **1명 리뷰** 후 머지
- PR 제목도 커밋 메시지와 동일한 형식 사용

### 주석
- 한글로 작성
- "왜" 그렇게 했는지를 설명 (코드가 "무엇"을 하는지는 코드 자체로 표현)

```python
# Good: 이유를 설명
# Gemini API 응답이 빈 문자열일 수 있어 기본값 처리
question = response.text or "질문을 생성하지 못했습니다."

# Bad: 코드를 그대로 반복
# question에 response.text를 할당
question = response.text
```
