# 🎯 Project Specific Context: Python-FastAPI-MariaDB

## 📋 Custom Rules
- **README Update Rule**: 기능이 추가되거나 수정될 때마다 해당 내용에 맞춰 **`README.md` 파일을 즉시 업데이트**할 것. (포트폴리오 완성도를 높이기 위함)
- **Tech Goal**: Spring Boot의 구조를 FastAPI에 잘 이식하면서도 파이썬스러운(Pythonic) 코드를 지향함.

## 🏗 Project Architecture
- **Layered Architecture**: Router ➡️ Service ➡️ Repository ➡️ Model
- **Auth**: JWT based authentication with BCrypt hashing.
- **Environment**: Managed via `.env` and `pydantic-settings`.
