from django.core.management.base import BaseCommand
from query_generator.models import Company, ProductCategory, QueryTemplate
from query_generator.services import QueryGenerationService

class Command(BaseCommand):
    help = 'Generates test queries for a sample company'

    def handle(self, *args, **kwargs):
        # Create a test company
        company, created = Company.objects.get_or_create(
            name="Nike",
            defaults={
                'industry': "Sports and Apparel",
                'description': "Global leader in athletic footwear and apparel",
                'website': "https://www.nike.com"
            }
        )
        self.stdout.write(f"{'Created' if created else 'Found'} company: {company.name}")

        # Create some product categories
        categories = [
            "Running Shoes",
            "Basketball Shoes",
            "Athletic Apparel",
            "Sports Equipment"
        ]
        
        for cat_name in categories:
            category, created = ProductCategory.objects.get_or_create(
                name=cat_name,
                company=company,
                defaults={'description': f"{cat_name} by {company.name}"}
            )
            self.stdout.write(f"{'Created' if created else 'Found'} category: {category.name}")

        # Create some query templates
        templates = [
            {
                'query_type': 'BRAND',
                'template_text': "What is the overall brand perception of {company} in the {industry} market?"
            },
            {
                'query_type': 'PRODUCT',
                'template_text': "How do customers rate {company}'s {product_category} in terms of quality and durability?"
            },
            {
                'query_type': 'SERVICE',
                'template_text': "What are common customer service experiences with {company} in their retail stores?"
            }
        ]

        for template in templates:
            QueryTemplate.objects.get_or_create(
                template_text=template['template_text'],
                query_type=template['query_type'],
                industry=company.industry
            )
            self.stdout.write(f"Created template for type: {template['query_type']}")

        # Generate queries
        service = QueryGenerationService(company)
        queries = service.generate_queries(num_queries=5)  # Start with 5 for testing
        
        self.stdout.write(self.style.SUCCESS(f'Successfully generated {len(queries)} queries'))
        
        # Print generated queries
        for query in queries:
            self.stdout.write("\n" + "="*50)
            self.stdout.write(f"Query Type: {query.query_type}")
            self.stdout.write(f"Query Text: {query.query_text}")
            self.stdout.write("Tags:")
            for tag in query.tags.all():
                self.stdout.write(f"  - {tag.name}: {tag.value}") 