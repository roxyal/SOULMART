from django.db import models

from django.urls import reverse
# Create your models here.

class Category(models.Model):
    # db_index = True -> implies that query acceleration
    # instead of reading the entire, once found it return the result
    name = models.CharField(max_length=250, db_index=True)

    # A slug is a URL-friendly version of a string, typically used for creating
    # human-readable and search engine-friendly URLs. It is often derived from a title
    # or a descriptive text and contains only alphanumeric characters, hyphens, or underscores.
    # example; www.nike.com/shoe/nike-air-jordan
    slug = models.SlugField(max_length=250, unique=True)


    class Meta:
        # In Django, it automatically add a s after Category, we dont want it to happen
        # so kind of change the name
        verbose_name_plural = 'categories'
 
    # Category (1), Category (2), Category (3)
    def __str__(self):

        return self.name
    
    # Create a dynamic custom urls -> with respect to the slug name
    def get_absolute_url(self):

        return reverse('list-category', args=[self.slug])
    
class Product(models.Model):

    # We need a foreign key, such that it has a relationship with Category
    # on_delete=models.CASCADE means tht if a certain Category is deleted, that product associate under
    # will also be deleted
    category = models.ForeignKey(Category, related_name='product', on_delete=models.CASCADE, null=True)

    title = models.CharField(max_length=250)

    brand = models.CharField(max_length=250, default='un-branded')

    # blank = True -> implies that optional (dont really need to put)
    description = models.TextField(blank=True)

    slug = models.SlugField(max_length=250) # Unique Products

    price = models.DecimalField(max_digits=4, decimal_places=2)

    # upload to images folder, where images is under 'media/images'
    image = models.ImageField(upload_to='images/')

    class Meta:
        # In Django, it automatically add a s after Category, we dont want it to happen
        # so kind of change the name
        verbose_name_plural = 'products'
 
    # Product (1), Product (2), Product (3)
    def __str__(self):

        return self.title
    
    # Create a dynamic custom urls -> with respect to the slug name
    def get_absolute_url(self):

        return reverse('product-info', args=[self.slug])