from django.db import models

class res_admin_detail(models.Model):
    id  = models.AutoField(primary_key=True,default="")
    name = models.CharField(max_length=45, unique=True,default="")
    email=  models.CharField(max_length=45, unique=True,default="")
    password= models.CharField(max_length=45,default="")
    
    class  Meta:
        db_table="res_admin_detail"
    
# Create your models here.
class res_customer_detail(models.Model):
    id = models.AutoField(primary_key=True,default="")
    fname= models.CharField(max_length=45,default="")
    lname= models.CharField(max_length=45,default="")
    mail= models.CharField(max_length=45,default="")
    pwd= models.CharField(max_length=45,default="")
    
    class  Meta:
        db_table="res_customer_detail"


class ProjectDetail(models.Model):
    id  = models.AutoField(primary_key=True,default="")
    url = models.URLField()
    pname = models.CharField(max_length=255)
    status = models.CharField(max_length=50)
    user = models.ForeignKey(res_customer_detail, on_delete=models.CASCADE)

    def __str__(self):
        return self.pname

class CrawledData(models.Model):
    project = models.ForeignKey(ProjectDetail, on_delete=models.CASCADE)
    url = models.URLField()

    def __str__(self):
        return self.url

class MetaInformation(models.Model):
    crawled_data = models.OneToOneField(CrawledData, on_delete=models.CASCADE)
    meta_tag_count = models.IntegerField()

    def __str__(self):
        return f"Meta Information for {self.crawled_data}"

class PageQuality(models.Model):
    crawled_data = models.OneToOneField(CrawledData, on_delete=models.CASCADE)
    pages_with_image = models.IntegerField()

    def __str__(self):
        return f"Page Quality for {self.crawled_data}"

# Add other tables for PageStructure, LinkStructure, ServerInfo, and ExternalFactors similarly
