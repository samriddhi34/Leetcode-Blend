from django.db import models

# Create your models here.
class LeetCodeUser(models.Model):
    username = models.CharField(max_length = 100 , unique = True)
    total_solved = models.IntegerField(default = 0)
    easy_solved = models.IntegerField(default = 0)
    medium_solved = models.IntegerField(default = 0)
    hard_solved = models.IntegerField(default = 0)
    topics = models.JSONField(default = dict)
    last_updated = models.DateTimeField(auto_now=True)
    def is_outdated(self):
        # Refresh data if older than 24 hours
        return (timezone.now() - self.last_updated) > timedelta(hours=24)
    
class Question(models.Model):
    DIFFICULTY_CHOICES = [
        ('E' , 'Easy'),
        ('M' , 'Medium'),
        ('H' , 'Hard')
    ]
    question_id = models.IntegerField(unique=True)
    title = models.CharField(max_length=255)
    acceptance_rate = models.FloatField(default= 0)
    isPremium = models.BooleanField()
    difficulty = models.CharField(max_length= 10 , choices= DIFFICULTY_CHOICES)
    Question_Link = models.URLField()
    solution = models.URLField(blank=True, null=True)
    topics = models.JSONField(default= list)

    def __str__(self):
        return f"{self.question_id}. {self.title} "

                                     
