from zeep import Client


def send_request(client, data):
    r = client.service.checkText(**data)
    return r


def treatment_response(response, text):
    if response is None:
        from yandex_translate import YandexTranslate
        API = 'trnsl.1.1.20190709T063903Z.7e39efa042c9543b.16ef16a3444c163c8ad03b4d4a2ce728be47a798'
        translate = YandexTranslate(API)
        return translate.translate(text, 'ru-en')
    else:
        return None


def treatment_response_composite(response, text):
    if response is 'Success':
        from yandex_translate import YandexTranslate
        API = 'trnsl.1.1.20190709T063903Z.7e39efa042c9543b.16ef16a3444c163c8ad03b4d4a2ce728be47a798'
        translate = YandexTranslate(API)
        return translate.translate(text, 'ru-en')
    else:
        return None


def treatment_translate(response):
    if response is None:
        print("Введён текст с ошибками!\n")
    else:
        print("Перевод: " + ' '.join(response['text']))


def main_function():
    text = input("Введите текст для перевода: ")
    # cl = Client('http://speller.yandex.net/services/spellservice?WSDL')
    cl = Client('http://DESKTOP-0M0S9AF:8088/mockSpellServiceSoap?WSDL')
    req_data = {'text': text, 'lang': 'ru', 'options': 32,
                'format': 'plain'}
    r = send_request(cl, req_data)
    translate = treatment_response(r, text)
    treatment_translate(translate)


if __name__ == "__main__":
    main_function()


