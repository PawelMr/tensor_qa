# Есть маркер @pytest.mark.id_check(1, 2, 3), нужно вывести на печать, то что в него передано
#
# >>> 1, 2, 3
import logging
import pytest


logging.basicConfig(level=logging.INFO)


@pytest.mark.id_check(1, 2, 3)
def test(request):
    """
    тест с записью лога
    логирование настроено в pytest.ini
    """
    mark = request.node.get_closest_marker("id_check")
    logging.info(f" в id_check переданы {mark.args}")


