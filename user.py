from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, user_id, user_name, email, password):
        self.id = user_id
        self.user_name = user_name
        self.email = email
        self.password = password
        # admin - 0
        # creator - 1
        # collector - 2
        self.user_type = ''
        self.profile_img = ''
        self.balance = 0

