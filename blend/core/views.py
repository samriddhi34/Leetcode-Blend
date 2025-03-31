from django.shortcuts import render
from django.http import JsonResponse
from .utils.leetcode_api import fetch_leetcode_user_data
from .utils.leetcode_parser import parse_leetcode_data
from .models import LeetCodeUser , Question  # If LeetCodeUser is in the same app's models.py
from django.db.models import Q
from collections import defaultdict




# Create your views here.
def index(request):
    return render(request , 'core/home.html')

def user(request):
    return render(request , 'core/user.html')


def compare_users(request):
    if request.method == 'GET':
        usernames_str = request.GET.get('users', '')
        usernames = [u.strip() for u in usernames_str.split(',') if u.strip()]
        print(f"Trying usernames: {usernames}")  # Debugging
        
        users_data = []
        for username in usernames:
            try:
                print(f"\n=== Trying {username} ===")  # Debugging
                raw_data = fetch_leetcode_user_data(username)
                print("Raw API response:", raw_data)  # Debugging
                if not raw_data:
                    raise ValueError(f"No data found for {username}")
                    
                parsed_data = parse_leetcode_data(raw_data)
                print("Parsed data:", parsed_data)  # Debugging
                if not parsed_data:
                    raise ValueError(f"Failed to parse data for {username}")

                user, _ = LeetCodeUser.objects.update_or_create(
                    username=username,
                    defaults=parsed_data
                )
                users_data.append(user)
                
            except Exception as e:
                print(f"Error processing {username}: {str(e)}")
                continue
        
        if not users_data:
            return render(request, 'core/error.html', {'message': 'No valid users found'})
        users_data = sorted(users_data , key = lambda user : user.total_solved , reverse= True)
            
        return render(request, 'core/results.html', {'users': users_data})
    

def generate_common_list(request):
    context = {'users': [], 'common_topics': [], 'questions': [], 'error': None}
    
    if request.method == 'POST':
        try:
            usernames = request.POST.get('usernames', '').split(',')
            if len(usernames) < 2:
                raise ValueError("At least two usernames required")
                
            # Fetch users and their topics
            users = LeetCodeUser.objects.filter(username__in=usernames)
            if users.count() < 2:
                raise ValueError("One or more users not found")
                
            context['users'] = [user.username for user in users]

            # Find common topics across all users
            common_topics = set(users[0].topics.keys())
            for user in users[1:]:
                common_topics &= set(user.topics.keys())
                if not common_topics:
                    break

            if not common_topics:
                raise ValueError("No common topics found between users")
                
            # Calculate average solved count for each common topic
            topic_avg = {}
            for topic in common_topics:
                total = sum(user.topics.get(topic, 0) for user in users)
                avg = total / len(users)
                topic_avg[topic] = avg
            
            # Sort topics by average (descending)
            sorted_topics = sorted(topic_avg.items(), key=lambda x: -x[1])
            context['common_topics'] = [t[0] for t in sorted_topics]

            # Fetch all questions with ANY common topic
            query = Q()
            for topic, _ in sorted_topics:
                query |= Q(topics__icontains=topic)  # SQLite workaround
            
            questions = Question.objects.filter(query).distinct()

            # Assign priority to questions based on their highest-ranked topic
            question_priority = []
            for question in questions:
                # Find all common topics this question belongs to
                question_topics = [t for t in question.topics if t in topic_avg]
                if not question_topics:
                    continue  # Skip if no overlap (edge case)
                
                # Get the highest priority (topic with highest average)
                max_priority = max(topic_avg[t] for t in question_topics)
                
                # Difficulty order: Easy=0, Medium=1, Hard=2
                difficulty_order = {'E': 0, 'M': 1, 'H': 2}
                
                # Use question_id as tiebreaker
                question_priority.append((
                    -max_priority,  # Negative for ascending sort
                    difficulty_order[question.difficulty],
                    -question.acceptance_rate,
                    question.question_id  # Use ID instead of the object
                ))
            
            # Sort by priority, difficulty, acceptance rate, then ID
            question_priority.sort()
            
            # Extract sorted question IDs (first 20)
            sorted_question_ids = [q[3] for q in question_priority[:20]]
            
            # Preserve order using Django's Case/When
            from django.db.models import Case, When
            preserved_order = Case(
                *[When(question_id=id, then=pos) for pos, id in enumerate(sorted_question_ids)]
            )
            context['questions'] = Question.objects.filter(
                question_id__in=sorted_question_ids
            ).order_by(preserved_order)

        except Exception as e:
            context['error'] = str(e)

    return render(request, 'core/common_list.html', context)