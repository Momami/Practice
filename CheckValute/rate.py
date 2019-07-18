import xml.etree.ElementTree as ET
from datetime import datetime
from zeep import Client
from zeep.wsdl.utils import etree_to_string
import pandas as pd
from sqlalchemy import create_engine
from urllib import parse


def recieve_valuteID(cnn):
    data = pd.read_sql("select ValuteID, RateDate from Rate", cnn)
    valutes = list(data['ValuteID'])
    date = list(data['RateDate'])
    valute_date = dict()
    for i in range(len(valutes)):
        valute_date[valutes[i]] = datetime.strptime(date[i], '%Y-%m-%d')
    return valute_date


def connect_db():
    params = parse.quote_plus(r'DRIVER={SQL Server};SERVER=DESKTOP-0M0S9AF;'
                              r'DATABASE=ValuteDB;Trusted_Connection=yes')
    conn_str = 'mssql+pyodbc:///?odbc_connect={}'.format(params)
    engine = create_engine(conn_str)
    return engine


def find_rate_in_DB(valute_name, cnn, res):
    data = pd.read_sql("select RateVal from Rate where ValuteID = '" + valute_name + "'", cnn)
    res[valute_name] = data['RateVal'][0]


def main_function():
    day_actual = 1
    result, upgrade = dict(), []
    title = "Введите валюты для получения курса: \n" \
            "(ввод осуществляется через пробел в одну строку)\n"
    valutes = input(title).split()
    date = datetime.strptime(input("Введите дату в формате DD-MM-YYYY: "),
                             '%d-%m-%Y')
    conn = connect_db()
    val_day = recieve_valuteID(conn)
    for valute in valutes:
        if valute in val_day.keys():
            if (date - val_day[valute]).days <= day_actual or \
                    (val_day[valute] - date).days > 0:
                find_rate_in_DB(valute, conn, result)
                continue
        upgrade.append(valute)
    # раскоментировать при работе напрямую с ЦБ
    # mas_update, non_valid = update_rate(upgrade, date)
    # раскомментировать при работе с композитом
    mas_update, non_valid = update_rate_composite(upgrade, date)
    for elem, rate in mas_update.items():
        if elem in val_day.keys():
            update_DB(elem, rate, date, conn)
        else:
            insert_DB(elem, rate, date, conn)
        result[elem] = rate
    result.update(non_valid)
    print_result(result)


def print_result(result):
    print("Курсы валют\n")
    for elem, rate in result.items():
        print('{0}: {1}'.format(elem, rate))


def update_DB(elem, rate, date, conn):
    data = pd.read_sql("select * from Rate", conn)
    dt = str(date.date())
    data.loc[data['ValuteID'] == elem, 'RateVal'] = [rate]
    data.loc[data['ValuteID'] == elem, 'RateDate'] = [dt]
    data.reset_index(drop=True, inplace=True)
    data.to_sql("Rate", conn, if_exists="replace", index=False)


def insert_DB(elem, rate, date, conn):
    dt = str(date.date())
    df1 = pd.DataFrame.from_dict({'ValuteID': [elem], 'RateVal': [rate], 'RateDate': [dt]})
    df1.to_sql("Rate", conn, if_exists='append', index=False)


def send_request(cl, data):
    resp = cl.service.GetCursOnDateXML(On_date=data)
    return resp


def send_enumXML(cl):
    resp = cl.service.EnumValutesXML(False)
    return resp


def enum_valutes(cl, upg):
    res = []
    exc = dict()
    response = send_enumXML(cl)
    dom = ET.fromstring(etree_to_string(response).decode())
    for elem in upg:
        current = dom.findall(
            './EnumValutes[VcharCode="' + elem + '"]'
        )
        if current:
            res.append(elem)
        else:
            exc[elem] = "Valute Not Found"
    return res, exc


# поиск курса валюты без композита (напрямую с ЦБ)
def update_rate(upgrade, date):
    client = Client("http://www.cbr.ru/DailyInfoWebServ/DailyInfo.asmx?WSDL")
    validate_valute, non_validate = enum_valutes(client, upgrade)

    response = send_request(client, date)

    dom = ET.fromstring(etree_to_string(response).decode())

    needed_currencies = dict()
    for elem in validate_valute:
        new_elem = dom.findall(
            "./ValuteCursOnDate[VchCode='" + elem + "']"  # /Vcurs
            # , namespaces
        )
        if not new_elem:
            non_validate[elem] = 'Curs Not Found'
        for valute in new_elem:
            name = ''
            value = ''
            for node in valute.getiterator():
                if node.tag == 'VchCode':
                    name = node.text
                if node.tag == 'Vcurs':
                    value = node.text
            needed_currencies[name] = value

    #for name, value in needed_currencies.items():
    #    print(name + ': ' + value)

    return needed_currencies, non_validate


# запрос к композиту
def send_composite(client, data):
    r = client.service.execute(**data)
    return r


# поиск курса валюты с помощью композита
def update_rate_composite(upgrade, date):
    # изменить строку на WSDL сервиса композита
    wsdl = 'http://ulbs12-sales-app01.neoflex.ru:8001/soa-infra/services/default/Project3/MyUpdateRate?WSDL'
    client = Client(wsdl)
    req_data = {'dateOnValute': date, 'valute': upgrade}

    response = send_composite(client, req_data)

    non_valid, result = dict(), dict()
    for valute in response:
        name, value = valute['name'], valute['value']
        if value == 'Curs Not Found' or value == 'Valute Not Found':
            non_valid[name] = value
        else:
            result[name] = value
    return result, non_valid


if __name__ == "__main__":
    main_function()
