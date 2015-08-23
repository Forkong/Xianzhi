from django.db import models

class Good(models.Model):
    uid = models.ForeignKey('User', db_column='uid', blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    tag = models.IntegerField(blank=True, null=True)
    size = models.CharField(max_length=255, blank=True, null=True)
    material = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    is_available = models.IntegerField(blank=True, null=True)
    create_date = models.DateTimeField(blank=True, null=True)
    photo_path = models.CharField(max_length=255, blank=True, null=True)
    photo_name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'good'

class User(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    passwd = models.CharField(max_length=255, blank=True, null=True)
    create_date = models.DateTimeField(blank=True, null=True)
    is_available = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user'
