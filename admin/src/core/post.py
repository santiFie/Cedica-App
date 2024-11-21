from src.core.models.post import Post
from src.core import database
from datetime import datetime

def create_enums():
    from src.core.models.post import states_enum
    states_enum.create(database.db.engine, checkfirst=True)

def list_all_posts():
    return Post.query.all()

def list_posts( page, per_page, author = None, published_from = None, published_to= datetime.now()):
    """
    Return posts that are published
    """

    query = Post.query.filter_by(state='Publicado')

    if author:
        query = query.filter(Post.author.ilike(f'%{author}%'))

    if published_from:
        query = query.filter(Post.posted_at >= published_from)

    if published_to:
        query = query.filter(Post.posted_at <= published_to)

    total_post = query.count()

    max_pages = (total_post + per_page - 1) // per_page

    page = max(1, min(page, max_pages))

    offset = (page - 1) * per_page
    posts = query.order_by(Post.posted_at.desc()).offset(offset).limit(per_page).all()

    return posts, total_post


def title_exists(title):
    return Post.query.filter_by(title=title).first() is not None

def get_post(post_id):
    return Post.query.get(post_id)

def create_post(title, content, author, summary, state):
    try:
        if state == "Publicado":
            posted_at = datetime.now()
        else:
            posted_at = None
        post = Post(title=title, content=content, author=author, summary=summary, state=state, posted_at=posted_at)
        database.db.session.add(post)
        database.db.session.commit()
    except Exception as e:
        database.db.session.rollback()
        raise e
    return post

def update_post(post_id, title, content, summary, state):
    try:
        post = get_post(post_id)
        post.title = title
        post.content = content
        post.summary = summary
        if post.state != "Publicado" and state == "Publicado":
            post.posted_at = datetime.now()
        if post.state == "Publicado" and state != "Publicado":
            post.posted_at = None
        post.state = state
        database.db.session.commit()
    except Exception as e:
        database.db.session.rollback()
        raise e
    return post

def delete_post(post_id):
    post = get_post(post_id)
    if post is None:
        return False
    database.db.session.delete(post)
    database.db.session.commit()

    return True

def find_all_posts(title=None, state=None, order_by='asc', page=1):
    """
    Search for all posts and horsewomen with the given parameters
    """

    per_page = 10

    query = Post.query

    # Filtro por title
    if title:
        query = query.filter(Post.title.ilike(f"%{title}%"))

    # Filtro por state
    if state:
        query = query.filter(Post.state == state)

    # Ordenamiento
    if order_by == "asc":
        query = query.order_by(
            Post.title.asc()
        )  
    else:
        query = query.order_by(
            Post.title.desc()
        )  

    total_posts = query.count()

    # Manejo del caso en el que no haya posts
    if total_posts == 0:
        return [], 0

    max_pages = (total_posts + per_page - 1) // per_page  # Redondeo hacia arriba

    # Aseguramos que la página solicitada no sea menor que 1
    if page < 1:
        page = 1

    # Aseguramos que la página solicitada no sea mayor que el número máximo de páginas
    if page > max_pages:
        page = max_pages

    offset = (page - 1) * per_page
    posts = query.offset(offset).limit(per_page).all()

    return posts, max_pages