# Cheat Sheet: PostgreSQL + Docker — Project SNJ

Referensi cepat perintah yang dipakai sehari-hari untuk project data warehouse ini.
Semua perintah `docker compose` dijalankan dari folder `dwh_project` (tempat `docker-compose.yml` berada).

---

## 1. Mengelola Container (Docker Compose)

| Perintah | Fungsi |
|---|---|
| `docker compose up -d` | Menghidupkan semua service (PostgreSQL, pgAdmin). `-d` = jalan di background |
| `docker compose stop` | Mematikan container, **data tetap tersimpan** |
| `docker compose start` | Menghidupkan lagi container yang sudah di-stop |
| `docker compose restart` | Mematikan lalu menghidupkan ulang (kalau ada perubahan config kecil) |
| `docker compose down` | Menghapus container & network, **data tetap tersimpan** di volume |
| `docker compose down -v` | Menghapus container & **volume/data sekaligus** — hati-hati, data hilang permanen |
| `docker ps` | Lihat container mana saja yang sedang jalan, beserta status & port |
| `docker ps -a` | Lihat SEMUA container termasuk yang sudah berhenti |
| `docker logs snj-dwh-postgres` | Lihat log/pesan error dari container PostgreSQL |
| `docker logs -f snj-dwh-postgres` | Lihat log secara live/real-time (`-f` = follow) |

---

## 2. Masuk & Keluar dari Database

| Perintah | Fungsi |
|---|---|
| `docker exec -it snj-dwh-postgres psql -U snj_admin -d snj_data_warehouse` | Masuk ke dalam database lewat `psql` |
| `\q` | Keluar dari `psql`, kembali ke terminal biasa |
| `\c nama_database` | Pindah/connect ke database lain (di dalam `psql`) |
| `\du` | Lihat daftar user/role yang ada |

---

## 3. Menjalankan File SQL (Load Schema, dll)

| Perintah | Fungsi |
|---|---|
| `docker exec -i snj-dwh-postgres psql -U snj_admin -d snj_data_warehouse < schema.sql` | Jalankan seluruh isi file `.sql` ke database (dari terminal biasa, di luar `psql`) |
| `docker exec -it snj-dwh-postgres pg_dump -U snj_admin snj_data_warehouse > backup.sql` | Backup seluruh database ke file `.sql` |

---

## 4. Melihat Struktur Database (dalam `psql`)

| Perintah | Fungsi |
|---|---|
| `\l` | Lihat daftar semua database |
| `\dt` | Lihat daftar tabel di database aktif |
| `\dt nama_schema.*` | Lihat tabel di schema tertentu, misal `\dt staging.*` atau `\dt warehouse.*` |
| `\d nama_tabel` | Lihat struktur/kolom dari satu tabel (nama kolom, tipe data, index) |
| `\dn` | Lihat daftar schema (misal: `staging`, `warehouse`) |
| `\dv` | Lihat daftar view |
| `\dx` | Lihat extension yang terpasang |

---

## 5. Query Dasar (SQL Standar, Sama di Manapun)

```sql
-- Lihat semua data di suatu tabel
SELECT * FROM warehouse.dim_vendor;

-- Lihat data dengan filter
SELECT * FROM warehouse.fact_vendor_transaksi WHERE tanggal = '2026-08-01';

-- Hitung jumlah baris
SELECT COUNT(*) FROM warehouse.fact_vendor_transaksi;

-- Tambah data manual (untuk testing)
INSERT INTO warehouse.dim_vendor (vendor_code, vendor_name)
VALUES ('VDR001', 'PT Contoh Sejahtera');

-- Update data
UPDATE warehouse.dim_vendor
SET vendor_name = 'PT Contoh Sejahtera Abadi'
WHERE vendor_code = 'VDR001';

-- Hapus data
DELETE FROM warehouse.dim_vendor WHERE vendor_code = 'VDR001';

-- Join antar tabel (fact + dimension)
SELECT f.tanggal, v.vendor_name, f.nilai
FROM warehouse.fact_vendor_transaksi f
JOIN warehouse.dim_vendor v ON f.vendor_id = v.vendor_id
LIMIT 10;
```

---

## 6. Cek Performa Query (Optimasi)

```sql
-- Lihat rencana eksekusi query (cek apakah pakai index atau full scan)
EXPLAIN ANALYZE SELECT * FROM warehouse.fact_vendor_transaksi WHERE tanggal = '2026-08-01';

-- Update statistik tabel supaya query planner akurat
ANALYZE warehouse.fact_vendor_transaksi;

-- Refresh materialized view
REFRESH MATERIALIZED VIEW warehouse.mv_summary_bulanan;
```

---

## 7. Alur Kerja Harian yang Umum Dipakai

```bash
# Pagi hari / mulai kerja
docker compose up -d
docker ps                    # pastikan status "Up"

# Masuk untuk cek/query data
docker exec -it snj-dwh-postgres psql -U snj_admin -d snj_data_warehouse

# ...kerja di dalam psql...
\q                            # keluar setelah selesai

# Selesai kerja / mau tutup laptop
docker compose stop           # data aman tersimpan, container berhenti
```

---

## Catatan Penting

- **`docker compose down -v`** menghapus data PERMANEN — jangan dipakai sembarangan setelah ada data penting tersimpan. Gunakan `docker compose stop` untuk mematikan sementara.
- Sebelum keluar dari `psql`, pastikan sudah selesai mengetik query (tidak sedang di tengah statement yang belum ada `;`-nya).
- Nama container (`snj-dwh-postgres`) dipakai untuk perintah `docker exec`/`docker logs`. Nama service (`postgres`) dipakai kalau container lain (misal pgAdmin/Airflow) perlu connect ke database ini.
