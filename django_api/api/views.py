import requests
from django.http import JsonResponse
from .models import LivePost
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def fetch_and_save_live_posts(request):
    # 1. Menarik data dari URL eksternal
    current_offset = LivePost.objects.count()
    limit = 10

    url = "https://jsonplaceholder.typicode.com/posts"
    params = {
        "_start": current_offset,
        "_limit": limit
    }

    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        saved_count = 0
        
        # 2. Looping data dan simpan ke database (dengan validasi anti-duplikat)
        for item in data:
            # update_or_create berfungsi mengecek: jika post_id sudah ada, abaikan/update. Jika belum, buat baru.
            obj, created = LivePost.objects.update_or_create(
                id=item['id'],
                defaults={
                    'user_id': item['userId'],
                    'title': item['title'],
                    'body': item['body']
                }
            )
            if created:
                saved_count += 1
                
        return JsonResponse({
            "status": "success",
            "message": f"Berhasil menarik dan menyimpan {saved_count} data baru ke database."
        })
    else:
        return JsonResponse({"status": "error", "message": "Gagal menghubungi JSONPlaceholder"}, status=400)