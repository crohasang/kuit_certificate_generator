# 📜 KUIT Certificate Generator
KUIT(건국대학교 기획/개발 동아리) 수료증 자동 생성 프로그램

## 📁 프로젝트 구조

```
kuit-certificate/
│
├── script.py            # 메인 생성 스크립트
│
├── template/
│   └── template.pdf     # 수료증 템플릿 (gitignore에 포함)
│
├── assets/
│   └── fonts/
│       └── NanumMyeongjoBold.ttf  # 나눔명조 볼드체
│
├── data/
│   └── data.json          # 수료생 정보 (gitignore에 포함)
│
├── output/
│   └── certificates/      # 생성된 PDF 파일들 (gitignore에 포함)
│
├── requirements.txt       # 파이썬 패키지 의존성
└── README.md
```

## 🚀 설치 방법

1. 가상환경 생성
```bash
python3 -m venv venv
```

2. 가상환경 활성화
- Windows:
```bash
.\venv\Scripts\activate
```
- macOS/Linux:
```bash
source venv/bin/activate
```

3. 필요한 패키지 설치
```bash
pip install -r requirements.txt
```

## 💻 사용 방법

1. `data/data.json` 파일에 수료생 정보를 입력합니다.
2. `template/template.pdf`에 수료증 템플릿을 넣습니다.
3. 스크립트를 실행합니다:
```bash
python script.py
```
4. 생성된 수료증은 `output/certificates/` 디렉토리에서 확인할 수 있습니다.

## 📋 데이터 포맷 (data.json)

```json
[
    {
        "project": "프로젝트명",
        "members": [
            {
                "part": "파트",
                "name": "이름"
            }
        ]
    }
]
```

## ⚠️ 주의사항
- `venv/` 디렉토리와 `data/data.json`, `template/template.pdf` 파일은 git에 포함되지 않습니다.
- 프로젝트를 새로 받은 경우 가상환경을 생성하고 패키지를 설치해야 합니다.
- 프로젝트를 새로 받은 경우 수료증 템플릿 파일을 `template/template.pdf`에 넣어야 합니다.
