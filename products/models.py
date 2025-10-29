from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify


GENDER_CHOICES = [
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Unisex', 'Unisex'),
]

CATEGORY_CHOICES = [
    ('Hoodie', 'Hoodie'),
    ('Pants', 'Pants'),
    ('Socks', 'Socks'),
    ('T-Shirt', 'T-Shirt'),
    ('Accessory', 'Accessory'),
]

SIZE_CHOICES = [
    ('XS', 'XS'),
    ('S', 'S'),
    ('M', 'M'),
    ('L', 'L'),
    ('XL', 'XL'),
    ('XXL', 'XXL'),
]



class Collection(models.Model):

    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    release_date = models.DateField(blank=True, null=True)

    class Meta:
        ordering = ['-release_date']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)




class Product(models.Model):
    title = models.CharField(max_length=255)
    collection = models.ForeignKey(Collection, on_delete=models.SET_NULL, null=True, blank=True,related_name='products')
    description_text = models.TextField()
    slug = models.SlugField(unique=True, blank=True)
    categories = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    size = models.CharField(max_length=5, choices=SIZE_CHOICES, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, db_index=True)
    stock = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    color = models.CharField(max_length=30, blank=True, null=True)
    review = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        default=0,
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            num = 1
            while Product.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{num}"
                num += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title




class ProductVariant(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='variants')
    color = models.CharField(max_length=50)
    size = models.CharField(max_length=4, choices=SIZE_CHOICES)
    stock = models.PositiveIntegerField(default=0)
    sku = models.CharField(max_length=100, blank=True, null=True)



    def save(self, *args, **kwargs):
        if not self.sku:
            base = self.product.title.replace(" ", "").upper()
            self.sku = f"{base[:6]}-{self.color[:3].upper()}-{self.size.upper()}"
        super().save(*args, **kwargs)


    class Meta:
        unique_together = ('product', 'color', 'size')

    def __str__(self):
        return f"{self.product.title} - {self.color} ({self.size})"




class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    filename = models.CharField(max_length=255)
    alt_text = models.CharField(max_length=255, blank=True)
    order = models.PositiveIntegerField(default=0)
    image_type = models.CharField(
        max_length=20,
        choices=[
            ("thumbnail", "Thumbnail"),
            ("gallery", "Gallery"),
            ("banner", "Banner"),
        ],
        default="gallery"
    )


    def __str__(self):
        return f"{self.product.title}{self.product.color} - {self.filename}"



