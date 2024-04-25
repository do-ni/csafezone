import streamlit as st
import pandas as pd
import math

def main():
    """
    C-Safe Zone
    """
    st.title("C-Safe Zone")
    st.markdown("## Mencegah Pasang Baru Di Lokasi Bermasalah")

    inputan()

def inputan():
    pb_file = st.file_uploader("Upload Data PB (CSV)", type=["csv"])
    persil_file = st.file_uploader("Upload Data Persil (CSV)", type=["csv"])
    jarak = st.number_input("Input radius periksa (m)")

    if pb_file and persil_file:
        data_pb = pd.read_csv(pb_file)
        data_persil = pd.read_csv(persil_file)

        hitungan(data_pb, data_persil, jarak)

def hitungan(data_pb, data_persil, inpradius):
    hasil = []

    for i, persil_row in data_persil.iterrows():
        for j, pb_row in data_pb.iterrows():
            koordinat = persil_row['Koordinat'].split(',')
            koordinat2 = pb_row['Lokasi'].split(',')

            long, lat = float(koordinat[0]), float(koordinat[1])
            long1, lat1 = float(koordinat2[0]), float(koordinat2[1])

            jarak = round(math.sqrt(((long1 - long) ** 2) + ((lat1 - lat) ** 2)) * 110567)

            if jarak <= inpradius:
                row = [
                    pb_row['IDPel'], pb_row['Nama'], pb_row['Tanggal Pasang'], pb_row['Lokasi'],
                    persil_row['IDPel'], persil_row['Nama'], persil_row['Tarif'], persil_row['Daya'],
                    persil_row['Tanggal'], persil_row['Koordinat'], persil_row['Temuan'], jarak
                ]
                hasil.append(row)

    if hasil:
        st.write(pd.DataFrame(hasil, columns=[
            'IDPel PB', 'Nama PB', 'Tanggal Pasang', 'Koordinat PB',
            'IDPel TO', 'Nama TO', 'Tarif TO', 'Daya TO', 'Tanggal Temuan',
            'Koordinat TO', 'Keterangan TO', 'Jarak (m)'
        ]))
    else:
        st.write("Tidak ada hasil yang ditemukan.")

if __name__ == '__main__':
    main()
