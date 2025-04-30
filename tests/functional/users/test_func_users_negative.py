import allure
import pytest
from http import HTTPStatus

@pytest.mark.negative
@allure.epic("Функциональное тестирование пользователей")
@allure.feature("Негативные тесты")

class TestUsersNegative:

    @allure.story('Получение одного пользователя')
    @pytest.mark.parametrize("user_id, expected_status", [

        # ❌ Негативные кейсы
        (0, HTTPStatus.NOT_FOUND),
        ("((@*@(@(@(@", HTTPStatus.BAD_REQUEST),
        (-1, HTTPStatus.NOT_FOUND),
        ("text", HTTPStatus.BAD_REQUEST),
        (99.99, HTTPStatus.NOT_FOUND),
        (99999, HTTPStatus.NOT_FOUND)

    ])
    def test_get_user(self, users_api, user_id, expected_status, logger):
        with allure.step(f"Отправляю GET-запрос к эндпоинту /users/{user_id}"):
            response = users_api.get_user(user_id)
            logger.info(f"Ответ: {response.status_code} - тело запроса - {response.text}")
            assert response.status_code == expected_status, (f"Ожидался статус: {expected_status},"
                                                             f"но получен: {response.status_code}")

    @pytest.mark.xfail(reason="dummyjson не валидирует данные, даже невалидные проходят")
    @allure.story('Создание пользователя')
    @pytest.mark.parametrize("user_data, expected_status", [
        # ❌ Отрицательный возраст
        ({
             "firstName": "Negative",
             "lastName": "Age",
             "age": -5
         }, HTTPStatus.BAD_REQUEST),

        # ❌ Пустое имя
        ({
             "firstName": "",
             "lastName": "NoName",
             "age": 20
         }, HTTPStatus.BAD_REQUEST),

        # ❌ Невалидный email
        ({
             "firstName": "Bad",
             "lastName": "Email",
             "age": 25,
             "email": "not-an-email"
         }, HTTPStatus.BAD_REQUEST),

        # ❌ Некорректный URL изображения
        ({
             "firstName": "Invalid",
             "lastName": "Image",
             "age": 40,
             "image": "not-a-url"
         }, HTTPStatus.BAD_REQUEST),

        # ❌ SQL-инъекция
        ({
             "firstName": "' OR 1=1; --",
             "lastName": "Hacker",
             "age": 35
         }, HTTPStatus.BAD_REQUEST),

        # ❌ XSS-атака
        ({
             "firstName": "<script>alert('xss')</script>",
             "lastName": "XSS",
             "age": 19
         }, HTTPStatus.BAD_REQUEST),

        # ❌ Пустой словарь
        ({}, HTTPStatus.BAD_REQUEST),

        # ❌ Лишние поля
        ({
             "firstName": "Extra",
             "lastName": "Field",
             "age": 29,
             "unknownField": "???"
         }, HTTPStatus.BAD_REQUEST),
    ])
    def test_create_user(self, users_api, user_data, expected_status, logger):
        with allure.step(f'Отправляю POST - запрос на эндпоинт /users/add с параметрами: {user_data}'):
            response = users_api.create_user(user_data)
            logger.info(f'POST - запрос на эндпоинт /users/add')
            logger.info(f'Ответ: {response.status_code} тело запроса: {response.text}')
            assert response.status_code == expected_status, (f"Ожидался статус: {expected_status},"
                                                             f"но получен: {response.status_code}")

    @pytest.mark.xfail(reason="dummyjson не валидирует данные, даже невалидные проходят")
    @allure.story("Обновление пользователя")
    @pytest.mark.parametrize("user_id, updated_user, expected_status", [

        # ❌ Негативные кейсы
        (9999, {"firstName": "Ghost"}, HTTPStatus.NOT_FOUND),  # несуществующий пользователь
        (4, {}, HTTPStatus.OK),  # API всё равно вернёт 200/OK (dummyjson не валидирует)
        (3, {"age": "not-a-number"}, HTTPStatus.OK),  # невалидный тип, но dummyjson примет
        (6, {"unknownField": "some value"}, HTTPStatus.OK),  # лишнее поле
        (2, {"firstName": "<script>alert('xss')</script>"}, HTTPStatus.OK),  # XSS
        (1, {"firstName": "' OR 1=1 --"}, HTTPStatus.OK),  # SQL-инъекция
    ])
    def test_update_user(self, users_api, user_id, updated_user, expected_status, logger):
        with allure.step(f'Отправляю PUT - запрос к эндпоинту /users/{user_id} с параметрами: {updated_user}'):
            response = users_api.update_user(user_id=user_id, user_data=updated_user)
            logger.info(f"PUT - запрос к эндпоинту /users/{user_id}")
            logger.info(f"Ответ: {response.status_code} - {response.text}")
            assert response.status_code == expected_status, (f"Ожидался статус: {expected_status},"
                                                             f"но получен: {response.status_code}")

    @allure.story("Удаление пользователя")
    @pytest.mark.parametrize("user_id, expected_status", [
        (9999, HTTPStatus.NOT_FOUND),
        (0, HTTPStatus.NOT_FOUND)
    ])
    def test_delete_user(self, users_api, user_id, expected_status, logger):
        with allure.step(f"Отправляю DELETE-запрос на эндпоинт /users{user_id}"):
            response = users_api.delete_user(user_id)
            logger.info(f"Ответ: {response.status_code} - {response.text}")
            assert response.status_code == expected_status, (f"Ожидался статус: {expected_status},"
                                                             f"но получен: {response.status_code}")
