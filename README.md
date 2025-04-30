🧪 DummyJson API  Testing

Проект по автоматизации тестирования публичного API [DummyJSON](https://dummyjson.com), реализованный с использованием `pytest`, `requests`, `allure` и `pydantic`. Архитектура построена по паттерну Page Object для API.

## 📁 Структура проекта
```
DummyJsonAPI/
│
├── logs/                  # Логи выполнения тестов
├── reports/               # Allure отчёты
│   └── allure-results/
├── schemas/               # Pydantic-схемы для валидации ответов
├── src/
│   └── api/               # Базовые и специфические API-классы
├── tests/
│   ├── functional/        # Основные функциональные тесты
│   └── conftest.py        # Общие фикстуры и настройки
├── Dockerfile             # Docker-инструкция для запуска тестов
├── pytest.ini             # Pytest настройки
└── requirements.txt       # Зависимости проекта
```

---

## 🧰 Стек технологий

- **Python 3.10+**
- **Pytest** — фреймворк для тестирования
- **Requests** — HTTP-клиент
- **Allure** — генерация отчетов
- **Pydantic** — валидация схем
- **Page Object (API)** — паттерн организации API-классов

---
## 📌 Эндпоинты, покрытые тестами

- `auth/login`
- `products`
- `posts`
- `comments`
- `users`
- `carts`
- `todos`

Для каждого из них реализованы:
- Позитивные тесты
- Негативные тесты
- Проверка структуры ответа через Pydantic-схемы

## 🚀 Быстрый старт

### 1. Клонирование

```bash
git clone https://github.com/Otto-debug/DummyJson.git
cd DummyJsonAPI

