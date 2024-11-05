from src.core.models.post import Post

def list_posts():
    return Post.query.all()