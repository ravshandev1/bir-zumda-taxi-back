from rest_framework import views, response, generics, status
from .serializers import ClientSerializer, TaxiDriverSerializer
from .models import Client, TaxiDriver


class TaxiAPI(generics.CreateAPIView):
    queryset = TaxiDriver.objects.all()
    serializer_class = TaxiDriverSerializer

    def post(self, request, *args, **kwargs):
        user = TaxiDriver.objects.filter(telegram_id=self.request.query_params.get('id')).first()
        if user:
            serializer = TaxiDriverSerializer(instance=user, data=self.request.data, partial=True)
        else:
            serializer = TaxiDriverSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response()

    def get(self, request, *args, **kwargs):
        user = TaxiDriver.objects.filter(telegram_id=self.request.query_params.get('id')).first()
        serializer = TaxiDriverSerializer(user)
        return response.Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        TaxiDriver.objects.filter(telegram_id=self.request.query_params.get('id')).delete()
        Client.objects.filter(telegram_id=self.request.query_params.get('id')).delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)


class ClientAPI(generics.CreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    def post(self, request, *args, **kwargs):
        user = Client.objects.filter(telegram_id=self.request.query_params.get('id')).first()
        if user:
            serializer = ClientSerializer(instance=user, data=self.request.data, partial=True)
        else:
            serializer = ClientSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response()

    def get(self, request, *args, **kwargs):
        user = Client.objects.filter(telegram_id=self.request.query_params.get('id')).first()
        serializer = ClientSerializer(user)
        return response.Response(serializer.data)


class UserAPI(views.APIView):
    def get(self, request, *args, **kwargs):
        if Client.objects.filter(telegram_id=self.kwargs.get('pk')).first():
            return response.Response(status=status.HTTP_201_CREATED)
        elif TaxiDriver.objects.filter(telegram_id=self.kwargs.get('pk')).first():
            return response.Response(status=status.HTTP_202_ACCEPTED)
        else:
            return response.Response(status=status.HTTP_404_NOT_FOUND)
