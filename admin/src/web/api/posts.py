from src.core import post
from src.web.schema.post import posts_schema as posts_api
from flask import Blueprint, request, jsonify

bp = Blueprint('posts_api', __name__, url_prefix='/api/posts')

@bp.get('/')
def index_posts():

    posts = post.list_posts()
    data = posts_api.dumps(posts)

    return jsonify(data)

