from app import db
from app.models import User


from sqlalchemy import update

import sys

if len(sys.argv) == 3:
    print("Setting isAdmin for user", sys.argv[1], "to", sys.argv[2])
    USERNAME = sys.argv[1]
    ISADMIN = sys.argv[2]
else:
    print(len(sys.argv))
    print("Usage", sys.argv[0], "username 1/0")
    sys.exit(1)

user = User.query.filter_by(username = USERNAME).one()
print("Current Setting:", user.username, "isAdmin:", user.isAdmin)
user.isAdmin = ISADMIN



db.session.commit()
print("\nNew Setting:", user.username, "isAdmin:", user.isAdmin)