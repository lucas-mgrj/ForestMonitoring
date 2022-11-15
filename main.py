import json
import time
from datetime import datetime

import requests
import mysql.connector


def f__Configuration():
    global host
    global user
    global password
    global database
    global IsConfigured
    host = input('Digite o "host": ')
    user = input('Digite o "user": ')
    password = input('Digite o "password": ')
    database = input('Digite o "database": ')
    IsConfigured = 1
    host = 'localhost'
    user = 'root'
    password = '22000833lucas!'
    database = 'db_ForestMonitoring'
    return [host, user, password, database, IsConfigured]


def f__DateTime():
    try:
        DateTime = f'{str(datetime.now()).split(" ")[0]} ' \
                   f'{str(datetime.now()).split(" ")[1].split(".")[0].split(":")[0]}' \
                   f':{str(datetime.now()).split(" ")[1].split(".")[0].split(":")[1]}' \
                   f':{str(datetime.now()).split(" ")[1].split(".")[0].split(":")[2]}'
    except:
        DateTime = f'yyyy-mm-dd HH:MM:SS'

    return DateTime


def f__Translate(rawString):
    CookedString = rawString. \
        replace(r'\u00c3', 'Ã'). \
        replace(r'\u00c1', 'Á'). \
        replace(r'\u00d3', 'Ó'). \
        replace(r'\u00cd', 'Í'). \
        replace(r'\u00c2', 'Â'). \
        replace(r'\u00c9', 'É'). \
        replace(r'\u00c7', 'Ç'). \
        replace(r'\u00d5', 'Õ'). \
        replace(r'\u00da', 'Ú'). \
        replace(r'\u00d4', 'Ô'). \
        replace(r'\u00ca', 'Ê')
    return CookedString


def f__SQL(Operation=1,
           vPais='default',
           vEstado='default',
           vMunicipio='default',
           vDataHoraGMT='default',
           vLatitude='default',
           vLongitude='default',
           vSatelite='default',
           vRiscoFogo='default',
           vPrecipitacao='default',
           vNrDiasSemChuva='default',
           vidINPE='default',
           xTimeProgram=''):
    db_connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database,
    )
    cursor = db_connection.cursor()
    if Operation == 1:
        sql = "SELECT latitude, longitude, satelite, " \
              " data_hora_gmt, timeprogram, pais, " \
              " estado, municipio, risco_fogo, " \
              " precipitacao, nr_dias_sem_chuva, idinpe " \
              "FROM " \
              " tbl_pesquisasfeitas"
        cursor.execute(sql)

        for (latitude, longitude, satelite,
             data_hora_gmt, timeprogram, pais,
             estado, municipio, risco_fogo,
             precipitacao, nr_dias_sem_chuva, idinpe) in cursor:
            return f'{latitude}//{longitude}//{satelite}//' \
                   f'{data_hora_gmt}//{timeprogram}//{pais}//' \
                   f'{estado}//{municipio}//{risco_fogo}//' \
                   f'{precipitacao}//{nr_dias_sem_chuva}//{idinpe}'

        cursor.close()
        db_connection.commit()
        db_connection.close()
    elif Operation == 2:
        sql = "INSERT INTO tbl_pesquisasfeitas (" \
              "latitude, " \
              "longitude, " \
              "satelite, " \
              "data_hora_gmt, " \
              "timeprogram, " \
              "pais, " \
              "estado, " \
              "municipio, " \
              "risco_fogo, " \
              "precipitacao, " \
              "nr_dias_sem_chuva, " \
              "idinpe)" \
              "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (vLatitude, vLongitude, vSatelite, vDataHoraGMT, xTimeProgram,
                  vPais, vEstado, vMunicipio, vRiscoFogo, vPrecipitacao, vNrDiasSemChuva, vidINPE)
        cursor.execute(sql, values)
        db_connection.commit()
        db_connection.close()
    elif Operation == 3:
        sql = f'SELECT idinpe FROM tbl_pesquisasfeitas WHERE idinpe = "{vidINPE}"'
        cursor.execute(sql)
        resultado = cursor.fetchall()
        if len(resultado) != 0:
            return 1
        else:
            return 0


def f__req():
    url = requests.get("http://queimadas.dgi.inpe.br/api/focos/?pais_id=33&estado_id=35")
    text = url.text

    rawData = json.loads(text)
    for i in range(len(rawData)):
        cookedData = rawData[i]
        idINPE = cookedData['id']
        Pais = cookedData['properties']['pais']
        Estado = f__Translate(cookedData['properties']['estado'])
        Municipio = f__Translate(cookedData['properties']['municipio'])
        DataHoraGMT = cookedData['properties']['data_hora_gmt']
        Latitude = cookedData['properties']['latitude']
        Longitude = cookedData['properties']['longitude']
        Satelite = cookedData['properties']['satelite']
        RiscoFogo = cookedData['properties']['risco_fogo']
        Precipitacao = cookedData['properties']['precipitacao']
        NrDiasSemChuva = cookedData['properties']['numero_dias_sem_chuva']
        TimeSearch = f__DateTime().split(" ")[1]
        if RiscoFogo is None:
            RiscoFogo = "S/D"
        if Precipitacao is None:
            Precipitacao = "S/D"
        if NrDiasSemChuva is None:
            NrDiasSemChuva = "S/D"

        IsExist = f__SQL(Operation=3, vidINPE=idINPE)
        if IsExist == 1:
            print(f'{f__DateTime()} --> Dado já existente no banco, \n\tid: {idINPE}\n\n')
        elif IsExist == 0:
            print('\nPais: ', Pais,
                  '\nEstado: ', Estado,
                  '\nMunicípio: ', Municipio,
                  '\nDataHoraGMT: ', DataHoraGMT,
                  '\nLatitude: ', Latitude,
                  '\nLongitude', Longitude,
                  '\nSatelite: ', Satelite,
                  '\nRisco de Fogo: ', RiscoFogo,
                  '\nPrecipitacao: ', Precipitacao,
                  '\nNr de Dias Sem Chuva:', NrDiasSemChuva,
                  '\nID INPE: ', idINPE)

            f__SQL(Operation=2,
                   vPais=Pais,
                   vEstado=Estado,
                   vMunicipio=Municipio,
                   vDataHoraGMT=DataHoraGMT,
                   vLatitude=Latitude,
                   vLongitude=Longitude,
                   vSatelite=Satelite,
                   vRiscoFogo=RiscoFogo,
                   vPrecipitacao=Precipitacao,
                   vNrDiasSemChuva=NrDiasSemChuva,
                   vidINPE=idINPE,
                   xTimeProgram=TimeSearch)


if __name__ == '__main__':
    f__Configuration()
    while True:
        f__req()
        time.sleep(600)
