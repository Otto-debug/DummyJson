import allure
import pytest
from http import HTTPStatus


@pytest.mark.negative
@allure.epic("Функциональное тестирование 'задач'")
@allure.feature("Негативные кейсы")
class TestTodosNegative:

    @allure.story('Получение одной задачи')
    @pytest.mark.parametrize('todos_id, expected_status', [
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
    def test_get_todos(self, todos_api, todos_id, expected_status, logger):
        with allure.step(f'Отправляю GET-запрос на эндпоинт на /todos/{todos_id}'):
            response = todos_api.get_todos(todos_id)
            logger.info(f'Ответ: {response.status_code} - {response.text}')
            assert response.status_code == expected_status, (f"Ожидался статус: {response},"
                                                             f"но пришёл: {response.status_code}")

    @pytest.mark.xfail(reason="dummyjson не валидирует данные, даже невалидные проходят")
    @allure.story("Создание задачи")
    @pytest.mark.parametrize('todos_data, expected_status', [
        ({
             'todo': '+_)(*&^%$#@!',
             'completed': False,
             'userId': 5,
         }, HTTPStatus.BAD_REQUEST),
        ({
             'todo': 1234,
             'completed': '',
             'userId': 500,
         }, HTTPStatus.BAD_REQUEST),
        ({
             'todo': 'text' * 30,
             'completed': False,
             'userId': 1,
         }, HTTPStatus.BAD_REQUEST),
        ({
             'todo': 'text' * 10,
             'completed': False,
             'userId': 0,
         }, HTTPStatus.BAD_REQUEST),
        ({
             'todo': '',
             'completed': 100,
             'userId': -1,
         }, HTTPStatus.BAD_REQUEST),
    ])
    def test_create_todos(self, todos_api, todos_data, expected_status, logger):
        with allure.step(f'Отправляю POST-запрос на эндпоинт /todos/add с параметрами: {todos_data}'):
            response = todos_api.create_todos(todos_data)
            logger.info(f'Ответ: {response.status_code} - {response.text}')
            assert response.status_code == expected_status, (f'Ожидался статус: {expected_status},'
                                                             f'но пришёл: {response.status_code}')

    @pytest.mark.xfail(reason="dummyjson не валидирует данные, даже невалидные проходят")
    @allure.story("Обновление задачи")
    @pytest.mark.parametrize("todos_id, update_todos, expected_status", [
        (1, {
            'completed': '',
        }, HTTPStatus.BAD_REQUEST),
        (10, {
            'completed': 100,
        }, HTTPStatus.BAD_REQUEST),
        (20, {
            'completed': -1,
        }, HTTPStatus.BAD_REQUEST),
        (111, {
            'completed': 0,
        }, HTTPStatus.BAD_REQUEST),
        (1, {
            'completed': "+_)(*&^%$#@!",
        }, HTTPStatus.BAD_REQUEST),
    ])
    def test_update_todos(self, todos_api, todos_id, update_todos, expected_status, logger):
        with allure.step(
            f"Отправляю PUT-запрос на эндпоинт /todos/{todos_id} с обновленными параметрами: {update_todos}"):
            response = todos_api.update_todos(todos_id, update_todos)
            logger.info(f"Ответ: {response.status_code} - {response.text}")
            assert response.status_code == expected_status, (f'Ожидался статус: {expected_status},'
                                                             f'но получен: {response.status_code}')

    @allure.story("Удаление задачи")
    @pytest.mark.parametrize("todos_id, expected_status", [
        (0.1, HTTPStatus.NOT_FOUND),
        (-1, HTTPStatus.NOT_FOUND),
        (999999999, HTTPStatus.NOT_FOUND),
        (0, HTTPStatus.NOT_FOUND),
        ("", HTTPStatus.NOT_FOUND)
    ])
    def test_delete_todos(self, todos_api, todos_id, expected_status, logger):
        with allure.step(f"Отправляю DELETE-запрос на эндпоинт /todos/{todos_id}"):
            response = todos_api.delete_todos(todos_id)
            logger.info(f'Ответ: {response.status_code} - {response.text}')
            assert response.status_code == expected_status, (f"Ожидался статус: {expected_status},"
                                                             f"но пришёл: {response.status_code}")
