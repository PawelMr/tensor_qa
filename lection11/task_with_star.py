# Перейти на  https://sbis.ru/
# В Footer'e найти "Скачать СБИС"
# Перейти по ней
# Скачать СБИС Плагин для вашей ОС в папку с данным тестом
# Убедиться, что плагин скачался
# Вывести на печать размер скачанного файла в мегабайтах
# Для сдачи задания пришлите код и запись с экрана прохождения теста


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
# import wget
import os


download_dir = os.path.abspath(".")

# https://spurqlabs.com/how-to-download-a-file-using-python-and-selenium/
chrome_options = Options()
# производительность но на сбис ру не заметна
# chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--verbose')
# chrome_options.add_argument('--disable-gpu')
# chrome_options.add_argument('--disable-software-rasterizer')

# это должно отключать
# chrome_options.add_argument("--disable-notifications")
# chrome_options.add_argument("--safebrowsing-disable-download-protection")
chrome_options.add_experimental_option("prefs", {
    "download.default_directory": download_dir,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
})


browser = webdriver.Chrome(options=chrome_options)

sbis_site = 'https://sbis.ru/'
# команда time.sleep устанавливает паузу в 2 секунд, чтобы мы успели увидеть, что происходит в браузере
time.sleep(2)
try:
    browser.get("https://sbis.ru")
    assert browser.current_url == sbis_site, 'Неверно открыт сайт'
    time.sleep(2)
    download_link = browser.find_element(By.XPATH,
                                         '//a[text()="Скачать СБИС"]')
    download_link.location_once_scrolled_into_view
    download_link.click()
    time.sleep(2)

    plugin_button = browser.find_element(By.CSS_SELECTOR,
                                         '[data-id="plugin"]')
    plugin_button.click()
    time.sleep(3)

    plugin_link = browser.find_element(By.XPATH,
                                       "//a[contains(text(), 'Exe')]")

    plugin_link.click()
    time.sleep(5)
    list_name_file_plugin = [i for i in os.listdir('.') if "sbisplugin-setup-web" in i]
    if len(list_name_file_plugin) == 0:
        raise AssertionError(" не скачался файл")
    elif len(list_name_file_plugin) == 1:
        name_file = 'sbisplugin-setup-web.exe'
    else:
        list_name_file_plugin.remove('sbisplugin-setup-web.exe')
        dict_file = {int(i.rstrip(").exe").lstrip("sbisplugin-setup-web (")): i for i in list_name_file_plugin}
        key = max(dict_file)
        name_file = dict_file[key]

    file_size = os.stat(name_file).st_size / (1024 ** 2)
    print(f"скачен файл: '{name_file}'\n"
          f"Размер: {file_size} Mb")

    # # а так было бы проще
    # url_plugin = plugin_link.get_attribute("href")
    # list_name_file_folder = os.listdir('.')
    # list_name_file_plugin = [i for i in list_name_file_folder if "plugin" in i]
    # name_file = f"plugin_{len(list_name_file_plugin)}.exe"
    # wget.download(url_plugin, name_file)
    # file_size = os.stat(name_file).st_size / (1024**2)
    # print(f"скачен файл: {name_file}\n"
    #       f"Размер: {file_size} Mb")

finally:
    browser.quit()

