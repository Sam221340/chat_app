from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from .models import Group
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import JsonResponse
from Chat_app import settings
from django.core.mail import send_mail
from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import json
def home(request):
    u_id = request.user.id
    groups = Group.objects.filter(members = u_id)
    return render(request, 'chat_home.html', {'groups': groups})

@login_required
def new_group(request):
    u = request.user
    new = Group.objects.create(created_by= u)
    new.members.add(u)
    new.save()
    return redirect('chat_home')

@login_required
def join_group_with_uuid(request, uuid):
    u = request.user
    gp = Group.objects.get(uuid=uuid)
    gp.members.add(u)
    gp.save()
    return redirect('chat_home')


@login_required
def leave_group(request, uuid):
    u = request.user
    gp = Group.objects.get(uuid= uuid)
    gp.members.remove(u)
    gp.save()
    return redirect('chat_home')

@login_required
def open_chat(request, uuid):
    group = Group.objects.get(uuid= uuid)
    users = User.objects.all()
    if request.user not in group.members.all():
        return HttpResponseForbidden('Not a member, Try again')
    messages = group.message_set.all()
    sorted_messages = sorted(messages, key = lambda x: x.timestamp)
    return render(request, 'chat.html', context={'messages': sorted_messages, 'uuid':uuid, 'users':users})

@login_required
def remove_group(request, uuid):
	u = request.user
	Group.objects.get(uuid=uuid).delete()
	return redirect('chat_home')







import ssl
from django.core.mail import EmailMultiAlternatives

@login_required
@csrf_exempt
def join_group(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        group_uuid = data.get('group_uuid')
        user_email = data.get('user_email')
        
        # Send join request email
        subject = "You have been invited to join my chat group"
        from_email = settings.EMAIL_HOST_USER
        to_email = [user_email]
        
        # Construct the join link
        join_link = f"http://{request.get_host()}/chat_room/join_group/{group_uuid}"
        
        # Render email template
        html_message = render_to_string('invitation_email.html', {'join_link': join_link})
        plain_message = strip_tags(html_message)
        
        # Send email without specifying SSL context
        send_mail(subject, plain_message, from_email, to_email, html_message=html_message)
        
        return JsonResponse({'message': 'Join request processed successfully'})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
