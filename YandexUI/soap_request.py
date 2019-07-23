from zeep import Client
from yandex_translate import YandexTranslate

list_lang = None


def send_request(client, data):
    r = client.service.CheckText(data)
    return r

def send_request_not_comp(client, data):
    r = client.service.checkText(**data)
    return r

def treatment_opt(text):
    API = 'trnsl.1.1.20190709T063903Z.7e39efa042c9543b' \
          + '.16ef16a3444c163c8ad03b4d4a2ce728be47a798'
    return YandexTranslate(API)


def treatment(text):
    translate = treatment_opt(text)
    print("Выберите целевой язык: \n")
    list_lang = list(translate.langs)
    for num, lan in enumerate(list_lang):
        print('{} - {}'.format(num, lan), end=' ')
        if (num + 1) % 5 == 0:
            print()
    print()
    lang = input()
    while not lang.isdigit() and int(lang) > 32:
        lang = input("Неверно введен номер языка! \n Попробуйте еще раз.\n")
    return translate.translate(text, list_lang[int(lang)])


def treat(text, lang):
    translate = treatment_opt(text)
    return translate.translate(text, lang)


# обработка при прямом подключении к YandexSpeller
def treatment_response(response, text, lang):
    if response is None:
        return treat(text, lang)
    else:
        return None


# обработка при работе с композитом
def treatment_response_composite(response, text):
    if response == 'Success':
        return treatment(text)
    else:
        return None


def treatment_translate(response):
    if response is None:
        print("Введён текст с ошибками!\n")
    else:
        print("Перевод: " + ' '.join(response['text']))


def link_wsdl():
    wsdl = 'http://speller.yandex.net/services/spellservice?WSDL'
    cl = Client(wsdl)
    return cl


def main_ui(text, lang, check):
    cl = link_wsdl()
    req_data = {'text': text, 'lang': 'en', 'options': 32,
                'format': 'plain'}
    if check:
        r = send_request_not_comp(cl, req_data)
    else:
        r = None
    translate = treatment_response(r, text, lang)
    if translate is None:
        return None
    else:
        return ' '.join(translate['text'])


def main_function():
    text = input("Введите текст для перевода: ")
    wsdl = 'http://ulbs12-sales-app01.neoflex.ru:' \
           + '8001/soa-infra/services/default/Project1/MySpellerWebService?WSDL'
    wsdl_clean = 'http://speller.yandex.net/services/spellservice?WSDL'
    # cl = Client(wsdl)
    cl = Client(wsdl_clean)
    req_data = {'text': text, 'lang': 'en', 'options': 32,
                'format': 'plain'}

    r = send_request_not_comp(cl, req_data)
    # r = send_request(cl, text)
    translate = treatment_response(r, text, 'ru')
    # translate = treatment_response_composite(r, text)
    treatment_translate(translate)


def get_lang():
    tr = treatment_opt('api')
    list_lang = list(tr.langs)
    list_lang.sort()
    return list_lang


if __name__ == "__main__":
    main_function()
