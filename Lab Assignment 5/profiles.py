"""
profiles.py - handles user data storage and retrieval
uses a dict as hash table internally
"""


class ProfileManager:
    def __init__(self):
        self.users = {}

    def add_user(self, uid, name, age, interests, city="", profession="", bio=""):
        if not uid or not isinstance(uid, str):
            print("  [ERROR] Invalid user ID.")
            return False
        if uid in self.users:
            print(f"  [ERROR] '{uid}' already exists.")
            return False
        self.users[uid] = {
            "user_id": uid,
            "name": name,
            "age": age,
            "interests": list(interests),
            "city": city,
            "profession": profession,
            "bio": bio,
        }
        return True

    def get_user_profile(self, uid):
        p = self.users.get(uid)
        if p is None:
            print(f"  [ERROR] User '{uid}' not found.")
        return p

    def update_user_profile(self, uid, **fields):
        if uid not in self.users:
            print(f"  [ERROR] '{uid}' not found.")
            return False
        allowed = {"name", "age", "interests", "city", "profession", "bio"}
        for k, v in fields.items():
            if k in allowed:
                self.users[uid][k] = v
        return True

    def user_exists(self, uid):
        return uid in self.users

    def all_user_ids(self):
        return list(self.users.keys())

    def display_profile(self, uid):
        p = self.get_user_profile(uid)
        if not p:
            return
        print(f"""
  ┌─ Profile ──────────────────────────────────┐
  │  ID         : {p['user_id']:<30}│
  │  Name       : {p['name']:<30}│
  │  Age        : {str(p['age']):<30}│
  │  Interests  : {', '.join(p['interests']):<30}│
  │  City       : {p['city']:<30}│
  │  Profession : {p['profession']:<30}│
  │  Bio        : {p['bio'][:30]:<30}│
  └─────────────────────────────────────────────┘""")

    def display_all_profiles(self):
        if not self.users:
            print("  (no users yet)")
            return
        for uid in self.users:
            self.display_profile(uid)
