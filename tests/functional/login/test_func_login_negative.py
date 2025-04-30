import allure
import pytest
from http import HTTPStatus

@pytest.mark.negative
@allure.epic("Функциональное тестирование авторизации")
@allure.feature("Негативные кейсы")
class TestLoginNegative:

    @allure.story("Авторизация")
    @pytest.mark.parametrize("user_data, expected_status", [
        ({'username': 'atuny0', 'password': '9uQFF1Lh'}, HTTPStatus.NOT_FOUND),
        ({'username': 'hbingley1', 'password': 'CQutx25i8r'}, HTTPStatus.NOT_FOUND),
        ({'username': 'rshawe2', 'password': 'mSZJtB'}, HTTPStatus.NOT_FOUND),
    ])
    def test_login(self, login_api, user_data, expected_status, logger):
        with allure.step(f"Отправляю POST-запрос на эндпоинт /auth/login с параметрами: {user_data}"):
            response = login_api.login(user_data)
            logger.info(f'Ответ: {response.status_code} - {response.text}')
            assert response.status_code == expected_status, (f"Ожидался статус: {expected_status},"
                                                             f"но пришёл: {response.status_code}")
