import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
from tabulate import tabulate

# ==============================
# Koneksi ke Database
# ==============================
def create_connection():
    conn = mysql.connector.connect(
        host="localhost",      
        user="root",           
        password="Ruffymysql",  
        database="rumah_sakit"
    )
    return conn

# ==============================
# 1. Read Table
# ==============================
def read_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pasien;")
    rows = cursor.fetchall()
    col_names = [desc[0] for desc in cursor.description]
    print(tabulate(rows, headers=col_names, tablefmt="psql"))
    cursor.close()
    conn.close()

# ==============================
# 2. Show Statistik
# ==============================
def show_statistics(column_name):
    conn = create_connection()
    query = f"SELECT {column_name} FROM pasien;"
    df = pd.read_sql(query, conn)
    if df.empty:
        print("Data tidak tersedia")
    else:
        print(df.describe())
    conn.close()

# ==============================
# 3. Data Visualization
# ==============================
def visualize_column(column_name):
    conn = create_connection()
    query = f"SELECT {column_name} FROM pasien;"
    df = pd.read_sql(query, conn)

    if df[column_name].dtype == 'object':  # categorical
        df[column_name].value_counts().plot(kind="bar")
        plt.title(f"Distribusi {column_name}")
        plt.xlabel(column_name)
        plt.ylabel("Count")
        plt.show()
    else:  # numerical
        df[column_name].plot(kind="hist", bins=10, rwidth=0.8)
        plt.title(f"Histogram {column_name}")
        plt.xlabel(column_name)
        plt.ylabel("Frequency")
        plt.show()

    conn.close()

# ==============================
# 4. Add Data
# ==============================
def add_data(id_pasien, nama, usia, jenis_kelamin, diagnosis, tanggal_masuk):
    conn = create_connection()
    cursor = conn.cursor()
    query = """
    INSERT INTO pasien (id_pasien, nama, usia, jenis_kelamin, diagnosis, tanggal_masuk)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    values = (id_pasien, nama, usia, jenis_kelamin, diagnosis, tanggal_masuk)
    try:
        cursor.execute(query, values)
        conn.commit()
        print("✅ Data berhasil ditambahkan")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    cursor.close()
    conn.close()

# ==============================
# 5. Import Dataset Excel
# ==============================
def import_dataset(file_path):
    df = pd.read_excel(file_path)
    conn = create_connection()
    cursor = conn.cursor()

    for _, row in df.iterrows():
        query = """
        INSERT INTO pasien (id_pasien, nama, usia, jenis_kelamin, diagnosis, tanggal_masuk)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            nama=VALUES(nama),
            usia=VALUES(usia),
            jenis_kelamin=VALUES(jenis_kelamin),
            diagnosis=VALUES(diagnosis),
            tanggal_masuk=VALUES(tanggal_masuk);
        """
        values = (
            int(row["id_pasien"]),
            row["nama"],
            int(row["usia"]),
            row["jenis_kelamin"],
            row["diagnosis"],
            row["tanggal_masuk"].date()
        )
        cursor.execute(query, values)

    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Import dataset selesai")

# ==============================
# Menu Utama
# ==============================
def main():
    while True:
        print("\n=== Capstone Project Rumah Sakit ===")
        print("1. Read Table")
        print("2. Show Statistik")
        print("3. Data Visualization")
        print("4. Add Data")
        print("5. Keluar")
        print("6. Import Dataset Excel")

        choice = input("Pilih menu: ")

        if choice == "1":
            read_table()
        elif choice == "2":
            col = input("Masukkan nama kolom (contoh: usia): ")
            show_statistics(col)
        elif choice == "3":
            col = input("Masukkan nama kolom untuk visualisasi: ")
            visualize_column(col)
        elif choice == "4":
            id_pasien = int(input("ID Pasien: "))
            nama = input("Nama: ")
            usia = int(input("Usia: "))
            jenis_kelamin = input("Jenis Kelamin (Laki-laki/Perempuan): ")
            diagnosis = input("Diagnosis: ")
            tanggal_masuk = input("Tanggal Masuk (YYYY-MM-DD): ")
            add_data(id_pasien, nama, usia, jenis_kelamin, diagnosis, tanggal_masuk)
        elif choice == "5":
            print("Keluar dari program...")
            break
        elif choice == "6":
            file_path = input("Masukkan path file Excel (contoh: dataset_pasien.xlsx): ")
            import_dataset(file_path)
        else:
            print("Pilihan tidak valid, coba lagi.")

if __name__ == "__main__":
    main()
