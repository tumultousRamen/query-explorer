import openai
from django.conf import settings
from typing import List
from .models import Company, Query, QueryTemplate, QueryTag

class QueryGenerationService:
    def __init__(self, company: Company):
        self.company = company
        openai.api_key = settings.OPENAI_API_KEY

    def generate_queries(self, num_queries: int = 50) -> List[Query]:
        # Get templates for the company's industry
        templates = QueryTemplate.objects.filter(
            industry=self.company.industry,
            is_active=True
        )
        
        system_prompt = f"""
        Generate specific, analytical queries about {self.company.name}, a company in the {self.company.industry} industry.
        Focus on brand perception, product quality, customer service, and market positioning.
        Each query should be detailed and specific, suitable for AI analysis.
        """

        template_examples = "\n".join([t.template_text for t in templates])
        
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Generate {num_queries} unique queries. Use these templates as examples:\n{template_examples}"}
            ],
            temperature=0.8,
            max_tokens=2000
        )

        # Parse and store queries
        generated_queries = []
        query_texts = self._parse_gpt_response(response)
        
        for query_text in query_texts:
            query_type = self._determine_query_type(query_text)
            query = Query.objects.create(
                company=self.company,
                query_text=query_text,
                query_type=query_type,
                relevance_score=0.7  # Default score, can be adjusted later
            )
            self._generate_tags(query)
            generated_queries.append(query)

        return generated_queries

    def _parse_gpt_response(self, response) -> List[str]:
        # Implementation to parse GPT response into individual queries
        # This would need to be adapted based on the actual response format
        content = response.choices[0].message.content
        return [q.strip() for q in content.split('\n') if q.strip()]

    def _determine_query_type(self, query_text: str) -> str:
        # Use GPT to classify query type
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Classify this query into one of these categories: BRAND, PRODUCT, SERVICE, COMP, TREND, SENT"},
                {"role": "user", "content": query_text}
            ],
            temperature=0.3
        )
        return response.choices[0].message.content.strip()

    def _generate_tags(self, query: Query):
        # Generate relevant tags for the query
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Generate 3-5 relevant tags for this query in format 'key: value'"},
                {"role": "user", "content": query.query_text}
            ],
            temperature=0.3
        )
        
        tags = response.choices[0].message.content.strip().split('\n')
        for tag in tags:
            if ':' in tag:
                name, value = tag.split(':', 1)
                QueryTag.objects.create(
                    query=query,
                    name=name.strip(),
                    value=value.strip()
                ) 