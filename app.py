from pywebio.input import *
from pywebio.output import *

import xlsxwriter
import math
import pandas as pd

from pywebio import config
from pywebio import start_server
from pywebio.session import run_js

from pywebio.platform.flask import webio_view
from pywebio import STATIC_PATH
from flask import Flask, send_from_directory
import argparse

app = Flask(__name__)

@config(theme="dark")


def app2():
    """
    C-Safe Zone
    """
    put_text("C-Safe Zone").style('text-align:center; color: red; font-size: 40px'),
    put_markdown("## Mencegah Pasang Baru Di Lokasi Bermasalah").style('text-align:center; color:Grey; font-size: 20px'),

    inputan()
    
def inputan():
    file=input_group(
        'Cek Data Pasang Baru dan TO Persil',[
            file_upload('Data PB :',name='pb', accept='.csv', multiple=False),
            file_upload('Data Persil :',name='persil', accept='.csv', multiple=False),
            input('Input radius periksa (m)', name='jarak2', type=FLOAT)
         ])

    open(str(file['pb']['filename']), 'wb').write(file['pb']['content'])
    data_pb = pd.read_csv(str(file['pb']['filename']))
    
    open(str(file['persil']['filename']), 'wb').write(file['persil']['content'])
    data_persil = pd.read_csv(str(file['persil']['filename']))

    jml_data_persil=data_persil.index
    jml_data_pb=data_pb.index

    inpradius=file['jarak2']

    hitungan(jml_data_persil, jml_data_pb, data_persil, data_pb, inpradius)

def hitungan(jml_data_persil, jml_data_pb, data_persil, data_pb, inpradius):
    
    hasil = []
    for i in jml_data_persil:
        data = {}
        data['IDPelTO'] = data_persil['IDPel'][i]
        data['NamaTO'] = data_persil['Nama'][i]
        data['TarifTO'] = data_persil['Tarif'][i]
        data['DayaTO'] = data_persil['Daya'][i]
        data['TanggalTO'] = data_persil['Tanggal'][i]
        data['Koordinat'] = data_persil['Koordinat'][i]
        data['Keterangan'] = data_persil['Temuan'][i]

        IDPelTO = data['IDPelTO']
        NamaTO = data['NamaTO']
        TarifTO = data['TarifTO']
        DayaTO = data['DayaTO']
        TanggalTO = data['TanggalTO']
        KoordinatTO = data['Koordinat']
        Keterangan = data['Keterangan']
    
        koordinat=data['Koordinat']
        x,y=koordinat.split(',')[0],koordinat.split(',')[1]
        long=float(x)
        lat=float(y)

        for j in jml_data_pb:
            data2 = {}
            data2['IDPelPB'] = data_pb['IDPel'][j]
            data2['NamaPB'] = data_pb['Nama'][j]
            data2['TanggalPB'] = data_pb['Tanggal Pasang'][j]
            data2['Koordinat2'] = data_pb['Lokasi'][j]

            IDPelPB = data2['IDPelPB']
            NamaPB = data2['NamaPB']
            TanggalPB = data2['TanggalPB']
            KoordinatPB = data2['Koordinat2']

            koordinat2=data_pb['Lokasi'][j]
            x1,y1=koordinat2.split(',')[0],koordinat2.split(',')[1]
            long1=float(x1)
            lat1=float(y1)

            jarak=round((math.sqrt(((long1-long)**2)+((lat1-lat)**2)))*110567)

            if jarak <= inpradius:
                
                row = [IDPelPB, NamaPB, TanggalPB, KoordinatPB, IDPelTO, NamaTO, TarifTO, DayaTO, TanggalTO, KoordinatTO, Keterangan, jarak]
                hasil.append(row)
    

    put_table(hasil, header=['IDPel PB', 'Nama PB', 'Tanggal Pasang','Koordinat PB', 'IDPel TO', 'Nama TO', 'Tarif TO', 'Daya TO', 'Tanggal Temuan', 'Koordinat TO', 'Keterangan TO', 'Jarak (m)'])

    put_button("Kembali",onclick=lambda: run_js('window.location.reload()'))

#if __name__ == '__main__':
#    start_server(app, port=80)
app.add_url_rule('/tool', 'webio_view', webio_view(app2),
		 methods=['GET', 'POST', 'OPTIONS'])

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, default=8888)
    args = parser.parse_args()

    start_server(app2, port=args.port)
