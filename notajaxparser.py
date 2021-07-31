import requests
base_api_url = 'https://urfu.ru/api/ratings/departmental/1/'
base_page_get_url = 'https://urfu.ru/'
api_urls = {
    'ienim' : '4/1/',
    'inmt' : '17/1/',
    'rtf' : '7/1/',
    'isa' : '12/1/',
    'ipe' : '9/1/',
    'ifo' : '10/1/',
    'ieu' : '25/1/',
    'ugi' : '19/1/',
    'uei' : '13/1/',
    'fti' : '14/1/',
    'xti' : '15/1/',
}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36 OPR/77.0.4054.277',
}

def get_abit_status(instit,fio):
    try:
        url = requests.get(base_api_url + api_urls[instit], headers=headers).json()['url']
        page_source = requests.get(base_page_get_url + url, headers=headers).content.decode()
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
