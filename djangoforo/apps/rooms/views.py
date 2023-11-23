from django.shortcuts import render

def room_chat(request):
    return render(request, 'rooms/room_chat.html')
