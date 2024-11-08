from src.core.models.post import Post
from src.core import database

def create_enums():
    from src.core.models.post import states_enum
    states_enum.create(database.db.engine, checkfirst=True)

def list_all_posts():
    return Post.query.all()

def list_posts():
    """
    Return all the posts that are published
    """
    return Post.query.filter_by(state='Publicado').all()

def title_exists(title):
    return Post.query.filter_by(title=title).first() is not None

def get_post(post_id):
    return Post.query.get(post_id)

def create_post(title, content, author, summary, state, posted_at):
    try:
        post = Post(title=title, content=content, author=author, summary=summary, state=state, posted_at=posted_at)
        database.db.session.add(post)
        database.db.session.commit()
    except Exception as e:
        database.db.session.rollback()
        raise e
    return post

def update_post(post_id, title, content, summary, state, posted_at):
    try:
        post = get_post(post_id)
        post.title = title
        post.content = content
        post.summary = summary
        post.state = state
        post.posted_at = posted_at
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
        query = query.filter(Post.title == title)

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