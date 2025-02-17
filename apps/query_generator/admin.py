from django.contrib import admin
from .models import Company, ProductCategory, Query, QueryTag, QueryTemplate

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'industry', 'created_at', 'updated_at')
    search_fields = ('name', 'industry')
    list_filter = ('industry', 'created_at')

@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'company')
    search_fields = ('name', 'company__name')
    list_filter = ('company',)

@admin.register(Query)
class QueryAdmin(admin.ModelAdmin):
    list_display = ('company', 'query_type', 'priority', 'is_active', 'relevance_score', 'created_at')
    list_filter = ('query_type', 'priority', 'is_active', 'company')
    search_fields = ('query_text', 'company__name')
    readonly_fields = ('created_at', 'updated_at', 'last_executed')

@admin.register(QueryTag)
class QueryTagAdmin(admin.ModelAdmin):
    list_display = ('query', 'name', 'value')
    list_filter = ('name', 'query__company')
    search_fields = ('name', 'value', 'query__query_text')

@admin.register(QueryTemplate)
class QueryTemplateAdmin(admin.ModelAdmin):
    list_display = ('query_type', 'industry', 'is_active', 'created_at')
    list_filter = ('query_type', 'industry', 'is_active')
    search_fields = ('template_text', 'industry')
