from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from pytz import timezone as pytz_timezone
#from django.contrib.auth import authenticate, login, logout
from django.db.models import F
#from django.db import ConfeRoom
#from django.db import Confe rooms
#rom django.db import Orders

#會議室
class ConfeRoom(models.Model):
    num = models.CharField(max_length=5)
    size = models.CharField(max_length=5)
    open_time = models.DateTimeField(default=timezone.now) 
    close_time = models.DateTimeField(default=timezone.now)
    timezone = models.CharField(max_length=50, default='Your_Default_Timezone')
    room_status = models.CharField(max_length=2, default='✔️')

    class Meta:  # 正确的 Meta 类定义
        ordering = ["num"]
    
    def __str__(self):
        return self.num


#訂單資料
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #user = models.CharField(max_length=10, )
    room = models.ForeignKey(ConfeRoom, on_delete=models.CASCADE)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    checkdig =  models.CharField(max_length=4,default='未到' )
    cardid = models.CharField(max_length=20,default='' )


    def save(self, *args, **kwargs):
        # 如果 cardid 為空，則將其設為關聯User的first_name 值
        if not self.cardid:
            self.cardid = self.user.first_name
        super().save(*args, **kwargs)
    
    def __str__(self):
        return str(self.user)
    



class check(models.Model):
    #user = models.ForeignKey(User, on_delete=models.CASCADE)
    cardid = models.CharField(max_length=20,default='123456789' )
    room = models.ForeignKey(ConfeRoom, on_delete=models.CASCADE)
    check_time = models.DateTimeField(null=True, blank=True)


    def __str__(self):
        return str(self.cardid)

# def to_check(**kwargs):
#     cardid = int(kwargs.get('cardid'))
#     room= int(kwargs.get('room'))
#     check_time= int(kwargs.get('check_time'))
#     for u in User:
#         if u.first_name == cardid:
#             try:
#                 with transaction.atomic():
#                     item = Item.objects.select_for_update().get(id=1)
#                     item.stock = item.stock + 1
#                     item.save()
#                     time.sleep(delay)
#             except Exception as e:
#                 Exception('Unexpected error: {}'.format(e))



     


class Event(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateField()
    description = models.TextField()

    def __str__(self):
        return self.title
