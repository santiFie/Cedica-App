from src.core.models.post import Post
from src.core import database

def create_enums():
    from src.core.models.post import states_enum
    states_enum.create(database.db.engine, checkfirst=True)

def list_posts():
    return Post.query.filter_by(state='Publicado').all()

def title_exists(title):
    return Post.query.filter_by(title=title).first() is not None

def create_post(title, content, author, summary, state, posted_at):
    try:
        post = Post(title=title, content=content, author=author, summary=summary, state=state, posted_at=posted_at)
        database.db.session.add(post)
        database.db.session.commit()
    except Exception as e:
        database.db.session.rollback()
        raise e
    return post