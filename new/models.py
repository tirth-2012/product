from django.db import models

# Create your models here.
   
class category(models.Model):
    name=models.CharField(max_length=200)
    detail=models.CharField(max_length=500)
    slug = models.SlugField(unique=True)  # For URLs
    has_subcategories = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name

class SubCategory(models.Model):
    category = models.ForeignKey(category, related_name='subcategories', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name
    
    
class Product(models.Model):
    name=models.CharField(max_length=200)
    price=models.DecimalField(max_digits=50,decimal_places=2)
    detail=models.CharField(max_length=300)
    category = models.ForeignKey(category, on_delete=models.CASCADE, related_name='product')
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, null=True, blank=True)
    image=models.ImageField(upload_to='product_image')
    
    def __str__(self):
        return self.name
    
