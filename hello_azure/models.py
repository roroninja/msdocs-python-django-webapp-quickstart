from django.db import models

class FoundItem(models.Model):
    # 自動編碼的主鍵 ID
    id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=100, null=False)
    item_name = models.CharField(max_length=255, null=False)
    date_found = models.DateField(null=False)
    details = models.TextField(null=False)
    location = models.CharField(max_length=255, null=False)
    finder_email = models.EmailField(null=False)
    finder_password = models.CharField(max_length=128, null=False)
    image = models.ImageField(upload_to='found_items/', null=True, blank=True) 
    def __str__(self):
        return f"{self.item_name} - {self.category}"

