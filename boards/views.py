from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Board, List, Card
from .serializers import BoardSerializer
from rest_framework.views import APIView

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
    



class UpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = request.data

        # Actualizar o Crear Boards
        for board_data in data.get('Board', []):
            board_id = board_data.get('id')
            new_name = board_data.get('name')
            delete_board = board_data.get('delete', False)
            create_board = board_data.get('create', False)

            if create_board:
                # Crear nuevo board
                new_board = Board(name=new_name, creator=request.user)
                new_board.save()

            if board_id and not create_board:
                try:
                    board = Board.objects.get(id=board_id, creator=request.user)

                    if delete_board:
                        # Eliminar board
                        board.delete()
                    elif new_name:
                        # Actualizar nombre del board
                        board.name = new_name
                        board.save()

                except Board.DoesNotExist:
                    return Response({'error': f'Board with id {board_id} not found for the user.'}, status=status.HTTP_404_NOT_FOUND)

        # Actualizar o Crear Listas y Cards
        for list_data in data.get('List', []):
            list_id = list_data.get('id')
            new_name = list_data.get('name')
            new_order = list_data.get('order')
            delete_list = list_data.get('delete', False)
            create_list = list_data.get('create', False)
            board_id = list_data.get('board_id')

            if create_list:
                # Crear nueva lista
                new_list = List(name=new_name, order=new_order, board=Board.objects.get(id=board_id), creator=request.user)
                new_list.save()

            if list_id and not create_list:
                try:
                    list = List.objects.get(id=list_id, board__creator=request.user)

                    if delete_list:
                        # Eliminar lista
                        list.delete()
                    elif new_name:
                        list.name = new_name
                    if new_order is not None:
                        list.order = new_order

                    list.save()

                except List.DoesNotExist:
                    return Response({'error': f'List with id {list_id} not found for the user.'}, status=status.HTTP_404_NOT_FOUND)

        for card_data in data.get('Card', []):
            card_id = card_data.get('id')
            new_title = card_data.get('title')
            new_description = card_data.get('description')
            new_order = card_data.get('order')
            new_list_id = card_data.get('list_id')
            delete_card = card_data.get('delete', False)
            create_card = card_data.get('create', False)

            if create_card:
                # Crear nueva tarjeta
                new_card = Card(title=new_title, description=new_description, list=List.objects.get(id=new_list_id), order=new_order, creator=request.user)
                new_card.save()

            if card_id and not create_card:
                try:
                    card = Card.objects.get(id=card_id, list__board__creator=request.user)

                    if delete_card:
                        # Eliminar tarjeta
                        card.delete()
                    elif new_title:
                        card.title = new_title
                    if new_description:
                        card.description = new_description
                    if new_order is not None:
                        card.order = new_order
                    if new_list_id is not None:
                        try:
                            new_list = List.objects.get(id=new_list_id, board__creator=request.user)
                            card.list = new_list
                        except List.DoesNotExist:
                            return Response({'error': f'List with id {new_list_id} not found for the user.'}, status=status.HTTP_404_NOT_FOUND)

                    card.save()

                except Card.DoesNotExist:
                    return Response({'error': f'Card with id {card_id} not found for the user.'}, status=status.HTTP_404_NOT_FOUND)

        return Response({'message': 'Updates successful.'}, status=status.HTTP_200_OK)