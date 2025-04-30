import time
import allure
import pytest
from http import HTTPStatus

from pydantic import ValidationError
from schemas.products_schema import Product, ProductCreate


@pytest.mark.positive
@allure.epic("Функциональное тестирование продуктов")
@allure.feature("Позитивные кейсы")
class TestProductsPositive:

    @allure.story('Получение одного продукта')
    @pytest.mark.parametrize("product_id, expected_status", [
        # ✅ Позитивные кейсы
        (1, HTTPStatus.OK),
        (111, HTTPStatus.OK),
    ])
    def test_get_product(self, products_api, product_id, expected_status, logger):
        with allure.step(f'Отправляю GET-запрос к эндпоинту /products/{product_id}'):
            response = products_api.get_product(product_id)
            logger.info(f'GET-запрос к эндпоинту /products/{product_id}')
            logger.info(f'Ответ: {response.status_code} - {response.text}')
            assert response.status_code == expected_status, (f"Ожидался статус: {expected_status},"
                                                             f"но получен: {response.status_code}")

        if response.status_code == HTTPStatus.OK:
            with allure.step('Проверка валидации данных'):
                try:
                    product_data = Product(**response.json())
                    logger.info('Данные провалидированы')
                except ValidationError as e:
                    logger.error(f"Ошибка валидации данных: {e}")
                    pytest.fail(f'Ошибка валидации: {e}')

    @allure.story("Создание продукта")
    @pytest.mark.parametrize("product_data, expected_status", [
        # ✅ Позитивные кейсы
        ({'title': "Machine"}, HTTPStatus.CREATED),
        ({'title': "Car"}, HTTPStatus.CREATED),
    ])
    def test_create_product_positive(self, products_api, product_data, expected_status, logger):
        with allure.step(f'Отправляем POST-запрос к эндпоинту /products/add с параметрами: {product_data}'):
            response = products_api.create_product(product_data=product_data)
            logger.info(f'POST-запрос к эндпоинту /products/add с параметрами: {product_data}')
            logger.info(f'Ответ: {response.status_code} - {response.text}')
            assert response.status_code == expected_status, (f"Ожидался статус: {expected_status},"
                                                             f"но получен: {response.status_code}")

        if response.status_code == HTTPStatus.CREATED:
            with allure.step("Проверка валидации данных"):
                try:
                    product_data = ProductCreate(**response.json())
                    logger.info("Данные провалидированы")
                except ValidationError as e:
                    logger.error(f"Ошибка валидации данных: {e}")
                    pytest.fail(f"Ошибка валидации: {e}")

    @allure.story("Обновление продукта")
    @pytest.mark.parametrize("product_id, update_product, expected_status", [
        # ✅ Позитивные кейсы
        (1, {"title": "New Title"}, HTTPStatus.OK),
        (2, {"title": "New Car"}, HTTPStatus.OK)
    ])
    def test_update_product(self, products_api, product_id, update_product, expected_status, logger):
        with allure.step(f'Отправляю PUT-запрос на эндпоинт /products/{product_id}'):
            response = products_api.update_product(product_id=product_id, product_data=update_product)
            logger.info(f'Ответ: {response.status_code} - {response.text}')
            assert response.status_code == expected_status, (f"Ожидался статус: {expected_status},"
                                                             f"но получен: {response.status_code}")

        if response.status_code == HTTPStatus.OK:
            with allure.step('Проверка валидации данных'):
                try:
                    product_data = response.json()
                    validate_product = Product(**product_data)
                    logger.info('Данные провалидированы')
                except ValidationError as e:
                    logger.error(f"Ошибка валидации данных пользователей: {e}")
                    pytest.fail(f"Ошибка валидации: {e}")

            with allure.step('Проверка, что поля обновились'):
                for key, value in update_product.items():
                    assert getattr(validate_product, key) == value, f"Поле {key} не обновилось правильно"

    @allure.story("Удаление продукта")
    @pytest.mark.parametrize("product_id, expected_status", [
        # ✅ Позитивные кейсы
        (1, HTTPStatus.OK),
        (12, HTTPStatus.OK)
    ])
    def test_delete_product(self, products_api, product_id, expected_status, logger):
        with allure.step(f"Отправляю DELETE-запрос к эндпоинту /products/{product_id}"):
            response = products_api.delete_product(product_id=product_id)
            logger.info(f"Ответ: {response.status_code} - {response.text}")
            assert response.status_code == expected_status, (f"Ожидался статус: {expected_status},"
                                                             f"но пришел: {response.status_code}")

        if response.status_code == HTTPStatus.OK:
            with allure.step('Проверка валидации данных'):
                try:
                    delete_product = Product(**response.json())
                    logger.info(f"Удалён продукт: {delete_product}")
                except ValidationError as e:
                    logger.error(f"Ошибка валидации данных: {e}")
                    pytest.fail(f"Ошибка валидации")

            with allure.step("Проверка, что карточка действительно удалена"):
                timeout = 5
                interval = 0.5
                elapsed = 0
                while elapsed < timeout:
                    get_resp = products_api.get_product(product_id)
                    if get_resp.status_code == HTTPStatus.NOT_FOUND:
                        logger.info(f"Продукт с id={product_id} успешно удален")
                        break
                    time.sleep(interval)
                    elapsed += interval
                else:
                    pytest.fail(f"Продукт с id={product_id} все ещё существует спустя {timeout} секунд")
