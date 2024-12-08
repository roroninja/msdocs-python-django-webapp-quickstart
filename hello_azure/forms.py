from django import forms

class AddForm(forms.Form):
    item_name = forms.CharField(label='物品名稱', max_length=255, required=True)
    CATEGORY_CHOICES = [
        ('electronics', '電子產品'),
        ('personal', '個人用品'),
        ('clothing', '衣物'),
        ('card','卡片'),
        ('other', '其他'),
    ]
    category = forms.ChoiceField(label='類別', choices=CATEGORY_CHOICES, required=True)
 
    date = forms.DateField(label='拾獲日期', widget=forms.SelectDateWidget(), required=True)

    detail = forms.CharField(label='細節', widget=forms.Textarea, max_length=500, required=True)

    location = forms.CharField(label='拾獲地點', max_length=255, required=True)

    finder_email = forms.EmailField(label='拾獲人電子郵件', required=True)

    finder_pwd = forms.CharField(label='拾獲人密碼', widget=forms.PasswordInput, max_length=128, required=True)

    image = forms.ImageField(label='上傳圖片', required=False) 
