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


class BoardDetailView(generics.RetrieveAPIView):
    serializer_class = BoardSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Board.objects.filter(creator=user)

    def get(self, request, *args, **kwargs):
        board = self.get_object()

        # Check if the current user is the creator of the board
        if board.creator != request.user:
            return Response({'error': 'You do not have permission to access this board.'}, status=403)

        serializer = self.get_serializer(board)
        return Response(serializer.data)