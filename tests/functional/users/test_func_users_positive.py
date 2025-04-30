import time
import allure
import pytest
from http import HTTPStatus

from pydantic import ValidationError
from schemas.users_schema import User

@pytest.mark.positive
@allure.epic("Функциональное тестирование пользователей")
@allure.feature("Позитивные кейсы")
class TestUsersPositive:

    @allure.story("Получение пользователя")
    @pytest.mark.parametrize("user_id, expected_status", [
        # ✅ Позитивные кейсы
        (1, HTTPStatus.OK),
        (2, HTTPStatus.OK)
    ])
    def test_get_user(self, users_api, user_id, expected_status, logger):
        with allure.step(f"Отправляю GET-запрос к эндпоинту /users/{user_id}"):
            response = users_api.get_user(user_id)
            logger.info(f"Ответ: {response.status_code} - {response.text}")
            assert response.status_code == expected_status, (f"Ожидался статус: {expected_status},"
                                                             f"но получен: {response.status_code}")

        if response.status_code == HTTPStatus.OK:
            with allure.step('Проверка валидации данных'):
                try:
                    user_data = User(**response.json())
                    logger.info('Данные провалидированы')
                    assert user_data.id == user_id, f"ID пользователя в ответе: {user_id}"
                except ValidationError as e:
                    logger.error(f"Ошибка валидации данных пользователя: {e}")
                    pytest.fail(f'Ошибка валидации: {e}')

    @allure.story("Создание пользователя")
    @pytest.mark.parametrize("user_data, expected_status", [
        # ✅ Позитивные кейсы
        ({
             "firstName": "Tommy",
             "lastName": "Shelm",
             "age": 22
         }, HTTPStatus.CREATED),
        ({
             "firstName": "Anna",
             "lastName": "Smith",
             "age": 30,
             "gender": "female",
             "email": "anna.smith@example.com",
             "phone": "+1 234 567 89",
             "username": "anna30",
             "password": "pass1234",
             "birthDate": "1994-01-01",
             "image": "https://example.com/image.jpg"
         }, HTTPStatus.CREATED),
        ({
             "firstName": "Jake",
             "lastName": "Long",
             "age": 28,
             "gender": "male"
         }, HTTPStatus.CREATED),

    ])
    def test_create_user(self, users_api, user_data, expected_status, logger):
        with allure.step(f'Отправляю POST-запрос к эндпоинту /users/add с параметрами: {user_data}'):
            response = users_api.create_user(user_data)
            logger.info(f"Ответ: {response.status_code} - {response.status_code}")
            assert response.status_code == expected_status, (f"Ожидался статус: {expected_status},"
                                                             f"но получен: {response.status_code}")

        if response.status_code == HTTPStatus.CREATED:
            with allure.step('Проверка валидации данных'):
                try:
                    data = User(**response.json())
                    logger.info('Данные провалидированы')
                except ValidationError as e:
                    logger.error(f'Ошибка валидации данных: {e}')
                    pytest.fail(f"Ошибка валидации: {e}")

    @allure.story("Обновление пользователя")
    @pytest.mark.parametrize("user_id, updated_user, expected_status", [
        # ✅ Позитивные кейсы
        (5, {"firstName": "John", "lastName": "Doe"}, HTTPStatus.OK),
        (7, {"age": 45}, HTTPStatus.OK),
        (8, {"gender": "female", "email": "test@example.com"}, HTTPStatus.OK),
        (9, {"phone": "+1234567890", "birthDate": "1985-06-15"}, HTTPStatus.OK),
    ])
    def test_update_user(self, users_api, user_id, updated_user, expected_status, logger):
        with allure.step(f"Отправляю PUT-запрос к эндпоинту /users/{user_id}"):
            response = users_api.update_user(user_id=user_id, user_data=updated_user)
            logger.info(f"Ответ: {response.status_code} - {response.text}")
            assert response.status_code == expected_status, (f"Ожидался статус: {expected_status},"
                                                             f"но получен: {response.status_code}")

        if response.status_code == expected_status:
            with allure.step('Проверка валидации данных'):
                try:
                    user_data = response.json()
                    validated_user = User(**user_data)
                    logger.info('Данные провалидированы')
                except ValidationError as e:
                    logger.error(f"Ошибка валидации данных: {e}")
                    pytest.fail(f"Ошибка валидации")

    @allure.story("Удаление пользователя")
    @pytest.mark.parametrize("user_id, expected_status", [
        # ✅ Позитивные кейсы
        (1, HTTPStatus.OK),
        (2, HTTPStatus.OK)
    ])
    def test_delete_user(self, users_api, user_id, expected_status, logger):
        with allure.step(f"Отправляю DELETE-запрос на эндпоинт /users{user_id}"):
            response = users_api.delete_user(user_id)
            logger.info(f"Ответ: {response.status_code} - {response.text}")
            assert response.status_code == expected_status, (f"Ожидался статус: {expected_status},"
                                                             f"но получен: {response.status_code}")

        if response.status_code == HTTPStatus.OK:
            with allure.step('Проверка валидации данных'):
                try:
                    delete_user = User(**response.json())
                    logger.info(f"Пользователь удалён: {delete_user.id}")
                except ValidationError as e:
                    logger.error(f"Ошибка валидации данных: {e}")
                    pytest.fail(f"Ошибка валидации: {e}")

            with allure.step("Проверка, что задача действительно удалена"):
                timeout = 5
                interval = 0.5
                elapsed = 0
                while elapsed < timeout:
                    get_resp = users_api.get_user(user_id)
                    if get_resp.status_code == HTTPStatus.NOT_FOUND:
                        logger.info(f"Пользователь с id={user_id} успешно удалена")
                        break
                    time.sleep(interval)
                    elapsed += interval
                else:
                    pytest.fail(f"Пользователь с id={user_id} всё ещё существует спустя {timeout} секунд")


