import allure
import pytest
from http import HTTPStatus


@pytest.mark.negative
@allure.epic("Функциональное тестирование комментариев")
@allure.feature("Негативные кейсы")
class TestCommentsNegative:

    @allure.story("Получение одного комментария")
    @pytest.mark.parametrize("comment_id, expected_status", [
        (0, HTTPStatus.NOT_FOUND),
        (-1, HTTPStatus.NOT_FOUND),
        ("text", HTTPStatus.NOT_FOUND),
        ([], HTTPStatus.NOT_FOUND),
        ((), HTTPStatus.NOT_FOUND),
        ({}, HTTPStatus.NOT_FOUND),
        (99.99, HTTPStatus.NOT_FOUND),
        (99999, HTTPStatus.NOT_FOUND)
    ])
    def test_get_comment(self, comments_api, comment_id, expected_status, logger):
        with allure.step(f"Отправляю GET-запрос к эндпоинту /comments/{comment_id}"):
            response = comments_api.get_comments(comment_id)
            logger.info(f"Ответ: {response.status_code} - {response.text}")
            assert response.status_code == expected_status, (f"Ожидался статус: {expected_status},"
                                                             f"но пришел: {response.status_code}")

    @pytest.mark.xfail(reason="Данный API не обрабатывает данные")
    @allure.story("Создание комментария")
    @pytest.mark.parametrize("comment_data, expected_status", [
        ({
             'body': "+_)(*&^%$#@!",
             'postId': 3,
             'userId': 5,
         }, HTTPStatus.BAD_REQUEST),
        ({
             'body': "",
             'postId': 10,
             'userId': 333,
         }, HTTPStatus.BAD_REQUEST),
        ({
             'body': "This is test" * 20,
             'postId': 59,
             'userId': 150,
         }, HTTPStatus.BAD_REQUEST),
        ({
             'body': [],
             'postId': "",
             'userId': "",
         }, HTTPStatus.BAD_REQUEST),
        ({
             'body': str(),
             'postId': 0,
             'userId': 0,
         }, HTTPStatus.BAD_REQUEST),

    ])
    def test_create_comment(self, comments_api, comment_data, expected_status, logger):
        with allure.step(f"Отправляю POST-запрос к эндпоинту /comments/add с параметрами: {comment_data}"):
            response = comments_api.create_comments(comment_data)
            logger.info(f"Ответ: {response.status_code} - {response.text}")
            assert response.status_code == expected_status, (f"Ожидался статус: {expected_status},"
                                                             f"но пришёл: {response.status_code}")

    @pytest.mark.xfail(reason="Данный API не обрабатывает данные")
    @allure.story("Обновление комментария")
    @pytest.mark.parametrize("comment_id, update_data, expected_status", [
        (5, {'body': '+_)(*&^%$#@!'}, HTTPStatus.BAD_REQUEST),
        (25, {'body': 'text' * 20}, HTTPStatus.BAD_REQUEST),
        (73, {'body': ''}, HTTPStatus.BAD_REQUEST),
        (150, {'body': 0}, HTTPStatus.BAD_REQUEST),
        (89, {'': ""}, HTTPStatus.BAD_REQUEST)
    ])
    def test_update_comment(self, comments_api, comment_id, update_data, expected_status, logger):
        with allure.step(
            f"Отправляю PUT-запрос на эндпоинт /comments/{comment_id} с обновленными параметрами: {update_data}"):
            response = comments_api.update_comments(comment_id, update_data)
            logger.info(f"Ответ: {response.status_code} - {response.text}")
            assert response.status_code == expected_status, (f"Ожидался статус: {expected_status},"
                                                             f"но пришёл: {response.status_code}")

    @allure.story("Удаление комментария")
    @pytest.mark.parametrize("comment_id, expected_status", [
        (999, HTTPStatus.NOT_FOUND),
        (0, HTTPStatus.NOT_FOUND),
        (-1, HTTPStatus.NOT_FOUND),
        (99.99, HTTPStatus.NOT_FOUND)
    ])
    def test_delete_comment(self, comments_api, comment_id, expected_status, logger):
        with allure.step(f"Отправляю DELETE-запрос к эндпоинту /comments/{comment_id}"):
            response = comments_api.delete_comments(comment_id)
            logger.info(f"Ответ: {response.status_code} - {response.text}")
            assert response.status_code == expected_status, (f"Ожидал статус: {expected_status},"
                                                             f"но пришёл: {response.status_code}")


