from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import Board
from .serializers import BoardSerializer

class ListBoardsView(generics.ListAPIView):
    serializer_class = BoardSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Board.objects.filter(creator=user)
