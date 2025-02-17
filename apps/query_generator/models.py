from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

class Company(models.Model):
    name = models.CharField(max_length=255)
    industry = models.CharField(max_length=255)
    description = models.TextField()
    website = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Companies"

    def __str__(self):
        return self.name

class ProductCategory(models.Model):
    name = models.CharField(max_length=255)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='product_categories')
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Product categories"

    def __str__(self):
        return f"{self.company.name} - {self.name}"

class Query(models.Model):
    QUERY_TYPE_CHOICES = [
        ('BRAND', 'Brand Perception'),
        ('PRODUCT', 'Product Specific'),
        ('SERVICE', 'Customer Service'),
        ('COMP', 'Competitive Analysis'),
        ('TREND', 'Market Trends'),
        ('SENT', 'Sentiment Analysis')
    ]

    PRIORITY_CHOICES = [
        ('HIGH', 'High'),
        ('MEDIUM', 'Medium'),
        ('LOW', 'Low')
    ]

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='queries')
    product_category = models.ForeignKey(
        ProductCategory, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='queries'
    )
    query_text = models.TextField()
    query_type = models.CharField(max_length=10, choices=QUERY_TYPE_CHOICES)
    priority = models.CharField(max_length=6, choices=PRIORITY_CHOICES, default='MEDIUM')
    is_active = models.BooleanField(default=True)
    relevance_score = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        default=0.5
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_executed = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Queries"
        ordering = ['-relevance_score', '-created_at']

    def __str__(self):
        return f"{self.company.name} - {self.query_type}: {self.query_text[:50]}..."

class QueryTag(models.Model):
    query = models.ForeignKey(Query, on_delete=models.CASCADE, related_name='tags')
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=255)
    
    class Meta:
        unique_together = ['query', 'name']

    def __str__(self):
        return f"{self.query.company.name} - {self.name}: {self.value}"

class QueryTemplate(models.Model):
    template_text = models.TextField()
    query_type = models.CharField(max_length=10, choices=Query.QUERY_TYPE_CHOICES)
    industry = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.industry} - {self.query_type}: {self.template_text[:50]}..."
