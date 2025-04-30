import allure
import pytest
import time
from http import HTTPStatus

from pydantic import ValidationError
from schemas.comments_schema import CommentGet, CommentCreate, CommentUpdate


@pytest.mark.positive
@allure.epic("Функциональное тестирование комментариев")
@allure.feature("Позитивные кейсы")
class TestCommentsPositive:

    @allure.story("Получение одного комментария")
    @pytest.mark.parametrize("comment_id, expected_status", [
        (1, HTTPStatus.OK),
        (29, HTTPStatus.OK),
        (73, HTTPStatus.OK),
        (159, HTTPStatus.OK),
        (322, HTTPStatus.OK),
        (339, HTTPStatus.OK)
    ])
    def test_get_comment(self, comments_api, comment_id, expected_status, logger):
        with allure.step(f"Отправляю GET-запрос на эндпоинт /comments/{comment_id}"):
            response = comments_api.get_comments(comment_id)
            logger.info(f'Ответ: {response.status_code} - {response.text}')
            assert response.status_code == expected_status, (f"Ожидался статус: {expected_status},"
                                                             f"но получен: {response.status_code}")

        if response.status_code == HTTPStatus.OK:
            with allure.step('Проверка валидации данных'):
                try:
                    comment_data = CommentGet(**response.json())
                    logger.info("Данные провалидированы")
                    assert comment_data.id == comment_id, (f"Ожидался ID: {comment_id}, "
                                                           f"но пришёл: {comment_data.id}")
                except ValidationError as e:
                    logger.error(f"Ошибка валидации данных: {e}")
                    pytest.fail(f"Ошибка валидации")

    @allure.story("Создание комментария")
    @pytest.mark.parametrize("comment_data, expected_status", [
        ({
             'body': "This is test",
             'postId': 3,
             'userId': 5,
         }, HTTPStatus.CREATED),
        ({
             'body': "This is test - test",
             'postId': 10,
             'userId': 333,
         }, HTTPStatus.CREATED),
        ({
             'body': "This is test" * 2,
             'postId': 59,
             'userId': 150,
         }, HTTPStatus.CREATED),
    ])
    def test_create_comment(self, comments_api, comment_data, expected_status, logger):
        with allure.step(f"Отправляю POST-запрос на эндпоинт /comments/add с параметрами: {comment_data}"):
            response = comments_api.create_comments(comment_data)
            logger.info(f"Ответ: {response.status_code} - {response.text}")
            assert response.status_code == expected_status, (f"Ожидался статус: {expected_status},"
                                                             f"но пришёл: {response.status_code}")

        if response.status_code == HTTPStatus.CREATED:
            with allure.step('Проверка валидации данных'):
                try:
                    data = CommentCreate(**response.json())
                    logger.info('Данные провалидированы')
                except ValidationError as e:
                    logger.error(f"Ошибка валидации данных: {e}")
                    pytest.fail(f"Ошибка валидации: {e}")

    @allure.story("Обновление комментариев")
    @pytest.mark.parametrize("comment_id, update_comment, expected_status", [
        (5, {'body': 'Test-text'}, HTTPStatus.OK),
        (25, {'body': 'text' * 3}, HTTPStatus.OK),
        (73, {'body': 'Test-text'}, HTTPStatus.OK),
        (89, {'body': 'I think I should shift to the moon'}, HTTPStatus.OK)
    ])
    def test_update_comment(self, comments_api, comment_id, update_comment, expected_status, logger):
        with allure.step(
                f"Отправляю PUT-запрос на эндпоинт /comments/{comment_id} с обновленными параметрами: {update_comment}"):
            response = comments_api.update_comments(comment_id, update_comment)
            logger.info(f"Ответ: {response.status_code} - {response.text}")
            assert response.status_code == expected_status, (f"Ожидался статус: {expected_status},"
                                                             f"но пришёл: {response.status_code}")

        if response.status_code == HTTPStatus.OK:
            with allure.step('Проверка валидации данных'):
                try:
                    data = CommentUpdate(**response.json())
                    logger.info('Данные провалидированы')
                except ValidationError as e:
                    logger.error(f'Ошибка валидации данных: {e}')
                    pytest.fail(f"Ошибка валидации: {e}")

    @allure.story("Удаление комментария")
    @pytest.mark.parametrize("comment_id, expected_status", [
        (1, HTTPStatus.OK),
        (29, HTTPStatus.OK),
        (73, HTTPStatus.OK),
        (159, HTTPStatus.OK),
        (322, HTTPStatus.OK),
        (339, HTTPStatus.OK)
    ])
    def test_delete_comment(self, comments_api, comment_id, expected_status, logger):
        with allure.step(f"Отправляю DELETE-запрос на эндпоинт /comments/{comment_id}"):
            response = comments_api.delete_comments(comment_id)
            logger.info(f'Ответ: {response.status_code} - {response.text}')
            assert response.status_code == expected_status, (f"Ожидался статус: {expected_status},"
                                                             f"но пришёл: {response.status_code}")

        if response.status_code == HTTPStatus.OK:
            with allure.step('Проверка валидации данных'):
                try:
                    delete_user = CommentGet(**response.json())
                    logger.info(f'Комментарий удалён: {delete_user}')
                except ValidationError as e:
                    logger.error(f'Ошибка валидации данных: {e}')
                    pytest.fail(f'Ошибка валидации: {e}')

            with allure.step("Проверка, что комментарийк действительно удалён"):
                timeout = 5
                interval = 0.5
                elapsed = 0
                while elapsed < timeout:
                    get_resp = comments_api.get_comments(comment_id)
                    if get_resp.status_code == HTTPStatus.NOT_FOUND:
                        logger.info(f"Комментарий с id={comment_id} успешно удалён")
                        break
                    time.sleep(interval)
                    elapsed += interval
                else:
                    pytest.fail(f"Комментарий с id={comment_id} все ещё существует спустя {timeout} секунд")

