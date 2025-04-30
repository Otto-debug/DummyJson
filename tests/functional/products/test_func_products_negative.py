import allure
import pytest
from http import HTTPStatus

@pytest.mark.negative
@allure.epic("Функциональное тестирование продуктов")
@allure.feature("Негативные кейсы")
class TestProductsNegative:

    @allure.story("Получение одного продукта")
    @pytest.mark.parametrize("product_id, expected_status", [
        # ❌ Негативные кейсы
        (0, HTTPStatus.NOT_FOUND),
        ("((@*@(@(@(@", HTTPStatus.NOT_FOUND),
        (-1, HTTPStatus.NOT_FOUND),
        ("text", HTTPStatus.NOT_FOUND),
        (99.99, HTTPStatus.NOT_FOUND),
        (99999, HTTPStatus.NOT_FOUND)
    ])
    def test_get_product(self, products_api, product_id, expected_status, logger):
        with allure.step(f"Отправляю GET-запрос на эндпоинт /products/{product_id}"):
            response = products_api.get_product(product_id=product_id)
            logger.info(f"Ответ: {response.status_code} - {response.text}")
            assert response.status_code == expected_status, (f"Ожидался статус: {expected_status},"
                                                             f"но получен: {response.status_code}")

    @pytest.mark.xfail(reason="В тестах create и update не валидируется данные. API принимает любые данные")
    @allure.story("Создание нового продукта")
    @pytest.mark.parametrize("product_data, expected_status", [
        # ❌ Негативные кейсы
        ({"title": 1414141}, HTTPStatus.BAD_REQUEST),
        ({"title": "+_)(*&^%$#@!"}, HTTPStatus.BAD_REQUEST),
        ({"title": ""}, HTTPStatus.BAD_REQUEST),
        ({"title": "text"*50}, HTTPStatus.BAD_REQUEST),
        ({"title": 99.99}, HTTPStatus.BAD_REQUEST)
    ])
    def test_create_product(self, products_api, product_data, expected_status, logger):
        with allure.step(f"Отправляю POST-запрос на эндпоинт /products/add с параметрами: {product_data}"):
            response = products_api.create_product(product_data=product_data)
            logger.info(f"Ответ: {response.status_code} - {response.text}")
            assert response.status_code == expected_status, (f"Ожидался ответ: {expected_status},"
                                                             f"но получен: {response.status_code}")

    @pytest.mark.xfail(reason="В тестах create и update не валидируется данные. API принимает любые данные")
    @allure.story("Обновление продукта")
    @pytest.mark.parametrize("product_id, product_update, expected_status", [
        # ❌ Негативные кейсы
        (1, {"title": 0}, HTTPStatus.BAD_REQUEST),
        (3, {"title": "+_)(*&^%$#@!"}, HTTPStatus.BAD_REQUEST),
        (5, {"title": ""}, HTTPStatus.BAD_REQUEST),
        (10, {}, HTTPStatus.BAD_REQUEST)
    ])
    def test_update_product(self, products_api, product_id, product_update, expected_status, logger):
        with allure.step(f"Отправляю PUT-запрос на эндпоинт /products/{product_id} c параметрами: {product_update}"):
            response = products_api.update_product(product_id=product_id, product_data=product_update)
            logger.info(f"Ответ: {response.status_code} - {response.text}")
            assert response.status_code == expected_status, (f"Ожидался статус: {expected_status},"
                                                             f"но получен: {response.status_code}")

    @allure.story("Удаление продукта")
    @pytest.mark.parametrize("product_id, expected_status", [
        # ❌ Негативные кейсы
        (9999, HTTPStatus.NOT_FOUND),
        (0, HTTPStatus.NOT_FOUND),
        (-1, HTTPStatus.NOT_FOUND)
    ])
    def test_delete_product(self, products_api, product_id, expected_status, logger):
        with allure.step(f"Отправляю DELETE-запрос на эндпоинт /products/{product_id}"):
            response = products_api.delete_product(product_id=product_id)
            logger.info(f"Ответ: {response.status_code} - {response.text}")
            assert response.status_code == expected_status, (f"Ожидался ответ: {expected_status},"
                                                             f"но получен: {response.status_code}")





