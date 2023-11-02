from rest_framework import views, generics, response, status
from .serializers import TravelSerializer, TownSerializer, UserSerializer
from .models import Town, Destination, Travel, TelegramUser
from user.models import Client, TaxiDriver
from .tasks import task_travel, task_message_delete


class UserCreateAPI(generics.CreateAPIView):
    queryset = TelegramUser.objects.all()
    serializer_class = UserSerializer


class DestinationAPI(views.APIView):
    def get(self, request, *args, **kwargs):
        qs = Destination.objects.filter(taxi_driver__telegram_id=self.request.query_params.get('telegram_id'))
        lst = list()
        for i in qs:
            lst.append({'where': i.where.name, 'to_where': i.to_where.name, 'id': i.id})
        return response.Response(lst)

    def post(self, request, *args, **kwargs):
        taxi_driver = TaxiDriver.objects.filter(telegram_id=self.request.data['telegram_id']).first()
        where = Town.objects.filter(name__exact=self.request.data['where']).first()
        to_where = Town.objects.filter(name__exact=self.request.data['to_where']).first()
        if Destination.objects.filter(where=where, taxi_driver=taxi_driver, to_where_id=to_where.id).first():
            return response.Response(status=status.HTTP_302_FOUND)
        else:
            Destination.objects.create(taxi_driver_id=taxi_driver.id, where_id=where.id, to_where_id=to_where.id)
            return response.Response(status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        Destination.objects.filter(id=self.request.query_params.get('id')).delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)


class TownAPI(generics.ListAPIView):
    queryset = Town.objects.all()
    serializer_class = TownSerializer

    def get_queryset(self):
        where = self.request.query_params.get('where')
        if where:
            lst = list()
            for i in Town.objects.all():
                if i != Town.objects.filter(name__exact=where).first():
                    lst.append(i)
        else:
            lst = Town.objects.all()
        return lst


class TravelAPI(views.APIView):
    def post(self, request, *args, **kwargs):
        client = Client.objects.filter(telegram_id=self.request.query_params.get('telegram_id')).first()
        data = dict()
        where = Town.objects.filter(name__exact=self.request.data['where']).first()
        to_where = Town.objects.filter(name__exact=self.request.data['to_where']).first()
        data['client'] = client.id
        data['where'] = where.id
        data['to_where'] = to_where.id
        data['lat'] = self.request.data['lat']
        data['lon'] = self.request.data['lon']
        data['count_person'] = self.request.data['count_person']
        data['note'] = self.request.data['note']
        serializer = TravelSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        t_id = serializer.data['id']
        qs = Destination.objects.filter(where_id=where.id, to_where_id=to_where.id)
        lst = [i.taxi_driver.telegram_id for i in qs]
        task_travel.delay(note=data['note'], name=client.name, where=where.name, to_where=to_where.name, lst=lst,
                          phone=client.phone, username=client.username, lat=data['lat'], lon=data['lon'], t_id=t_id,
                          count_person=data['count_person'])
        return response.Response({'id': t_id, 'count': qs.count()}, status=status.HTTP_201_CREATED)

    def patch(self, request, *args, **kwargs):
        obj = Travel.objects.filter(id=self.request.query_params.get('id')).first()
        obj.completed = True
        obj.save()
        task_message_delete.delay(t_id=obj.id)
        return response.Response()
