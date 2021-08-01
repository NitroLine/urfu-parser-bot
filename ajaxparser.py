from contextlib import closing

from selenium.webdriver import Chrome  # pip install selenium
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

# use chrome to get page with javascript generated content
url = "https://urfu.ru/ru/ratings/"
alph = "АБВГДЕЖЗИКЛМНОПРСТУФХЦЧШЩЭЮЯ"
ans = 0
table = []


def get_abit_status(instit, fio):
    try:
        with closing(Chrome(ChromeDriverManager().install())) as browser:
            fio = str(fio)
            browser.get(url)
            WebDriverWait(browser, timeout=50).until(
                lambda x: x.find_element_by_class_name('urfu-admission-faculties'))
            button = browser.find_elements_by_xpath("//*[contains(text(), '{0}')]/../td[2]/ul/li/a".format(instit))
            button[0].click()
            WebDriverWait(browser, timeout=50).until(
                lambda x: x.find_element_by_class_name('etableTitle'))
            page_source = browser.page_source
            num_page = page_source.find(fio)
            if num_page == -1:
                ans = "Не нашли вас в списках ☹️ Проверьте институт и рег. номер."
            else:
                if not page_source[num_page + len(fio) + 2].isdigit():
                    ans = "Вы не проходите по конкурсу на бюджет 😥 (или ещё не подали согласие на зачислениe)"
                else:
                    num = page_source[num_page + len(fio) + 2]
                    if page_source[num_page + len(fio) + 3].isdigit():
                        num += page_source[num_page + len(fio) + 3]
                    ans = "Ваше место в рейтинге 😉: " + num
        print(ans)
        return ans
    except Exception as e:
        print(e)
        return "Произошла ошибка сервера 😰"
