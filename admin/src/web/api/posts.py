from src.core import post
from src.web.schema.post import post_schema as post_api
from flask import Blueprint, request, Response

bp = Blueprint('posts_api', __name__, url_prefix='/api/posts')

@bp.get('/')
def index_posts():

    posts = post.list_posts()
    data = post_api.dumps(posts)

    return make_json_response(data)


def make_json_response(data, status_code=200):
    return Response(data, status=status_code, mimetype='application/json')