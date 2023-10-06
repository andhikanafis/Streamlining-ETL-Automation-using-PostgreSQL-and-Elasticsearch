'''
=================================================
Graded Challenge 7

Nama  : Andhika Abdurachim Nafis
Batch : HCK-007

Program ini dirancang untuk mengotomatisasi transformasi dan pengisian data dari database PostgreSQL ke Elasticsearch.
Data yang di digunakan Graded Challenge ini berfokus untuk mengenali faktor-faktor yang memengaruhi tingkat attrition (keluar) karyawan di perusahaan.
=================================================
'''

# Import library yang akan di pakai
import pandas as pd
from elasticsearch import Elasticsearch
import psycopg2 as db

# Koneksi ke database PostgreSQL
conn_string = "dbname='db_phase2' host='localhost' user='postgres' password='123456'"
conn = db.connect(conn_string)

# Membaca data dari database PostgreSQL
df = pd.read_sql("SELECT * FROM table_gc7", conn)

# Menyimpan data dalam file CSV
df.to_csv('P2G7_Andhika-Nafis_Data_Raw.csv', index=False)
print("-------Data Saved------")


def preprocess_data(df):
    '''
   Fungsi ini digunakan untuk melakukan preprocessing data dalam dataframe.

  Parameters:
   df: pandas.DataFrame - dataframe yang akan diolah

  Return
   df: pandas.DataFrame - dataframe yang telah di-preprocesss
     
    Contoh Penggunaan:

    # 1. Membaca data dari file CSV
    df = pd.read_csv('data_employee.csv')

    # 2. Memanggil fungsi preprocess_data untuk preprocessing data
    df = preprocess_data(df)
  '''
    
    # Transformasi tipe data yang tidak cocok, kolom-kolom 'Age', 'EmployeeNumber', dan 'MonthlyIncome' akan diubah dari tipe data objek menjadi tipe data integer, yang lebih sesuai untuk tipe data ini.
    data_type = ['Age', 'EmployeeNumber', 'MonthlyIncome'] # Age, EmployeeNumber, dan MonthlyIncome seharusnya tipe int, bukan object
    df[data_type] = df[data_type].astype(int)
    
    # Bagian ini menggantikan nilai-nilai dalam kolom-kolom tertentu dalam dataframe df dengan nilai-nilai yang sesuai berdasarkan mapping yang diberikan.
    mapping = {
        'EnvironmentSatisfaction': {1: 'Low', 2: 'Medium', 3: 'High', 4: 'Very High'},
        'Education': {1: 'Below College', 2: 'College', 3: 'Bachelor', 4: 'Master', 5: 'Doctor'},
        'JobInvolvement': {1: 'Low', 2: 'Medium', 3: 'High', 4: 'Very High'},
        'PerformanceRating': {1: 'Bad', 2: 'Good'},
        'WorkLifeBalance': {1: 'Bad', 2: 'Good', 3: 'Better', 4: 'Best'},
        'RelationshipSatisfaction': {1: 'Low', 2: 'Medium', 3: 'High', 4: 'Very High'}
    }

    df.replace(mapping, inplace=True)

    # mengubah nama semua kolom dalam dataframe df menjadi huruf kecil (lowercase)
    df.columns = df.columns.str.lower()

    return df


# Transformasi DataFrame
df_final = preprocess_data(df) # ubah function menjadi dataframe df_final

# Menyimpan data yang telah diubah ke dalam file CSV
df_final.to_csv('P2G7_Andhika-Nafis_data_clean.csv', index=False) # simpan df kita menjadi csv data_clean

# Koneksi ke Elasticsearch
es = Elasticsearch("http://localhost:9200") # sambungan ke elasticsearch masing masing

df_final_gaksih=pd.read_csv('P2G7_Andhika-Nafis_data_clean.csv')
# Indeksasi data ke Elasticsearch
for i, r in df_final_gaksih.iterrows():
    doc = r.to_json()
    res = es.index(index="df_final_gaksih", body=doc)
    print(res)

