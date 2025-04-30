import allure
import pytest
from http import HTTPStatus

@pytest.mark.negative
@allure.epic("Функциональное тестирование карточек")
@allure.feature("Негативные кейсы")

class TestCartsNegative:

    @allure.story("Получение одной карточки")
    @pytest.mark.parametrize("cart_id, expected_status", [
        # ❌ Негативные кейсы
        (0, HTTPStatus.NOT_FOUND),
        (-1, HTTPStatus.NOT_FOUND),
        (99999, HTTPStatus.NOT_FOUND),
        ("text", HTTPStatus.NOT_FOUND),
        ("((@*@(@(@(@", HTTPStatus.NOT_FOUND),
        (99.99, HTTPStatus.NOT_FOUND),
        (None, HTTPStatus.NOT_FOUND),
        (True, HTTPStatus.NOT_FOUND),
        ([], HTTPStatus.NOT_FOUND),
        ({}, HTTPStatus.NOT_FOUND),
    ])
    def test_get_cart(self, carts_api, cart_id, expected_status, logger):
        with allure.step(f"Отправляю GET-запрос к энпдоинту /carts/{cart_id}"):
            response = carts_api.get_cart(cart_id=cart_id)
            logger.info(f"Ответ: {response.status_code} - {response.text}")
            assert response.status_code == expected_status, (f"Ожидал ответ: {expected_status},"
                                                             f"но получил: {response.status_code}")

    @pytest.mark.xfail(reason="dummyjson не валидирует данные, даже невалидные проходят")
    @allure.story("Создание карточки")
    @pytest.mark.parametrize("cart_data, expected_status", [
        # ❌ Негативные кейсы
        ({
             "userId": 0,
             "products": [""]
         }, HTTPStatus.BAD_REQUEST),

        ({
             "userId": "",
             "products": [
                 {"id": -1, "quantity": 0 / 5}
             ]
         }, HTTPStatus.BAD_REQUEST),

        ({}, HTTPStatus.BAD_REQUEST),

        ({
             "userId": None,
             "products": [{"id": 1, "quantity": 1}]
         }, HTTPStatus.BAD_REQUEST),

        ({
             "userId": 1,
             "products": None
         }, HTTPStatus.BAD_REQUEST),

        ({
             "userId": 1,
             "products": []
         }, HTTPStatus.BAD_REQUEST),

        ({
             "userId": 1,
             "products": [{"id": 1, "quantity": "a lot"}]
         }, HTTPStatus.BAD_REQUEST),

        ({
             "userId": 1,
             "products": [{}]
         }, HTTPStatus.BAD_REQUEST),

        ({
             "userId": 1,
             "products": [{"id": 1}]
         }, HTTPStatus.BAD_REQUEST),

        ({
             "userId": 1,
             "products": [{"quantity": 1}]
         }, HTTPStatus.BAD_REQUEST),

        ({
             "userId": 1,
             "products": [{"id": 1, "quantity": -5}]
         }, HTTPStatus.BAD_REQUEST),

        ({
             "userId": 1,
             "products": [{"id": "abc", "quantity": 1}]
         }, HTTPStatus.BAD_REQUEST),

        ({
             "userId": 1,
             "products": [
                 {"id": 1, "quantity": 1},
                 {"id": 1, "quantity": 2}
             ]
         }, HTTPStatus.BAD_REQUEST),
    ])
    def test_create_cart(self, carts_api, cart_data, expected_status, logger):
        with allure.step(f"Отправляю POST-запрос к эндпоинту /carts/add с параметрами: {cart_data}"):
            response = carts_api.create_cart(cart_data=cart_data)
            logger.info(f"Ответ: {response.status_code} - {response.text}")
            assert response.status_code == expected_status, (f"Ожидался ответ: {expected_status},"
                                                             f"но получен: {response.status_code}")

    @pytest.mark.xfail(reason="dummyjson не валидирует данные, даже невалидные проходят")
    @allure.story("Обновление карточки")
    @pytest.mark.parametrize("cart_id, updated_data, expected_status", [
        (1, {}, HTTPStatus.BAD_REQUEST),
        (1, {"userId": 1}, HTTPStatus.BAD_REQUEST),
        (1, {"products": [{"id": 1, "quantity": 2}]}, HTTPStatus.BAD_REQUEST),

        # ❌ Некорректные значения userId
        (1, {"userId": "", "products": [{"id": 1, "quantity": 2}]}, HTTPStatus.BAD_REQUEST),
        (1, {"userId": "text", "products": [{"id": 1, "quantity": 2}]}, HTTPStatus.BAD_REQUEST),
        (1, {"userId": None, "products": [{"id": 1, "quantity": 2}]}, HTTPStatus.BAD_REQUEST),

        # ❌ Некорректные значения products
        (1, {"userId": 1, "products": ""}, HTTPStatus.BAD_REQUEST),
        (1, {"userId": 1, "products": []}, HTTPStatus.BAD_REQUEST),
        (1, {"userId": 1, "products": [{}]}, HTTPStatus.BAD_REQUEST),
        (1, {"userId": 1, "products": [{"id": "abc", "quantity": 1}]}, HTTPStatus.BAD_REQUEST),
        (1, {"userId": 1, "products": [{"id": 1, "quantity": "five"}]}, HTTPStatus.BAD_REQUEST),
        (1, {"userId": 1, "products": [{"id": None, "quantity": 2}]}, HTTPStatus.BAD_REQUEST),

        # ❌ Комбинированные некорректные значения
        (1, {"userId": 0, "products": [""]}, HTTPStatus.BAD_REQUEST),
        (2, {"userId": "", "products": [{"id": -1, "quantity": 0 / 5}]}, HTTPStatus.BAD_REQUEST)
    ])
    def test_update_cart(self, carts_api, cart_id, updated_data, expected_status, logger):
        with allure.step(f"Отправляю PUT-запрос к эндпоинту /carts/{cart_id} с параметрами: {updated_data}"):
            response = carts_api.update_cart(cart_id=cart_id, cart_data=updated_data)
            logger.info(f"Ответ: {response.status_code} - {response.text}")
            assert response.status_code == expected_status, (f"Ожидался статус: {expected_status},"
                                                             f"но получен: {response.status_code}")

    @allure.story("Удаление пользователя")
    @pytest.mark.parametrize("cart_id, expected_status", [
        # ❌ Негативные кейсы
        (0, HTTPStatus.NOT_FOUND),
        (9999, HTTPStatus.NOT_FOUND),
        (-1, HTTPStatus.NOT_FOUND)
    ])
    def test_delete_cart(self, carts_api, cart_id, expected_status, logger):
        with allure.step(f"Отправляю DELETE-запрос к эндпоинту /carts/{cart_id}"):
            response = carts_api.delete_cart(cart_id)
            logger.info(f"Ответ: {response.status_code} - {response.text}")
            assert response.status_code == expected_status, (f"Ожидался ответ: {expected_status},"
                                                             f"но получен: {response.status_code}")