import pytest
import logging

from src.api.users_api import UsersAPI
from src.api.products_api import ProductsAPI
from src.api.carts_api import CartsAPI
from src.api.recipes_api import RecipesAPI
from src.api.posts_api import PostsAPI
from src.api.comments_api import CommentsAPI
from src.api.todos_api import TodosAPI
from src.api.login_api import LoginAPI

@pytest.fixture(scope='session')
def base_url():
    return 'https://dummyjson.com'

@pytest.fixture(scope='session')
def users_api(base_url):
    return UsersAPI(base_url=base_url)

@pytest.fixture(scope='session')
def products_api(base_url):
    return ProductsAPI(base_url=base_url)

@pytest.fixture(scope='session')
def carts_api(base_url):
    return CartsAPI(base_url=base_url)

@pytest.fixture(scope='session')
def recipes_api(base_url):
    return RecipesAPI(base_url=base_url)

@pytest.fixture(scope='session')
def posts_api(base_url):
    return PostsAPI(base_url=base_url)

@pytest.fixture(scope='session')
def comments_api(base_url):
    return CommentsAPI(base_url=base_url)

@pytest.fixture(scope='session')
def todos_api(base_url):
    return TodosAPI(base_url=base_url)

@pytest.fixture(scope='session')
def login_api(base_url):
    return LoginAPI(base_url=base_url)

@pytest.fixture(scope='session', autouse=True)
def logger():
    """Создание логгера"""
    logger = logging.getLogger()
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler('logs/api.log', encoding='utf-8', mode='w')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger

@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    """Конфиг для интеграции Allure"""


    # Настройка
    if hasattr(config, "option"):
        allure_dir = getattr(config.option, 'alluredir', None)
        if allure_dir:
            logging.info(f"Allure-отчёты сохранены в: {allure_dir}")

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Хук для добавление шагов в Allure"""
    outcome = yield
    report = outcome.get_result()

    if report.when == 'call' and report.failed:
        from allure_commons._allure import attach
        from allure_commons.types import AttachmentType

        # Добавление данных в отчёт при провале теста
        attach(
            body=str(report.longrepr),
            name="Test Failure Log",
            attachment_type=AttachmentType.TEXT
        )
