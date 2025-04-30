import time
import allure
import pytest
from http import HTTPStatus

from pydantic import ValidationError
from schemas.carts_schema import CartGET, CartPOSTPUT


@pytest.mark.positive
@allure.epic("Функциональное тестирование карточек")
@allure.feature("Позитивные кейсы")
class TestCartsPositive:

    @allure.story("Получение карточки")
    @pytest.mark.parametrize("cart_id, expected_status", [
        # ✅ Позитивные кейсы
        (1, HTTPStatus.OK),
        (2, HTTPStatus.OK),
        (100, HTTPStatus.OK),
        (3, HTTPStatus.OK),
        (20, HTTPStatus.OK),
    ])
    def test_get_cart(self, carts_api, cart_id, expected_status, logger):
        with allure.step(f"Отправляю GET-запрос к эндпоинту /carts/{cart_id}"):
            response = carts_api.get_cart(cart_id)
            logger.info(f"Ответ: {response.status_code} - {response.text}")
            assert response.status_code == expected_status, (f"Ожидался статус: {expected_status},"
                                                             f"но получен: {response.status_code}")

        if response.status_code == HTTPStatus.OK:
            with allure.step('Проверка валидации данных'):
                try:
                    cart_data = CartGET(**response.json())
                    logger.info('Данные провалидированы')
                    assert cart_data.id == cart_id, f"ID карточки в ответе: {cart_id}"
                except ValidationError as e:
                    logger.error(f"Ошибка валидации данных: {e}")
                    pytest.fail(f"Ошибка валидации")

    @allure.story("Создание карточки")
    @pytest.mark.parametrize("cart_data, expected_status", [
        # ✅ Позитивные кейсы
        (
                {
                    "userId": 1,
                    "products": [
                        {"id": 1, "quantity": 2},
                        {"id": 50, "quantity": 1}
                    ]
                },
                HTTPStatus.CREATED
        ),
        (
                {
                    "userId": 2,
                    "products": [
                        {"id": 10, "quantity": 5}
                    ]
                },
                HTTPStatus.CREATED
        ),

        (
                {
                    "userId": 3,
                    "products": [{"id": 2, "quantity": 1}]
                },
                HTTPStatus.CREATED
        ),
        (
                {
                    "userId": 4,
                    "products": [{"id": i, "quantity": 1} for i in range(1, 11)]  # массив из 10 товаров
                },
                HTTPStatus.CREATED
        ),
        (
                {
                    "userId": 5,
                    "products": [
                        {"id": 1, "quantity": 2},
                        {"id": 1, "quantity": 3}
                    ]
                },
                HTTPStatus.CREATED
        ),
    ])
    def test_create_cart(self, carts_api, cart_data, expected_status, logger):
        with allure.step(f"Отправляю POST-запрос к эндпоинту /carts/add с параметрами: {cart_data}"):
            response = carts_api.create_cart(cart_data=cart_data)
            logger.info(f"Ответ: {response.status_code} - {response.text}")
            assert response.status_code == expected_status, (f"Ожидался статус: {expected_status},"
                                                             f"но пришел: {response.status_code}")

        if response.status_code == HTTPStatus.CREATED:
            try:
                data = CartPOSTPUT(**response.json())
                logger.info(f"Данные провалидированы")
            except ValidationError as e:
                logger.error(f"Ошибка валидации данных: {e}")
                pytest.fail(f"Ошибка валидации: {e}")

    @allure.story("Обновление карточки")
    @pytest.mark.parametrize("cart_id, update_cart, expected_status", [
        # ✅ Позитивные кейсы
        (
                1,
                {
                    "products": [
                        {"id": 1, "quantity": 4},
                        {"id": 100, "quantity": 2}
                    ]
                },
                HTTPStatus.OK
        ),
        (
                2,
                {
                    "products": [
                        {"id": 5, "quantity": 1}
                    ]
                },
                HTTPStatus.OK
        ),
        (
                1,
                {
                    "products": [{"id": 3, "quantity": 1}]
                },
                HTTPStatus.OK
        ),

        (
                1,
                {
                    "products": [{"id": i, "quantity": 1} for i in range(1, 6)]
                },
                HTTPStatus.OK
        ),
        (
                1,
                {
                    "products": [
                        {"id": 1, "quantity": 4},
                        {"id": 100, "quantity": 2}
                    ]
                },
                HTTPStatus.OK
        ),
    ])
    def test_update_cart(self, carts_api, cart_id, update_cart, expected_status, logger):
        with allure.step(f"Отправляю PUT-запрос к эндпоинту /carts/{cart_id} с обновленными: {update_cart}"):
            response = carts_api.update_cart(cart_id=cart_id, cart_data=update_cart)
            logger.info(f"Ответ: {response.status_code} - {response.text}")
            assert response.status_code == expected_status, (f"Ожидался ответ: {expected_status}, "
                                                             f"но пришел: {response.status_code}")

        if response.status_code == HTTPStatus.OK:
            with allure.step("Проверка валидации данных"):
                try:
                    data = CartPOSTPUT(**response.json())
                    logger.info('Данные провалидированы')
                except ValidationError as e:
                    logger.error(f"Ошибка валидации данных: {e}")
                    pytest.fail(f"Ошибка валидации: {e}")

    @allure.story("Удаление карточки")
    @pytest.mark.parametrize("cart_id, expected_status", [
        # ✅ Позитивные кейсы
        (1, HTTPStatus.OK),
        (22, HTTPStatus.OK)
    ])
    def test_delete_cart(self, carts_api, cart_id, expected_status, logger):
        with allure.step(f"Отправляю DELETE-запрос к эндпоинту /carts/{cart_id}"):
            response = carts_api.delete_cart(cart_id=cart_id)
            logger.info(f"Ответ: {response.status_code} - {response.text}")
            assert response.status_code == expected_status, (f"Ожидался ответ: {expected_status},"
                                                             f"но получен: {response.status_code}")

        if response.status_code == HTTPStatus.OK:
            with allure.step('Проверка валидации данных'):
                try:
                    delete_user = CartGET(**response.json())
                    logger.info(f"Карточка удалена: {delete_user}")
                except ValidationError as e:
                    logger.error(f"Ошибка валидации данных: {e}")
                    pytest.fail(f"Ошибка валидации: {e}")

            with allure.step("Проверка, что карточка действительно удалена"):
                timeout = 5
                interval = 0.5
                elapsed = 0
                while elapsed < timeout:
                    get_resp = carts_api.get_cart(cart_id)
                    if get_resp.status_code == HTTPStatus.NOT_FOUND:
                        logger.info(f"Карточка с id={cart_id} успешно удалена")
                        break
                    time.sleep(interval)
                    elapsed += interval
                else:
                    pytest.fail(f"Карточка с id={cart_id} все ещё существует спустя {timeout} секунд")