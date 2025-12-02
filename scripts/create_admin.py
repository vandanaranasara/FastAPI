import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.models import User
from app.utils import hash_password  # or Hasher.hash_password

def create_admin():
    db = SessionLocal()

    admin = db.query(User).filter(User.username == "admin@gmail.com").first()

    if admin:
        print("Admin already exists:", admin.username)
        return


    new_admin = User(
        username="admin@gmail.com",
        password=hash_password("admin123"),
        is_admin=True
    )

    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)

    print("Admin created:", new_admin.username)


if __name__ == "__main__":
    create_admin()
