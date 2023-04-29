from werkzeug.security import check_password_hash


class User:
    def __init__(self, username, password, created_at):
        self.username = username
        self.password = password
        self.created_at = created_at

    @staticmethod
    def is_authenticated(self):
        return True

    @staticmethod
    def is_active(self):
        return True

    @staticmethod
    def is_anonymous(self):
        return False

    def created_time(self):
        return self.created_at

    def get_id(self):
        return self.username

    def check_password(self, password_input):
        return check_password_hash(self.password, password_input)
