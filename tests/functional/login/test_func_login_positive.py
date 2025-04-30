import allure
import pytest
from http import HTTPStatus

@pytest.mark.positive
@allure.epic("Функциональное тестирование авторизации")
@allure.feature("Положительные кейсы")
class TestLoginPositive:

    @allure.story("Авторизация")
    @pytest.mark.parametrize("user_data, expected_status", [
        ({'username': 'kminchelle', 'password': '0lelplR'}, HTTPStatus.OK),
    ])
    def test_login(self, login_api, user_data, expected_status, logger):
        with allure.step(f"Отправляю POST-запрос на эндпоинт /auth/login с параметрами: {user_data}"):
            response = login_api.login(user_data)
            logger.info(f'Ответ: {response.status_code} - {response.text}')
            assert response.status_code == expected_status, (f"Ожидался статус: {expected_status},"
                                                             f"но пришёл: {response.status_code}")
