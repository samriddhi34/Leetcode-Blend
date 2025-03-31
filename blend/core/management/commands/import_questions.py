# core/management/commands/import_questions.py
import csv
from django.core.management.base import BaseCommand
from core.models import Question

class Command(BaseCommand):
    help = 'Import LeetCode questions from CSV'
    
    def add_arguments(self, parser):
        parser.add_argument('csv_path', type=str)
        
    def handle(self, *args, **options):
        difficulty_mapping = {
            "Easy": "E",
            "Medium": "M",
            "Hard": "H"
        }
        
        with open(options['csv_path'], 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    # Extract topics
                    topics = [t.strip() for t in row['topics'].split(',')] if row.get('topics') else []
                    
                    # Map difficulty (e.g., "Easy" → "E")
                    difficulty = difficulty_mapping.get(row['Difficulty'], 'E')  # Default to 'E'
                    
                    # Create the question
                    Question.objects.create(
                        question_id=int(row['Question_No']),
                        title=row['Question'],
                        acceptance_rate=float(row['Acceptance'].strip('%')) / 100,
                        isPremium=row['isPremium'].lower() == 'true',
                        difficulty=difficulty,  # Now "E", "M", or "H"
                        Question_Link=row['Question_Link'],
                        solution=row['Solution'] if row['Solution'] else None,
                        topics=topics
                    )
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error in row {row}: {str(e)}"))