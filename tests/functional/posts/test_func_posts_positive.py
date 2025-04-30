import time

import allure
import pytest
from http import HTTPStatus

from pydantic import ValidationError
from schemas.posts_schema import PostBase, PostGet, PostCreate

@pytest.mark.positive
@allure.epic("Функциональное тестирование постов")
@allure.feature("Позитивные тесты")
class TestPostsPositive:

    @allure.story("Получение одного поста")
    @pytest.mark.parametrize("post_id, expected_status", [
        # ✅ Позитивные кейсы
        (15, HTTPStatus.OK),
        (38, HTTPStatus.OK),
        (103, HTTPStatus.OK),
        (222, HTTPStatus.OK),
        (250, HTTPStatus.OK)
    ])
    def test_get_post(self, posts_api, post_id, expected_status, logger):
        with allure.step(f"Отправляю GET-запрос на эндпоинт /posts/{post_id}"):
            response = posts_api.get_post(post_id)
            logger.info(f"Ответ: {response.status_code} - {response.text}")
            assert response.status_code == expected_status, (f"Ожидал статус: {expected_status},"
                                                             f"но получил: {response.status_code}")

        if response.status_code == HTTPStatus.OK:
            with allure.step('Проверка валидации данных'):
                try:
                    post_data = PostGet(**response.json())
                    logger.info("Данные провалидированы")
                    assert post_data.id == post_data, f"ID поста в ответе: {post_id}"
                except ValidationError as e:
                    logger.error(f"Ошибка валидации данных: {e}")
                    pytest.fail(f"Ошибка валидации: {e}")

    @allure.story("Создание поста")
    @pytest.mark.parametrize("post_data, expected_status", [
        # ✅ Позитивные кейсы
        (
                {
                    "title": "Exploring the Mountains",
                    "body": "A detailed guide on mountain hiking essentials.",
                    "userId": 3,
                    "tags": ["travel", "adventure", "hiking"]
                },
                HTTPStatus.CREATED
        ),
        (
                {
                    "title": "Python Tips & Tricks",
                    "body": "Improve your Python skills with these tips.",
                    "userId": 5,
                    "tags": ["programming", "python", "development"]
                },
                HTTPStatus.CREATED
        )
    ])
    def test_create_post(self, posts_api, post_data, expected_status, logger):
        with allure.step(f"Отправляю POST-запрос к эндпоинту /posts/add с параметрами: {post_data}"):
            response = posts_api.create_post(post_data)
            logger.info(f"Ответ: {response.status_code} - {response.text}")
            assert response.status_code == expected_status, (f"Ожидался статус: {expected_status},"
                                                             f"но получен: {response.status_code}")

        if response.status_code == HTTPStatus.CREATED:
            with allure.step("Проверка валидации данных"):
                try:
                    data = PostCreate(**response.json())
                    logger.info("Данные провалидированы")
                except ValidationError as e:
                    logger.error(f"Ошибка валидации данных: {e}")
                    pytest.fail(f"Ошибка валидации: {e}")

    @allure.story("Обновление поста")
    @pytest.mark.parametrize("post_id, update_data, expected_status", [
        # ✅ Позитивные кейсы
        (
                1,
                {"title": "Updated Title", "body": "Updated body of the post"},
                HTTPStatus.OK
        ),
        (
                2,
                {"tags": ["updated", "tags", "list"]},
                HTTPStatus.OK
        ),
        (
                3,
                {"reactions": 25},
                HTTPStatus.OK
        )
    ])
    def test_update_post(self, posts_api, post_id, update_data, expected_status, logger):
        with allure.step(f"Отправляю PUT-запрос к эндпоинту /posts/{post_id} с обновленными параметрами: {update_data}"):
            response = posts_api.update_post(post_id, update_data)
            logger.info(f"Ответ: {response.status_code} - {response.text}")
            assert response.status_code == expected_status, (f"Ожидался статус: {expected_status},"
                                                             f"но пришёл: {response.status_code}")

        if response.status_code == HTTPStatus.OK:
            with allure.step("Проверка валидации данных"):
                try:
                    data = PostBase(**response.json())
                    logger.info("Данные провалидированы")
                except ValidationError as e:
                    logger.error(f"Ошибка валидации данных: {e}")
                    pytest.fail(f"Ошибка валидации")

    @allure.story("Удаление поста")
    @pytest.mark.parametrize("post_id, expected_status", [
        # ✅ Позитивные кейсы
        (25, HTTPStatus.OK),
        (33, HTTPStatus.OK),
        (101, HTTPStatus.OK),
        (173, HTTPStatus.OK),
        (223, HTTPStatus.OK),
        (250, HTTPStatus.OK)
    ])
    def test_delete_post(self, posts_api, post_id, expected_status, logger):
        with allure.step(f"Отправляю DELETE-запрос к эндпоинту /posts/{post_id}"):
            response = posts_api.delete_post(post_id)
            logger.info(f"Ответ: {response.status_code} - {response.text}")
            assert response.status_code == expected_status, (f"Ожидался статус: {expected_status},"
                                                             f"но получен: {response.status_code}")

        if response.status_code == HTTPStatus.OK:
            with allure.step('Проверка валидации данных'):
                try:
                    delete_post = PostGet(**response.json())
                    logger.info(f"Пост удалён: {delete_post}")
                except ValidationError as e:
                    logger.error(f"Ошибка валидации данных: {e}")
                    pytest.fail(f"Ошибка валидации: {e}")

            with allure.step("Проверка, что пост действительно удалён"):
                timeout = 5
                interval = 0.5
                elapsed = 0
                while elapsed < timeout:
                    get_resp = posts_api.get_post(post_id)
                    if get_resp.status_code == HTTPStatus.NOT_FOUND:
                        logger.info(f"Пост с id={post_id} успешно удалён")
                        break
                    time.sleep(interval)
                    elapsed += interval
                else:
                    pytest.fail(f"Пост с id={post_id} все ещё существует")