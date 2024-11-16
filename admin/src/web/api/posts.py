from src.core import post
from src.web.schema.post import posts_schema as posts_api
from flask import Blueprint, request, jsonify, Response

bp = Blueprint('posts_api', __name__, url_prefix='/api/posts')

@bp.get('/')
def index_posts():

    author = request.args.get('author',  default= None)
    published_from = request.args.get('published_from',  default= None)
    published_to = request.args.get('published_to',  default= None)
    page = request.args.get('page',  default= 1, type=int)
    per_page = request.args.get('per_page', default= 25, type=int)

    posts = post.list_posts(page, per_page, author, published_from, published_to)
    data = posts_api.dumps(posts)

    return Response(data, mimetype='application/json')

