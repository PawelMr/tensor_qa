from atf.ui import *


class AuthOnline(Region):
    """авторизация и переход на нужную страницу"""

    login = TextField(By.CSS_SELECTOR, '[name="Login"]', 'логин')
    password = TextField(By.CSS_SELECTOR, '[name="Password"]', 'пароль')

    def auth(self, login: str, password: str, site=None):
        """
        Авторизация
        :param login: логин
        :param password: пароль
        :param site: сайт
        """
        if not site:
            site = self.config.get('SITE_MESSAGE')
        self.browser.open(site)
        self.login.type_in(login + Keys.ENTER)
        self.login.should_be(ExactText(login))
        self.password.type_in(password + Keys.ENTER)
        self.browser.should_be(UrlContains(site), msg="страница не открылась")
        self.check_page_load_wasaby()
