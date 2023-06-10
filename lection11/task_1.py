# Перейти на https://sbis.ru/
# Перейти в раздел "Контакты"
# Найти баннер Тензор, кликнуть по нему
# Перейти на https://tensor.ru/
# Проверить, что есть блок новости "Сила в людях"
# Перейдите в этом блоке в "Подробнее" и убедитесь, что открывается https://tensor.ru/about
# Для сдачи задания пришлите код и запись с экрана прохождения теста


from selenium import webdriver
from selenium.webdriver.common.by import By
import time


browser = webdriver.Chrome()
sbis_site = 'https://sbis.ru/'
# команда time.sleep устанавливает паузу в 2 секунд, чтобы мы успели увидеть, что происходит в браузере
time.sleep(2)
try:
    browser.get("https://sbis.ru")
    assert browser.current_url == sbis_site, 'Неверно открыт сайт'
    time.sleep(2)
    # ищем ссылку контакты
    contacts_button = browser.find_element(By.CSS_SELECTOR,
                                           ".sbisru-Header__menu .sbisru-Header__menu-item [href='/contacts']")
    link_txt = contacts_button.text
    assert link_txt == 'Контакты', f"название ссылки отличается от ожидаемого, на странице : {link_txt}"
    contacts_button.click()
    time.sleep(2)
    # ищем банер тензора
    tensor_button = browser.find_element(By.CSS_SELECTOR, "#contacts_clients .sbisru-Contacts__logo-tensor")
    tensor_button.click()
    time.sleep(2)
    new_window = browser.window_handles[1]
    browser.switch_to.window(new_window)
    # ищем блок новостей по классу ожидаем что в нем будет "сила в людях"
    news_button = browser.find_element(By.CSS_SELECTOR, ".tensor_ru-Index__block4-content")

    # ищем заголовок
    header_block = browser.find_element(By.CSS_SELECTOR,
                                        ".tensor_ru-Index__block4-content .tensor_ru-Index__card-title")
    title = header_block.text
    assert title == 'Сила в людях', f"название блока новостей не совпало с ожидаемым, на странице : {title}"
    # просто для красоты видео
    header_block.location_once_scrolled_into_view

    # ищем все параграфы блока их должно быть 3
    list_block = browser.find_elements(By.CSS_SELECTOR, ".tensor_ru-Index__block4-content .tensor_ru-Index__card-text")
    assert len(list_block) == 3, f"блок новостей содержит не 3 записи, но странице {len(list_block)} записей"
    # ищем ссылку подробней
    more_button = browser.find_element(By.CSS_SELECTOR, ".tensor_ru-Index__block4-content "
                                                        ".tensor_ru-Index__card-text:not(.tensor_ru-pb-16) "
                                                        ".tensor_ru-link")
    link_txt = more_button.text
    assert link_txt == 'Подробнее', f"название ссылки отличается от ожидаемого, на странице : {title}"
    # прокручиваем и кликаем по ссылке, автопрокрутка промахивается попадает в нижнюю панель
    # browser.execute_script("arguments[0].scrollIntoView();", more_button)
    more_button.location_once_scrolled_into_view
    time.sleep(2)
    more_button.click()
    assert browser.current_url == "https://tensor.ru/about", 'Неверно открыт сайт'
    time.sleep(4)

finally:
    browser.quit()
