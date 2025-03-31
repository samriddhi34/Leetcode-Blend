import requests

def fetch_leetcode_user_data(username):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Content-Type": "application/json"
        }
        
        response = requests.post(
            "https://leetcode.com/graphql",
            json={
                "query": """
                query getUserProfile($username: String!) {
                    matchedUser(username: $username) {
                        submitStatsGlobal {
                            acSubmissionNum { difficulty count }
                        }
                        tagProblemCounts {
                            advanced { tagName problemsSolved }
                            intermediate { tagName problemsSolved }
                            fundamental { tagName problemsSolved }
                        }
                    }
                }
                """,
                "variables": {"username": username}
            },
            headers=headers,
            timeout=10
        )
        
        if response.status_code != 200:
            return None
            
        return response.json()
        
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {str(e)}")
        return None