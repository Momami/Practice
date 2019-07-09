from spyne import Application, rpc, ServiceBase, Unicode
from lxml import etree
from spyne.protocol.soap import Soap11
from spyne.protocol.json import JsonDocument
from spyne.server.wsgi import WsgiApplication
from yandex_translate import YandexTranslate

class Soap(ServiceBase):
    @rpc(Unicode, _returns=Unicode)
    def Insoap(ctx, words):
        print(etree.tostring(ctx.in_document))
        translate = YandexTranslate('trnsl.1.1.20190709T063903Z.7e39efa042c9543b.16ef16a3444c163c8ad03b4d4a2ce728be47a798')
        tr = translate.translate(words, 'en')
        tr_answer = tr['text'][0]
        return tr_answer
app = Application([Soap], tns='Translator',
                          in_protocol=Soap11(validator='lxml'),
                         out_protocol=Soap11())
application = WsgiApplication(app)
if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    server = make_server('0.0.0.0', 8000, application)
    server.serve_forever()
