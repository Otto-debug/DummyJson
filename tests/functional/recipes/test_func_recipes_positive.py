import time

import allure
import pytest
from http import HTTPStatus

from pydantic import ValidationError
from schemas.recipes_schema import RecipeGET, RecipePOST, RecipeShort


@pytest.mark.positive
@allure.epic("Функциональное тестирование рецептов")
@allure.feature("Позитивные кейсы")
class TestRecipesPositive:

    @allure.story("Получение одного рецепта")
    @pytest.mark.parametrize("recipes_id, expected_status", [
        # ✅ Позитивные кейсы
        (1, HTTPStatus.OK),
        (15, HTTPStatus.OK),
        (20, HTTPStatus.OK),
        (35, HTTPStatus.OK),
        (50, HTTPStatus.OK),
    ])
    def test_get_recipes(self, recipes_api, recipes_id, expected_status, logger):
        with allure.step(f"Отправляю GET-запрос на эндпоинт /recipes/{recipes_id}"):
            response = recipes_api.get_recipes(recipes_id)
            logger.info(f"Ответ: {response.status_code} - {response.text}")
            assert response.status_code == expected_status, (f"Ожидал ответ: {expected_status}, "
                                                             f"но получил: {response.status_code}")

        if response.status_code == HTTPStatus.OK:
            with allure.step('Проверка валидации данных'):
                try:
                    recipes_data = RecipeGET(**response.json())
                    logger.info('Данные провалидированы')
                    assert recipes_data.id == recipes_id, f"ID рецепта в ответе: {recipes_id}"
                except ValidationError as e:
                    logger.error(f"Ошибка валидации данных: {e}")
                    pytest.fail(f"Ошибка валидации")

    @allure.story("Создание рецепта")
    @pytest.mark.parametrize('recipes_data, expected_status', [
        ({'name': "Tostes"}, HTTPStatus.CREATED),
        ({'name': "Draniki"}, HTTPStatus.CREATED),
        ({'name': 'Pelmeni'}, HTTPStatus.CREATED),
        ({'name': 'Сake «Berries miracle»'}, HTTPStatus.CREATED)
    ])
    def test_create_recipes(self, recipes_api, recipes_data, expected_status, logger):
        with allure.step(f"Отправляю POST-запрос на эндпоинт /recipes/add с параметрами: {recipes_data}"):
            response = recipes_api.create_recipes(recipes_data)
            logger.info(f"Ответ: {response.status_code} - {response.text}")
            assert response.status_code == HTTPStatus.CREATED, (f"Ожидался статус: {expected_status},"
                                                                f"но получен: {response.status_code}")

        if response.status_code == HTTPStatus.CREATED:
            with allure.step('Проверка валидации данных'):
                try:
                    data = RecipePOST(**response.json())
                    logger.info('Данные провалидированы')
                except ValidationError as e:
                    logger.error(f'Ошибка валидации данных: {e}')
                    pytest.fail(f"Ошибка валидации: {e}")

    @allure.story("Обновление рецепта")
    @pytest.mark.parametrize("recipes_id, update_recipes, expected_status", [
        (1, {'name': 'Borsch'}, HTTPStatus.OK),
        (25, {'name': 'Apple crumble'}, HTTPStatus.OK),
        (39, {'name': 'Сake «Berries miracle»'}, HTTPStatus.OK),
        (50, {'name': 'Pelmeni (Meat dumplings)'}, HTTPStatus.OK)
    ])
    def test_update_recipes(self, recipes_api, recipes_id, update_recipes, expected_status, logger):
        with allure.step(f"Отправляю PUT-запрос на эндпоинт /recipes/{recipes_id} с параметрами: {update_recipes}"):
            response = recipes_api.update_recipes(recipes_id, update_recipes)
            logger.info(f'Ответ: {response.status_code} - {response.text}')
            assert response.status_code == expected_status, (f"Ожидался статус: {expected_status},"
                                                             f"но пришел: {response.status_code}")

        if response.status_code == HTTPStatus.OK:
            with allure.step("Проверка валидации данных"):
                try:
                    data = RecipeShort(**response.json())
                    logger.info("Данные провалидированы")
                except ValidationError as e:
                    logger.error(f'Ошибка валидации данных: {e}')
                    pytest.fail(f'Ошибка валидации: {e}')

    @allure.story("Удаление рецепта")
    @pytest.mark.parametrize('recipes_id, expected_status', [
        (1, HTTPStatus.OK),
        (10, HTTPStatus.OK),
        (22, HTTPStatus.OK),
        (35, HTTPStatus.OK),
        (50, HTTPStatus.OK)
    ])
    def test_delete_recipes(self, recipes_api, recipes_id, expected_status, logger):
        with allure.step(f"Отправляю DELETE-запрос на эндпоинт /recipes/{recipes_id}"):
            response = recipes_api.delete_recipes(recipes_id)
            logger.info(f"Ответ: {response.status_code} - {response.text}")
            assert response.status_code == expected_status, (f"Ожидался ответ: {expected_status},"
                                                             f"но пришёл: {response.status_code}")

        if response.status_code == HTTPStatus.OK:
            with allure.step('Проверка валидации данных'):
                try:
                    delete_user = RecipeShort(**response.json())
                    logger.info(f"Рецепт удалён: {delete_user}")
                except ValidationError as e:
                    logger.error(f"Ошибка валидации данных: {e}")
                    pytest.fail(f"Ошибка валидации: {e}")

            with allure.step("Проверка, что рецепт действительно удалён"):
                timeout = 5
                interval = 0.5
                elapsed = 0
                while elapsed < timeout:
                    get_resp = recipes_api.get_recipes(recipes_id)
                    if get_resp.status_code == HTTPStatus.NOT_FOUND:
                        logger.info(f"Рецепт с id={recipes_id} успешно удалён")
                        break
                    time.sleep(interval)
                    elapsed += interval
                else:
                    pytest.fail(f"Рецепт с id={recipes_id} все ещё существует спустя {timeout} секунд")
