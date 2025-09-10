# membuat database
CREATE DATABASE IF NOT EXISTS rumah_sakit;
USE rumah_sakit;

# membuat tabel pasien
DROP TABLE IF EXISTS pasien;
CREATE TABLE pasien (
    id_pasien INT PRIMARY KEY,
    nama VARCHAR(100) NOT NULL,
    usia INT NOT NULL,
    jenis_kelamin VARCHAR(20) NOT NULL,
    diagnosis VARCHAR(100) NOT NULL,
    tanggal_masuk DATE NOT NULL
);
