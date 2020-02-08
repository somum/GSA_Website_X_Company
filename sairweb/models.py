from django.db import models
from django.utils import timezone

# Create your models here.

class destination(models.Model):
    dest_id=models.AutoField
    dest_name=models.CharField(max_length=50,default="")
    dest_created_date = models.DateTimeField(default=timezone.now)
    dest_desc = models.CharField(max_length=2000, default="")
    dest_img=models.ImageField(upload_to="sairweb/images/destination_img",default="")
    def __str__(self):
        return self.dest_name


class package(models.Model):
    pkg_id=models.AutoField
    pkg_name=models.CharField(max_length=50,default="")
    pkg_dest_name=models.CharField(max_length=50,default="")
    pkg_rating=models.CharField(max_length=50,default="")
    pkg_price=models.CharField(max_length=50,default="")
    pkg_created_date = models.DateTimeField(default=timezone.now)
    pkg_desc=models.CharField(max_length=2000,default="")
    pkg_img=models.ImageField(upload_to="sairweb/images/pkg_img",default="")
    def __str__(self):
        return self.pkg_name

class wadmin(models.Model):
    user_id=models.AutoField(primary_key=True)
    username=models.CharField(max_length=50,default="")
    password=models.CharField(max_length=50,default="")
    email=models.CharField(max_length=50,default="")
    type=models.CharField(max_length=50,default="")

    def __str__(self):
        return self.username


class visaInfo(models.Model):
    visa_id=models.AutoField(primary_key=True)
    #ref_no=models.AutoField(primary_key=True)
    fname=models.CharField(max_length=50,default="")
    passport_no=models.CharField(max_length=50,default="")
    dob=models.DateTimeField(default=timezone.now)
    visa_type=models.CharField(max_length=50,default="")
    vCountry=models.CharField(max_length=50,default="")
    contactNo=models.CharField(max_length=50,default="")
    visa_status=models.CharField(max_length=50,default="")
    #visa_img = models.ImageField(upload_to="sairweb/images/visa_img", default="")

    def __str__(self):
        #return self.fname
        return str(self.visa_id)

class visaInfoFile(models.Model):
    visa_img = models.FileField(upload_to="sairweb/images/visa_img", default="")
    visaInfo = models.ForeignKey(visaInfo, on_delete=models.CASCADE)

