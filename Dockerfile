# Используем официальный Python-образ
FROM python:3.12

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /DummyJsonAPI

# Копируем файлы проекта в контейнер
COPY . .

# Обновляем pip и устанавливаем зависимости
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Указываем команду, которая будет запускаться по умолчанию
# Например, запуск функциональных тестов
CMD ["pytest", "tests/functional", "--alluredir=reports/allure-results"]