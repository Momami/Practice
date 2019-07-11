import xml.etree.ElementTree as ET
import pyodbc
from datetime import datetime
from typing import Dict, Any
from zeep import Client
from zeep.wsdl.utils import etree_to_string
import pandas as pd


def recieve_valuteID(cnn):
    data = pd.read_sql("select ValuteID, RateDate from Rate", cnn)
    valutes = list(data['ValuteID'])
    date = list(data['RateDate'])
    valute_date = dict()
    for i in range(len(valutes)):
        valute_date[valutes[i]] = datetime.strptime(date[i], '%Y-%m-%d')
    return valute_date


def connect_db():
    server = 'DESKTOP-0M0S9AF'
    database = 'ValuteDB'
    driver = '{SQL Server}'  # Driver you need to connect to the database
    cnn = pyodbc.connect(
        'DRIVER=' + driver + ';PORT=port;SERVER=' + server + ';PORT=1443;DATABASE=' + database + '')
    return cnn


def find_rate_in_DB(valute_name, cnn):
    data = pd.read_sql("select RateVal from Rate where ValuteID = '" + valute_name + "'", cnn)
    return valute_name, data['RateVal'][0]


def main_function():
    day_actual = 1
    result, upgrade = [], []
    title = "Введите валюты для получения курса: \n" \
            "(ввод осуществляется через пробел в одну строку)\n"
    valutes = input(title).split()
    date = datetime.strptime(input("Введите дату в формате DD-MM-YYYY: "),
                             '%d-%m-%Y')
    conn = connect_db()
    val_day: Dict[Any, datetime] = recieve_valuteID(conn)
    for valute in valutes:
        if valute in val_day.keys():
            if (date - val_day[valute]).days <= day_actual or \
                    (val_day[valute] - date).days > 0:
                result.append(find_rate_in_DB(valute, conn))
                continue
        upgrade.append(valute)
    mas_update = update_rate(upgrade, date)
    for elem, rate in mas_update.items():
        if elem in val_day.keys():
            update_DB(elem, rate, date, conn)
        else:
            insert_DB(elem, rate, date, conn)
        result.append((elem, rate))
    print_result(result)


def print_result(result):
    print("Курсы валют\n")
    for elem, rate in result:
        print('{0}: {1}'.format(elem, rate))


def update_DB(elem, rate, date, conn):
    pd.read_sql("update Rate SET RateVal = '" + rate +
                "', RateDate = '" + date + "' WHERE ValuteID = '" + elem + "'", conn)


def insert_DB(elem, rate, date, conn):
    pd.read_sql("insert into Rate (ValuteID, RateVal, RateDate) VALUES ('" +
                elem + "', '" + rate + "', '" + date + "')", conn)


def send_request(cl, data):
    resp = cl.service.GetCursOnDateXML(On_date=data)
    return resp


def send_enumXML(cl):
    resp = cl.service.EnumValutesXML(False)
    return resp


def enum_valutes(cl, upg):
    res = []
    exc = []
    response = send_enumXML(cl)
    dom = ET.fromstring(etree_to_string(response).decode())
    for elem in upg:
        current = dom.findall(
            './[VCharCode = "' + elem + '"]'
        )
        if not current is None:
            res.append(elem)
        else:
            exc.append((elem, "Not Found"))
    return res, exc


def update_rate(upgrade, date):
    client = Client("http://www.cbr.ru/DailyInfoWebServ/DailyInfo.asmx?WSDL")
    date = datetime.now()
    # validate_valute, non_validate = enum_valutes(client, upgrade)

    response = send_request(client, date)

    dom = ET.fromstring(etree_to_string(response).decode())
    currencies = []
    needed_currencies = dict()
    print(upgrade)
    for elem in upgrade:
        new_elem = dom.findall(
            './ValuteCursOnDate[VchCode = "' + elem + '"]'  # /Vcurs
            # , namespaces
        )
        if not new_elem is None:
            currencies.append(new_elem)
        else:
            needed_currencies[elem] = 'Not Found'

    for valute in currencies:
        name = ''
        value = ''
        for node in valute.getiterator():
            if node.tag == 'VchCode':
                name = node.text
            if node.tag == 'Vcurs':
                value = node.text
        needed_currencies[name] = value

    for name, value in needed_currencies.items():
        print(name + ': ' + value)
    return needed_currencies


if __name__ == "__main__":
    main_function()
