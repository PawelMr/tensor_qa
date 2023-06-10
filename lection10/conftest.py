import pytest
import time


@pytest.fixture()
def delta_time_test():
    """
    Фикстуру для конкретного теста выводит время выполнения теста.
    """
    start_time = time.time()
    yield
    end_time = time.time()
    print(f"время выполнения теста{end_time-start_time}")


@pytest.fixture(scope="class")
def class_fixture():
    start_time = time.time()
    yield
    end_time = time.time()
    print(f"Время начала выполнения класса тестов: {start_time}")
    print(f"Время окончания выполнения класса тестов: {end_time}")