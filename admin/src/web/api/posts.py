from src.core import post
from src.web.schema.post import posts_schema as posts_api
from flask import Blueprint, request, jsonify, Response

bp = Blueprint("posts_api", __name__, url_prefix="/api/posts")


@bp.get("/")
def index_posts():
    """
    Handles the GET request to retrieve a paginated list of posts.

    Endpoint: /api/posts/

    Query Parameters:
    - page (int, optional): The page number to retrieve. Defaults to 1.
    - per_page (int, optional): The number of posts per page. Defaults to 25.

    Returns:
    - Response: A JSON response containing the list of posts and pagination metadata.

    Response JSON Structure:
    {
        "data": [ ... ],  # List of posts for the current page
            "current_page": int,  # The current page number
            "per_page": int,  # The number of posts per page
            "total_pages": int,  # The total number of pages
            "total_items": int,  # The total number of posts
            "has_next_page": bool  # Whether there is a next page
    """

    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("per_page", default=25, type=int)

    # Get posts from the database
    posts, total_posts = post.list_posts(page, per_page)

    # Calculate metadata
    total_pages = (total_posts + per_page - 1) // per_page
    has_next_page = page < total_pages

    response_data = posts
    data = posts_api.dump(response_data)

    data = {
        "data": data,
        "meta": {
            "current_page": page,
            "per_page": per_page,
            "total_pages": total_pages,
            "total_items": total_posts,
            "has_next_page": has_next_page,
        },
    }

    return jsonify(data)
