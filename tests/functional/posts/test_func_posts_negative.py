import allure
import pytest
from http import HTTPStatus

@pytest.mark.negative
@allure.epic("Функциональное тестирование")
@allure.feature("Негативные кейсы")
class TestPostsNegative:

    @allure.story("Получение одного поста")
    @pytest.mark.parametrize("post_id, expected_status", [
        # ❌ Негативные кейсы
        (0, HTTPStatus.NOT_FOUND),
        (-1, HTTPStatus.NOT_FOUND),
        (99999, HTTPStatus.NOT_FOUND),
        ("text", HTTPStatus.BAD_REQUEST),
        ("((@*@(@(@(@", HTTPStatus.BAD_REQUEST),
        (99.99, HTTPStatus.NOT_FOUND),
        (None, HTTPStatus.BAD_REQUEST),
        (True, HTTPStatus.BAD_REQUEST),
        ([], HTTPStatus.NOT_FOUND),
        ({}, HTTPStatus.NOT_FOUND),
    ])
    def test_get_post(self, posts_api, post_id, expected_status, logger):
        with allure.step(f"Отправляю GET-запрос к эндпоинту /posts/{post_id}"):
            response = posts_api.get_post(post_id)
            logger.info(f"Ответ: {response.status_code} - {response.text}")
            assert response.status_code == expected_status, (f"Ожидал статус: {expected_status},"
                                                             f"но получен: {response.status_code}")

    @pytest.mark.xfail(reason="dummyjson не валидирует входные данные")
    @allure.story("Создание поста")
    @pytest.mark.parametrize("post_data, expected_status", [
        # ❌ Негативные кейсы
        (
                {
                    "title": "+)(*&^$#@!",
                    "body": "A detailed guide on mountain hiking essentials.",
                    "userId": 0,
                    "tags": ["travel", "adventure", "hiking"]
                },
                HTTPStatus.BAD_REQUEST
        ),
        (
                {
                    "title": 1234515,
                    "body": "Improve your Python skills with these tips.",
                    "userId": 15,
                    "tags": ["programming", "python", "development"]
                },
                HTTPStatus.BAD_REQUEST
        ),
        (
                {

                    "body": "Improve your Python skills with these tips.",
                    "userId": 27,
                    "tags": ["programming", "python", "development"]
                },
                HTTPStatus.BAD_REQUEST
        ),
        (
                {
                    "title": 1234515,

                    "userId": 15,

                },
                HTTPStatus.BAD_REQUEST
        ),
    ])
    def test_create_post(self, posts_api, post_data, expected_status, logger):
        with allure.step(f"Отправляю POST-запрос на эндпоинт /posts/add с параметрами: {post_data}"):
            response = posts_api.create_post(post_data)
            logger.info(f"Ответ: {response.status_code} - {response.text}")
            assert response.status_code == expected_status, (f"Ожидался статус: {expected_status},"
                                                             f"но получен: {response.status_code}")

    @pytest.mark.xfail(reason="dummyjson не валидирует входные данные")
    @allure.story("Обновление поста")
    @pytest.mark.parametrize("post_id, update_data, expected_status", [
        # ❌ Негативные кейсы
        (
                15,
                {"title": 'text'*50},
                HTTPStatus.BAD_REQUEST
        ),
        (
                30,
                {"tags": [i for i in range(1, 20) if i % 2 == 0]},
                HTTPStatus.BAD_REQUEST
        ),
        (
                47,
                {"reactions": ""},
                HTTPStatus.BAD_REQUEST
        )
    ])
    def test_update_post(self, posts_api, post_id, update_data, expected_status, logger):
        with allure.step(f"Отправляю PUT-запрос на эндпоинт /posts/{post_id} с обновленными данными: {update_data}"):
            response = posts_api.update_post(post_id, update_data)
            logger.info(f"Ответ: {response.status_code} - {response.text}")
            assert response.status_code == expected_status, (f"Ожидался статус: {expected_status},"
                                                             f"но получен: {response.status_code}")

    @allure.story("Удаление поста")
    @pytest.mark.parametrize("post_id, expected_status", [
        (0.1, HTTPStatus.NOT_FOUND),
        (-1, HTTPStatus.NOT_FOUND),
        (999999999, HTTPStatus.NOT_FOUND),
        (0, HTTPStatus.NOT_FOUND),
        ("", HTTPStatus.NOT_FOUND)
    ])
    def test_delete_post(self, posts_api, post_id, expected_status, logger):
        with allure.step(f"Отправляю DELETE-запрос на эндпоинт /posts/{post_id}"):
            response = posts_api.delete_post(post_id)
            logger.info(f"Ответ: {response.status_code} - {response.text}")
            assert response.status_code == expected_status, (f"Ожидался статус: {expected_status},"
                                                             f"но получен: {response.status_code}")
