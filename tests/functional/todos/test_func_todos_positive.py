import time

import allure
import pytest
from http import HTTPStatus

from pydantic import ValidationError
from schemas.todos_schema import TodoGet, TodoCreate, TodoUpdate, TodoDelete

@pytest.mark.positive
@allure.epic("Функциональное тестирование 'задач'")
@allure.feature("Позитивные кейсы")
class TestTodosPositive:

    @allure.story("Получение одной задачи")
    @pytest.mark.parametrize("todos_id, expected_status", [
        # ✅ Позитивные кейсы
        (1, HTTPStatus.OK),
        (15, HTTPStatus.OK),
        (105, HTTPStatus.OK),
        (237, HTTPStatus.OK),
        (254, HTTPStatus.OK),
    ])
    def test_get_todos(self, todos_api, todos_id, expected_status, logger):
        with allure.step(f"Отправляю GET-запрос на эндпоинт /todos/{todos_id}"):
            response = todos_api.get_todos(todos_id)
            logger.info(f"Ответ: {response.status_code} - {response.text}")
            assert response.status_code == expected_status, (f'Ожидался ответ: {expected_status},'
                                                             f'но пришёл: {response.status_code}')

        if response.status_code == HTTPStatus.OK:
            with allure.step('Проверка валидации данных'):
                try:
                    todos_data = TodoGet(**response.json())
                    logger.info('Данные провалидированы')
                    assert todos_data.id == todos_id, (f'Ожидалась задача с id={todos_id},'
                                                       f'но пришла: {todos_data.id}')
                except ValidationError as e:
                    logger.error(f"Ошибка валидации данных: {e}")
                    pytest.fail(f"Ошибка валидации: {e}")

    @allure.story("Создание задачи")
    @pytest.mark.parametrize("todos_data, expected_status", [
        # ✅ Позитивные кейсы
        ({
            'todo': 'Use DummyJSON in the project',
            'completed': False,
            'userId': 5,
        }, HTTPStatus.CREATED),
        ({
             'todo': 'Use text'*3,
             'completed': True,
             'userId': 15,
         }, HTTPStatus.CREATED),
        ({
             'todo': 'TEXT'*3,
             'completed': False,
             'userId': 200,
         }, HTTPStatus.CREATED),
    ])
    def test_create_todos(self, todos_api, todos_data, expected_status, logger):
        with allure.step(f'Отправка POST-запрос на эндпоинт /todos/add/ с параметрами: {todos_data}'):
            response = todos_api.create_todos(todos_data)
            logger.info(f'Ответ: {response.status_code} - {response.text}')
            assert response.status_code == expected_status, (f"Ожидался статус: {expected_status},"
                                                             f"но пришёл: {response.status_code}")

        if response.status_code == HTTPStatus.CREATED:
            with allure.step("Проверка валидации данных"):
                try:
                    data = TodoCreate(**response.json())
                    logger.info('Данные провалидированы')
                except ValidationError as e:
                    logger.error(f"Ошибка валидации данных: {e}")
                    pytest.fail(f"Ошибка валидации: {e}")

    @allure.story("Обновление задачи")
    @pytest.mark.parametrize("todos_id, update_todos, expected_status", [
        # ✅ Позитивные кейсы
        (5, {
            'completed': False,
        }, HTTPStatus.OK),
        (200, {
            'completed': True,
        }, HTTPStatus.OK)
    ])
    def test_update_todos(self, todos_api, todos_id, update_todos, expected_status, logger):
        with allure.step(f"Отправляю PUT-запрос на эндпоинт /todos/{todos_id}"):
            response = todos_api.update_todos(todos_id, update_todos)
            logger.info(f'Ответ: {response.status_code} - {response.text}')
            assert response.status_code == expected_status, (f'Ожидался статус: {expected_status},'
                                                             f'но пришёл: {response.status_code}')

        if response.status_code == HTTPStatus.OK:
            with allure.step('Проверка валидации данных'):
                try:
                    todo_data = TodoUpdate(**response.json())
                    logger.info('Данные проваилидированы')
                except ValidationError as e:
                    logger.error(f"Ошибка валидации данных: {e}")
                    pytest.fail(f"Ошибка валидации: {e}")

    @allure.story("Удаление задачи")
    @pytest.mark.parametrize("todos_id, expected_status", [
        # ✅ Позитивные кейсы
        (1, HTTPStatus.OK),
        (10, HTTPStatus.OK),
        (187, HTTPStatus.OK),
        (254, HTTPStatus.OK)
    ])
    def test_delete_todos(self, todos_api, todos_id, expected_status, logger):
        with allure.step(f"Отправляю DELETE-запрос на эндпоинт /todos/{todos_id}"):
            response = todos_api.delete_todos(todos_id)
            logger.info(f"Ответ: {response.status_code} - {response.text}")
            assert response.status_code == expected_status, (f"Ожидался статус: {expected_status},"
                                                             f"но пришёл: {response.status_code}")

        if response.status_code == HTTPStatus.OK:
            with allure.step('Проверка валидации данных'):
                try:
                    delete_todos = TodoDelete(**response.json())
                    logger.info(f'Задача удалена: {delete_todos}')
                except ValidationError as e:
                    logger.error(f"Ошибка валидации данных: {e}")
                    pytest.fail(f"Ошибка валидации: {e}")

            with allure.step("Проверка, что задача действительно удалена"):
                timeout = 5
                interval = 0.5
                elapsed = 0
                while elapsed < timeout:
                    get_resp = todos_api.get_todos(todos_id)
                    if get_resp.status_code == HTTPStatus.NOT_FOUND:
                        logger.info(f"Задача с id={todos_id} успешно удалена")
                        break
                    time.sleep(interval)
                    elapsed += interval
                else:
                    pytest.fail(f"Задача с id={todos_id} всё ещё существует спустя {timeout} секунд")

