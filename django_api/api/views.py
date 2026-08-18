from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import ApiPost
from .serializers import ApiPostSerializer

@api_view(['GET'])
def get_posts(request):
    try:
        # Menarik data dari tabel transactionss di Postgres
        posts = ApiPost.objects.all().order_by('-id')
        serializer = ApiPostSerializer(posts, many=True)
        return Response({
            "status": "sukses",
            "total_data": len(serializer.data),
            "data": serializer.data
        })
    except Exception as e:
        return Response({"error": str(e)}, status=500)