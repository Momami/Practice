from zeep import Client


def send_request(client, data):
    r = client.service.CheckText(data)
    return r

# обработка при прямом подключении к YandexSpeller
def treatment_response(response, text):
    if response is None:
        from yandex_translate import YandexTranslate
        API = 'trnsl.1.1.20190709T063903Z.7e39efa042c9543b' \
              + '.16ef16a3444c163c8ad03b4d4a2ce728be47a798'
        translate = YandexTranslate(API)
        return translate.translate(text, 'ru')
    else:
        return None

# обработка при работе с композитом
def treatment_response_composite(response, text):
    if response == 'Success':
        from yandex_translate import YandexTranslate
        API = 'trnsl.1.1.20190709T063903Z.7e39efa042c9543b' \
              + '.16ef16a3444c163c8ad03b4d4a2ce728be47a798'
        translate = YandexTranslate(API)
        return translate.translate(text, 'ru')
    else:
        return None


def treatment_translate(response):
    if response is None:
        print("Введён текст с ошибками!\n")
    else:
        print("Перевод: " + ' '.join(response['text']))


def main_function():
    text = input("Введите текст для перевода: ")
    wsdl = 'http://ulbs12-sales-app01.neoflex.ru:' \
           + '8001/soa-infra/services/default/Project1/MySpellerWebService?WSDL'
    cl = Client(wsdl)
    # req_data = {'text': text, 'lang': 'en', 'options': 32,
    #             'format': 'plain'}

    r = send_request(cl, text)
    # translate = treatment_response(r, text)
    translate = treatment_response_composite(r, text)
    treatment_translate(translate)


if __name__ == "__main__":
    main_function()
