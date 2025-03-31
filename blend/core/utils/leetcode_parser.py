def parse_leetcode_data(data):
    try:
        if not data or "data" not in data or not data["data"]["matchedUser"]:
            return None

        user_data = data["data"]["matchedUser"]
        
        # Extract solved counts
        stats = user_data["submitStatsGlobal"]["acSubmissionNum"]
        solved_stats = {item["difficulty"]: item["count"] for item in stats}
        
        # Extract topics
        topics = {}
        for category in ["advanced", "intermediate", "fundamental"]:
            for tag in user_data["tagProblemCounts"][category]:
                topics[tag["tagName"]] = tag["problemsSolved"]

        return {
            "total_solved": solved_stats.get("All", 0),
            "easy_solved": solved_stats.get("Easy", 0),
            "medium_solved": solved_stats.get("Medium", 0),
            "hard_solved": solved_stats.get("Hard", 0),
            "topics": topics
        }
    except KeyError as e:
        print(f"Parsing error: Missing key {str(e)}")
        return None