import socket

def get_local_ip():
    # Membuat koneksi socket UDP
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Mencoba terhubung ke IP sembarang (tidak akan mengirim data apa pun)
        s.connect(('10.255.255.255', 1))
        # Mengambil alamat IP yang digunakan oleh koneksi tersebut
        ip_address = s.getsockname()[0]
    except Exception:
        ip_address = '127.0.0.1'
    finally:
        s.close()
    return ip_address

if __name__ == "__main__":
    ip_lokal = get_local_ip()
    print("="*50)
    print(f"🌐 IP Address Lokal Anda : {ip_lokal}")
    print("="*50)
    print(f"Berikan URL ini ke teman Anda untuk dites di Postman:\nhttp://{ip_lokal}:8000/api/transactions_seeder/")
    print("="*50)