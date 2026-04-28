# TWOTIMESS Design System

이 폴더는 `/Users/twotimess/Desktop/Climate` 프로젝트에서 사용한 UX/UI 스타일을
다른 프로젝트에도 거의 같은 결로 옮길 수 있도록 정리한 공유용 패키지입니다.

## 포함 파일

- `tokens.css`
  - 색상, 타이포, 간격, 보더, 레이아웃 폭 같은 기본 토큰
- `base.css`
  - 전역 reset, body, 기본 링크/텍스트 규칙
- `components.css`
  - 버튼, 패널, 탭, 칩, 표, 각주, 차트 패널 같은 공통 컴포넌트
- `patterns.css`
  - hero, section heading, 검색/정렬 바, 카드 레이아웃 같은 조합 패턴
- `example.html`
  - 이 시스템을 적용한 최소 예시 화면
- `CODEX_HANDOFF.md`
  - 다른 Codex에게 그대로 전달할 수 있는 적용 지침
- `GRAPH_AND_EXAM_GUIDE.md`
  - 그래프 선택, 통계 표시, 시험형 문제 설계에 대한 실전 가이드
- `HUMAN_GEOGRAPHY_GUIDE.md`
  - 인문지리 프로젝트에서 같은 톤앤매너를 유지하면서 정보 구조를 바꾸는 가이드

## 핵심 원칙

1. 시각 톤은 `흑백 + 연한 종이색 배경`을 기본으로 합니다.
2. 모서리는 둥글리지 않고 `직각`을 유지합니다.
3. `Pretendard` 계열을 기본 폰트로 사용합니다.
4. 제목은 크고 강하게, 본문은 차분하게 구성합니다.
5. 패널은 `1px` 보더로만 구분하고, 그림자와 그라데이션은 쓰지 않습니다.
6. 차트는 화려한 색보다 `검정/회색 대비`로 읽히게 합니다.
7. 정보성 앱 구조를 우선합니다.
   - `Hero -> Controls -> Main Content -> Comparison/Detail`

## 비주얼 규칙

- 배경색: `#efefec`
- 본문색: `#111111`
- 보조 텍스트: `#666666`
- 보더: `1px solid #111111`
- 보조 보더: `#d6d6d6`, `#e7e7e7`
- radius: `0`
- shadow: `none`

## 컴포넌트 목록

- `tw-panel`
- `tw-hero`
- `tw-eyebrow`
- `tw-switch`
- `tw-button`
- `tw-chip`
- `tw-badge`
- `tw-field`
- `tw-table`
- `tw-chart-panel`
- `tw-footnotes`

## 다른 프로젝트에 적용하는 순서

1. `tokens.css`, `base.css`, `components.css`, `patterns.css`를 복사합니다.
2. 새 프로젝트의 레이아웃을 semantic section으로 나눕니다.
3. 기존 UI를 새로 그리려 하지 말고, 먼저 `tw-hero`, `tw-panel`, `tw-section-heading`,
   `tw-controls-grid`, `tw-card-grid`에 끼워 맞춥니다.
4. 마지막에 필요한 부분만 토큰 단위로 조정합니다.
5. 프로젝트별 개성은 색이 아니라 `콘텐츠 구조와 데이터 표현`에서 줍니다.

## Codex 전달 팁

다른 Codex에게는 다음 두 가지를 함께 보내는 것이 좋습니다.

1. `design-system/` 폴더 전체
2. `CODEX_HANDOFF.md` 내용
3. 시험형 화면이나 교육용 앱이면 `GRAPH_AND_EXAM_GUIDE.md`도 같이 전달
4. 인문지리 프로젝트면 `HUMAN_GEOGRAPHY_GUIDE.md`도 같이 전달

이 조합이면 "느낌만 비슷하게"가 아니라 "같은 시스템으로 구현"하는 데 훨씬 유리합니다.

## 빠른 체크리스트

- Pretendard가 적용되었는가
- 배경이 너무 하얗거나 너무 어둡지 않은가
- 그림자, 글래스, 그라데이션이 들어가지 않았는가
- 버튼과 칩이 둥글지 않은가
- 제목과 섹션 위계가 분명한가
- 표와 그래프의 보더, 축, 각주 톤이 일관적인가
- 모바일에서 제목 줄바꿈이 깨지지 않는가
- 모든 spacing이 토큰 단위 안에서 움직이는가
