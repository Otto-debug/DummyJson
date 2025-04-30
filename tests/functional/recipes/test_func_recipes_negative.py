import allure
import pytest
from http import HTTPStatus

@pytest.mark.negative
@allure.epic("Функциональное тестирование рецептов")
@allure.feature("Негативные кейсы")
class TestRecipesNegative:

    @allure.story("Получение одного рецепта")
    @pytest.mark.parametrize("recipes_id, expected_status", [
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
    def test_get_recipes(self, recipes_api, recipes_id, expected_status, logger):
        with allure.step(f"Отправляю GET-запрос к эндпоинту /recipes/{recipes_id}"):
            response = recipes_api.get_recipes(recipes_id)
            logger.info(f"Ответ: {response.status_code} - {response.text}")
            assert response.status_code == expected_status, (f"Ожидал ответ: {expected_status},"
                                                             f"но пришел: {response.status_code}")

    @pytest.mark.xfail(reason="dummyjson не валидирует данные, даже невалидные проходят")
    @allure.story("Создание рецепта")
    @pytest.mark.parametrize("recipes_data, expected_status", [
        ({'name': 12345}, HTTPStatus.BAD_REQUEST),
        ({'name': "+_)(*&^%$#@!"}, HTTPStatus.BAD_REQUEST),
        ({'name': "test"*50}, HTTPStatus.BAD_REQUEST),
        ({'name': ""}, HTTPStatus.BAD_REQUEST),
        ({'name': "<script>alert('xss')</script>"}, HTTPStatus.BAD_REQUEST)
    ])
    def test_create_recipes(self, recipes_api,recipes_data, expected_status, logger):
        with allure.step(f"Отправляю POST-запрос на эндпоинт /recipes/add с параметрами: {recipes_data}"):
            response = recipes_api.create_recipes(recipes_data=recipes_data)
            logger.info(f'Ответ: {response.status_code} - {response.text}')
            assert response.status_code == expected_status, (f'Ожидался статус: {expected_status},'
                                                             f'но пришёл: {response.status_code}')

    @pytest.mark.xfail(reason="dummyjson не валидирует данные, даже невалидные проходят")
    @allure.story("Обновление рецепта")
    @pytest.mark.parametrize("recipes_id, update_data, expected_status", [
        (1, {'name': 12345}, HTTPStatus.BAD_REQUEST),
        (12, {'name': "+_)(*&^%$#@!"}, HTTPStatus.BAD_REQUEST),
        (27, {'name': "test" * 50}, HTTPStatus.BAD_REQUEST),
        (35, {'name': ""}, HTTPStatus.BAD_REQUEST),
        (50, {'name': "<script>alert('xss')</script>"}, HTTPStatus.BAD_REQUEST)
    ])
    def test_update_recipes(self, recipes_api, recipes_id, update_data, expected_status, logger):
        with allure.step(f'Отправляю PUT-запрос на эндпоинт /recipes/{recipes_id} с обновлёнными данными: {update_data}'):
            response = recipes_api.update_recipes(recipes_id, update_data)
            logger.info(f"Ответ: {response.status_code} - {response.text}")
            assert response.status_code == expected_status, (f"Ожидался статус: {expected_status},"
                                                             f"но пришёл: {response.status_code}")

    @allure.story("Удаление пользователя")
    @pytest.mark.parametrize("recipes_id, expected_status", [
        (0.1, HTTPStatus.NOT_FOUND),
        (-1, HTTPStatus.NOT_FOUND),
        (999999999, HTTPStatus.NOT_FOUND),
        (0, HTTPStatus.NOT_FOUND),
        ("", HTTPStatus.NOT_FOUND)
    ])
    def test_delete_recipes(self, recipes_api, recipes_id, expected_status, logger):
        with allure.step(f"Отправляю DELETE-запрос на эндпоинт /recipes/{recipes_id}"):
            response = recipes_api.delete_recipes(recipes_id)
            logger.info(f"Ответ: {response.status_code} - {response.text}")
            assert response.status_code == expected_status, (f"Ожидался статус: {expected_status},"
                                                             f"но пришёл: {response.status_code}")
