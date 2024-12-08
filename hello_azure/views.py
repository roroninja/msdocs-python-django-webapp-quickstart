import json
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import render
from django.http import JsonResponse
from .models import FoundItem
from .forms import AddForm
from django.contrib.auth.hashers import make_password,check_password
from django.core.mail import send_mail
from django.template.loader import render_to_string
# Create your views here.

def index(request):
    found_items = FoundItem.objects.all().values('id','item_name', 'category', 'date_found', 'details', 'location','image')
    return render(request, 'index.html', {'found_items': found_items})



def add(request):
    if request.method == 'POST':
        form = AddForm(request.POST,request.FILES)
        if form.is_valid():

            hashed_password = make_password(form.cleaned_data['finder_pwd']) 
            found_item = FoundItem(
                item_name=form.cleaned_data['item_name'],
                category=form.cleaned_data['category'],
                date_found=form.cleaned_data['date'],
                details=form.cleaned_data['detail'],
                location=form.cleaned_data['location'],
                finder_email=form.cleaned_data['finder_email'],
                finder_password=hashed_password,  
                image=form.cleaned_data.get('image')
            )
            found_item.save()
            return JsonResponse({'message': 'Item successfully added!'}, status=200)
        else:
            return JsonResponse({'message': 'Invalid form data'}, status=400)
    else:
        form = AddForm()
    return render(request, 'index.html', {'form': form})

def edit_item(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        item_id = data.get('id')
        email = data.get('email')
        password = data.get('password')

        try:
            found_item = FoundItem.objects.get(id=item_id)
            if found_item.finder_email == email and check_password(password, found_item.finder_password):

                return JsonResponse({
                    'success': True,
                    'item': {
                        'item_name': found_item.item_name,
                        'category': found_item.category,
                        'date_found': found_item.date_found.strftime('%Y-%m-%d'),  
                        'details': found_item.details,
                        'location': found_item.location,
                    }
                })
            else:
                return JsonResponse({'success': False, 'message': 'Email or Password is incorrect'}, status=400)
        except FoundItem.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Item not found'}, status=404)

    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)

    
def update_item(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        item_id = data.get('id')
        
        try:
            found_item = FoundItem.objects.get(id=item_id)
            found_item.item_name = data.get('item_name')
            found_item.category = data.get('category')
            found_item.date_found = data.get('date_found')
            found_item.details = data.get('details')
            found_item.location = data.get('location')
            found_item.save()

            return JsonResponse({'success': True})
        except FoundItem.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Item not found'}, status=404)

    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)

def delete_item(request, item_id):
    if request.method == 'DELETE':
        try:
            found_item = FoundItem.objects.get(id=item_id)
            found_item.delete()
            return JsonResponse({'success': True})
        except FoundItem.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Item not found'}, status=404)

    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)

def send_claim_notification(finder_email, item_id, item_name, claim_email):
    subject =("Item Claim Notification")
    
    message_template =(
        """
        <p>親愛的 {finder_email} 您好，</p>
        <p>您所登記的物品 {item_id} - {item_name} 有人要招領，</p>
        <p>招領人為 {claim_email}，</p>
        <p>請盡速與該招領人聯絡。</p>
        <p>提醒您招領後進行刪除該物件。</p>
        <p>感謝您的合作。</p>
        <p>Best regards,<br>nptufinder</p>
        """
    )

    message_html = message_template.format(
        finder_email=finder_email,
        item_id=item_id,
        item_name=item_name,
        claim_email=claim_email,
    )

    sender = settings.EMAIL_HOST_USER
    recipients = [finder_email]  

    send_mail(
        subject,
        '',  
        sender,
        recipients,
        html_message=message_html  
    )

def claim_item(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        item_id = data.get('item_id')
        claim_email = data.get('email')
        
        try:
            found_item = FoundItem.objects.get(id=item_id)
            finder_email = found_item.finder_email
            item_name = found_item.item_name

            send_claim_notification(finder_email, item_id, item_name, claim_email)
            return JsonResponse({'success': True, 'message': 'Item claimed successfully!'})
        except FoundItem.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Item not found'}, status=404)
        
    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)

def filtered_items(request):
    category = request.GET.get('category')
    found_items = FoundItem.objects.filter(category=category) if category else FoundItem.objects.all()

    # 使用模板渲染過濾後的 found_items，僅生成 HTML 不產生新頁面
    html = render_to_string('index.html', {'found_items': found_items, 'only_items': True})
    return JsonResponse({'html': html})