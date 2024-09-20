from src.core import board
from src.core.database import db



def run():

    issue1 = board.create_issue(
        title="Issue 1",
        description="This is the first issue",
        status="new",
        email = "Ejemplo@gmail.com"
    )
    issue2 = board.create_issue(
        title="Issue 2",
        description="This is the second issue",
        status="closed",
        email = "Ejemplo@gmail.com"
    )
    db.session.commit()
    issue3 = board.create_issue(
        title="Issue 3",
        description="This is the third issue",
        status="new",
        email = "Ejemplo@gmail.com"
    )

    user1 = board.create_user(
        email="Ejemplo@gmail.com",
        password="123456"
    )

