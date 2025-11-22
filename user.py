import uuid

class User:
    def __init__(self, name, course, year, interests, noise_level, sleep_schedule, social_level):
        self.id = str(uuid.uuid4())
        self.name = name
        self.course = course
        self.year = year
        self.interests = interests          
        self.noise_level = noise_level      
        self.sleep_schedule = sleep_schedule  
        self.social_level = social_level    


# User Storage + CRUD


users = {}

def create_user(name, course, year, interests, noise_level, sleep_schedule, social_level):
    user = User(name, course, year, interests, noise_level, sleep_schedule, social_level)
    users[user.id] = user
    return user

def get_user(user_id):
    return users.get(user_id)

def update_user(user_id, **kwargs):
    user = users.get(user_id)
    if not user:
        return None
    for key, value in kwargs.items():
        if hasattr(user, key):
            setattr(user, key, value)
    return user

def get_all_users(exclude_id=None):
    return [u for uid, u in users.items() if uid != exclude_id]



# Matching Logic


def jaccard_similarity(list1, list2):
    set1, set2 = set(list1), set(list2)
    if not set1 or not set2:
        return 0
    return len(set1 & set2) / len(set1 | set2)

def calculate_match_score(user, other):
    # 40% Interests
    interest_score = jaccard_similarity(user.interests, other.interests)

    # 40% Lifestyle
    sleep_score = 1 if user.sleep_schedule == other.sleep_schedule else 0
    noise_score = 1 - abs(user.noise_level - other.noise_level) / 4
    social_score = 1 - abs(user.social_level - other.social_level) / 4
    lifestyle_score = (sleep_score + noise_score + social_score) / 3

    # 20% Bonus based on course and year
    bonus = 0
    if user.course == other.course:
        bonus += 0.1
    if user.year == other.year:
        bonus += 0.1

    total = 0.4 * interest_score + 0.4 * lifestyle_score + 0.2 * bonus
    return round(total * 100, 2)

def get_matches(user_id, top_n=5):
    user = get_user(user_id)
    if not user:
        return []

    others = get_all_users(exclude_id=user_id)
    scored = [{"user": o, "score": calculate_match_score(user, o)} for o in others]
    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:top_n]


#  Print All Users


def print_all_users():
    print("\n=== ALL USERS IN MEMORY ===")
    for user in users.values():
        print(f"ID: {user.id}")
        print(f"Name: {user.name}")
        print(f"Course: {user.course}")
        print(f"Year: {user.year}")
        print(f"Interests: {user.interests}")
        print(f"Noise Level: {user.noise_level}")
        print(f"Sleep Schedule: {user.sleep_schedule}")
        print(f"Social Level: {user.social_level}")
        print("-" * 40)



# Demo Run


if __name__ == "__main__":
    # Create sample users
    u1 = create_user("Alice", "Computer Science", 1, ["gaming", "music"], 3, "Late", 4)
    u2 = create_user("Bob", "Computer Science", 1, ["music", "gym"], 2, "Late", 3)
    u3 = create_user("Charlie", "Engineering", 2, ["gaming", "sports"], 5, "Early", 2)

    print("User created:", u1.id)

    # Show all users
    print_all_users()

    # Show matches for Alice
    print("\n=== MATCHES FOR ALICE ===")
    matches = get_matches(u1.id)
    for m in matches:
        print(f"Match: {m['user'].name}, Score: {m['score']}")
