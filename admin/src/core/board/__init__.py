from src.core.board.issue import Issue, User
from src.core.database import db

def list_issues():
    issues = Issue.query.all()

    return issues

def create_issue(**kwargs):
    issue = Issue(**kwargs)
    db.session.add(issue)
    db.session.commit()
    print(issue)


    return issue

def create_user(**kwargs):
    user = User(**kwargs)
    db.session.add(user)
    db.session.commit()

    return user

