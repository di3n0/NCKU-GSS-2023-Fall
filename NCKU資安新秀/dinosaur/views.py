
from .models import Order
from dateutil import parser
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.contrib.auth import authenticate, login, logout
from .models import ConfeRoom, Order, check
from django.contrib import messages
from .forms import Logi_form, Register_form, AddForm
from .forms import EventForm
from django.utils import timezone
import pytz
from django.contrib.auth.models import User

#偵測POST
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
import datetime
from datetime import timedelta

#API
from rest_framework import viewsets
from rest_framework import permissions
from dinosaur.serializers import GroupSerializer


#CSP
from csp.decorators import csp_update


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = check.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]
    




#顯示可用的會議室
@csp_update(script_src="'self'", style_src="'self'")
def list(request):
    rooms = ConfeRoom.objects.all()
    for room in rooms:
        orders = Order.objects.filter(room=room, checkdig="使用中")
        if orders.exists():
            for order in orders:
                # 确认 order.checkdig 是否等于 1
                if order.checkdig == "使用中":
                    current_time = datetime.datetime.now(timezone.utc)
                    #current_time_adjusted = str(current_time)
                    #print(current_time_adjusted)
                    #print(type(current_time_adjusted))
                    new_format = '%Y-%m-%d %H:%M:%S%z'
                    current_time_adjusted = datetime.datetime.strftime(current_time,new_format)
                    
                    current_time_str =datetime.datetime.strptime(current_time_adjusted, "%Y-%m-%d %H:%M:%S%z")
                    #print(type(current_time_str))
                    #time_delta = timedelta(hours=8)
                    #current_time_str -= time_delta
                    print(current_time_str)
                    #print(type(current_time_str))
                    if order.end_time < current_time_str:
                        order.checkdig = "簽退"
                        order.save()
            for order in orders:
                # 确认 order.checkdig 是否等于 1
                if order.checkdig == "使用中":
                    # 将 ConfeRoom 中的 room_status 状态改为 0
                    room.room_status = '❌'
                    room.save()
        else:
            room.room_status = '✔️'
            room.save()

    content = {
        'room': rooms
    }
    return render(request, 'list.html', content)

#某個會議室預約詳情
@csp_update(script_src="'self'", style_src="'self'")
def appointment(request, id):
    room = get_object_or_404(ConfeRoom, id=id)
    d = datetime.date.today()
    order = Order.objects.filter(room=room, start_time__gte=d).order_by('start_time')
    content = {
        'order': order,
        'room': room
    }
    return render(request, 'order.html', content)

@csp_update(script_src="'self'", style_src="'self'")
def logi(request):
    form = Logi_form()
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        u = authenticate(username=username, password=password)
        if u and u.is_active:
            login(request, u)
            # 设置cookie
            response = redirect('dinosaur:list')
            response.set_cookie('cross-site-cookie', 'name', samesite='Strict', secure=True, httponly=True)
            return response

    content = {
        'form': form
    }
    return render(request, 'logi.html', content)

@csp_update(script_src="'self'", style_src="'self'")
def logo(request):
    if request.user.is_active:
        logout(request)
        return redirect('dinosaur:list')

# def register(request):
#     form = Register_form(request.POST)
#     if form.is_valid():
#         user = form.save(commit=False)
#         username = form.cleaned_data["username"]
#         password = form.cleaned_data["password"]
#         user.username = username
#         user.set_password(password)
#         user.save()
#         user = authenticate(username=username, password=password)
#         if user.is_active:
#             login(request, user)
#             return redirect('dinosaur:list')
#     content = {
#         'form': form
#     }
#     return render(request, 'logi.html', content)

@csp_update(script_src="'self'", style_src="'self'")
def register(request):
    if request.method == 'POST':
        form = Register_form(request.POST)
        if form.is_valid():
            user = form.save()  # 使用 form.save() 來處理用戶創建
            login(request, user)
            # 设置cookie
            response = redirect('dinosaur:list')
            response.set_cookie('cross-site-cookie', 'name', samesite='Strict', secure=True, httponly=True)
            return response

    else:
        form = Register_form()

    content = {
        'form': form
    }
    return render(request, 'logi.html', content)



# Your existing imports

@csp_update(script_src="'self'", style_src="'self'")
def add(request, id):
    if not request.user.is_active:
        return redirect('dinosaur:register')

    room = ConfeRoom.objects.get(id=id)
    room.timezone = 'Asia/Taipei'

    if request.method == "POST":
        form = AddForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.room = room 

            start_time_str = request.POST.get('start_time')
            end_time_str = request.POST.get('end_time')

            if not start_time_str or not end_time_str:
                messages.error(request, '請輸入有效的開始時間和結束時間')
                return redirect('/%s' % id)

            try:
                room_timezone = pytz.timezone(room.timezone)
                
                start_time = timezone.make_aware(parser.parse(start_time_str), timezone=room_timezone) 
                end_time = timezone.make_aware(parser.parse(end_time_str), timezone=room_timezone)  

                current_time = timezone.now()
                current_time = current_time.astimezone(room_timezone)

                # Check for overlapping orders
                conflicting_orders = Order.objects.filter(
                    room=room, start_time__lt=end_time, end_time__gt=start_time
                )

                if conflicting_orders.exists():
                    conflicting_orders=conflicting_orders.first()
                    if conflicting_orders.checkdig == "簽退":
                        instance.start_time = start_time
                        instance.end_time = end_time
                        instance.save()
                        return redirect('/%s' % id)
                    else:
                        messages.error(request, '該時間段已被預約')
                        return redirect('/%s' % id)

                if start_time > current_time:
                    if end_time > start_time: 
                        instance.start_time = start_time
                        instance.end_time = end_time
                        instance.save()
                        return redirect('/%s' % id)
                    else:
                        messages.error(request, '結束時間不能比開始時間早')
                        return redirect('/%s' % id)
                else:
                    messages.error(request, '超出預約範圍')
                    return redirect('/%s' % id)
            except ValueError:
                messages.error(request, '無效的日期時間格式')
                return redirect('/%s' % id)
    else:
        form = AddForm()

    context = {
        "form": form,
    }
    return render(request, 'logi.html', context)




@csp_update(script_src="'self'", style_src="'self'")
def delete(request, room_id, order_id):
    order = get_object_or_404(Order,id=order_id)
    if order.user != request.user:
        raise Http404
    order.delete()
    messages.success(request,'刪除成功！')
    return redirect('/%s' % room_id)


@csp_update(script_src="'self'", style_src="'self'")
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('calendar') 
    else:
        form = EventForm()
    
    return render(request, 'create_event.html', {'form': form})




from django.http import HttpResponseBadRequest

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def update_checkdig(request):
    if request.method == 'POST':
        try:
            data = request.data
            cardid = data.get('cardid')
            room_id = data.get('room')
            time_check = data.get('check_time')


            try:
                room_id = str(room_id)
            except ValueError:
                return HttpResponseBadRequest("無效的房間ID")
            
            try:
                room_id = int(room_id)
            except ValueError:
                return HttpResponseBadRequest("無效的房間ID")

            try:
                time_check = datetime.datetime.strptime(time_check, "%Y-%m-%d %H:%M:%S%z")
            except ValueError:
                return HttpResponseBadRequest("無效的時間格式")


            if not cardid or not room_id or not time_check:
                return HttpResponseBadRequest("輸入錯誤")


            # time_check = datetime.datetime.strptime(time_check, "%Y-%m-%d %H:%M:%S%z")
            time_delta = timedelta(hours=8)
            time_check -= time_delta

            orders = Order.objects.filter(cardid=cardid, room=room_id, start_time__lte=time_check, end_time__gte=time_check)

            
            if orders.exists():
                order = orders.first()
                if order.checkdig == '未到':
                    Order.objects.filter(cardid=order.cardid,room = order.room, checkdig='未到').update(checkdig='使用中')
                    return Response({'message': 'Checking successfully.'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Order not found or time criteria not met.'}, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f'Something went wrong: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)







# @api_view(['POST'])
# @permission_classes([permissions.IsAuthenticated])
# def update_isempty(request):
#     if request.method == 'POST':
#         try:
#             data = request.data
#             room_id = data.get('room')
#             time_check = data.get('check_time')

#             if not room_id or not time_check:
#                 return HttpResponseBadRequest("輸入錯誤")
        
#             time_check = datetime.datetime.strptime(time_check, "%Y-%m-%d %H:%M:%S%z")
#             time_delta = timedelta(hours=8)
#             time_check -= time_delta

#             orders = Order.objects.filter(room=room_id, start_time__lte=time_check, end_time__gte=time_check)

#             if orders.exists():
#                 order = orders.first()
#                 Order.objects.filter(room = order.room, checkdig='使用中').update(checkdig='簽退')
#                 return Response({'message': 'Emptying successfully.'}, status=status.HTTP_200_OK)
#             else:
#                 return Response({'error': 'Order not found or time criteria not met.'}, status=status.HTTP_404_NOT_FOUND)
#         except ValidationError as e:
#             return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
#         except Exception as e:
#             return Response({'error': f'Something went wrong: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
from django.core.exceptions import ValidationError

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def update_isempty(request):
    if request.method == 'POST':
        try:
            data = request.data
            room_id = data.get('room')
            time_check = data.get('check_time')

            try:
                room_id = int(room_id)
            except ValueError:
                return HttpResponseBadRequest("無效的房間ID")

            try:
                time_check = datetime.datetime.strptime(time_check, "%Y-%m-%d %H:%M:%S%z")
            except ValueError:
                return HttpResponseBadRequest("無效的時間格式")

            if not room_id or not time_check:
                return HttpResponseBadRequest("輸入錯誤")
        
            time_check -= timedelta(hours=8)

            orders = Order.objects.filter(room=room_id, start_time__lte=time_check, end_time__gte=time_check)

            if orders.exists():
                order = orders.first()
                Order.objects.filter(room=order.room, checkdig='使用中').update(checkdig='簽退')
                return Response({'message': 'Emptying successfully.'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Order not found or time criteria not met.'}, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f'Something went wrong: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
