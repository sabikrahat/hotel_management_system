from django.db import models

# Create your models here.
class UserModel(models.Model):
    email = models.CharField(max_length=40)
    password = models.CharField(max_length=1024)
    name = models.CharField(max_length=40)
    phone = models.CharField(max_length=20)
    role = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'users_data'

    def isExists(self):
        if UserModel.objects.filter(email=self.email):
            return True
        return False


class CustomerModel(models.Model):
    name = models.CharField(max_length=40)
    email = models.CharField(max_length=40)
    phone = models.CharField(max_length=20)
    capacity = models.CharField(max_length=20)
    budget = models.CharField(max_length=20)
    manager = models.CharField(max_length=20)
    status = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'customers_data'