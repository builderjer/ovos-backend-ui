class DuplicateUserError(Exception):
    def __init__(self, *user_id):
        super().__init__(user_id)
        if user_id:
            self.user_id = user_id[0]
        else:
            self.user_id = ''

    def __str__(self):
        return f"User {self.user_id} already exists"

class NoUserError(Exception):
    def __init__(self, *user_id):
        super().__init__(user_id)
        if user_id:
            self.user_id = user_id[0]
        else:
            self.user_id = ''

    def __str__(self):
        return f"User {self.user_id} does not exist"
