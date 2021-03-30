import requests
from user import User
import os
from dotenv import load_dotenv

# Load env variables
load_dotenv()

SHEETY_TOKEN = os.environ.get("SHEETY_TOKEN")
sheety_header = {"Authorization": f'Bearer {SHEETY_TOKEN}'}

response = requests.get(url="https://api.sheety.co/dd227305523e98d4aa37bcaff9e48d3e/24K/users", headers=sheety_header)
users_json = response.json()["users"]


# username_table = {u.username: u for u in users}
# userid_table = {u.id: u for u in users}
# s = [
#     {'id': 2, 'userName': 'sethluan', 'email': 'seth.luan@24karat.io', 'password': 'monster', 'userType': 0},
#     {'id': 3, 'userName': 'mogawa', 'email': 'ogawa.masaki@24karat.io', 'password': 'hunter', 'userType': 0}
# ]


class UserUtility:
    def __init__(self):
        self.users = {
            user['id']: User(
                user["id"],
                user["userName"],
                user["email"],
                user["password"]
            )
            for user in users_json}

    def find_user(self, user_id):
        user = self.users.get(int(user_id))
        return user