from flask import (
    Blueprint,
    redirect,
    render_template,
    request,
    flash,
    send_file,
    session,
    url_for,
)
from src.web.forms import NewPostForm, EditPostForm
from src.core import post
from src.core.models.post import states_enum

bp = Blueprint('posts', __name__, url_prefix='/posts')

@bp.get('/')
def index_posts():
    title = request.args.get('title')
    state = request.args.get('state')
    order_by = request.args.get('order_by')
    page = request.args.get("page", 1, type=int)
    posts, max_pages = post.find_all_posts(title, state, order_by, page=page)
    
    return render_template('posts/index_posts.html', posts=posts, page=page, max_pages=max_pages, states=states_enum.enums)

@bp.get('/new')
def new_post():
    states = states_enum.enums
    return render_template('posts/new_post.html', states=states)

@bp.post('/create')
def create_post():
    form = NewPostForm(request.form)
    if not form.validate():
        flash('Formulario inválido', 'error')
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'{field}: {error}', 'error')
        return render_template('posts/new_post.html', states=states_enum.enums)

    title = form.title.data
    content = form.content.data
    author = session['user']
    summary = form.summary.data
    state = form.state.data
    posted_at = form.posted_at.data

    post.create_post(title, content, author, summary, state, posted_at)
    flash('Publicación creada correctamente')
    return redirect(url_for('posts.new_post'))

@bp.get('/edit/<int:post_id>')
def edit_post(post_id):
    post_to_edit = post.get_post(post_id)
    states = states_enum.enums
    return render_template('posts/edit_post.html', post=post_to_edit, states=states)

@bp.post('/update/<int:post_id>')
def update_post(post_id):
    form = EditPostForm(request.form)
    if not form.validate():
        flash('Formulario inválido', 'error')
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'{field}: {error}', 'error')
        post_to_edit = post.get_post(post_id)
        return render_template('posts/edit_post.html', states=states_enum.enums, post=post_to_edit)

    title = request.form["title"]
    content = form.content.data
    summary = form.summary.data
    state = form.state.data
    posted_at = form.posted_at.data

    post.update_post(post_id, title, content, summary, state, posted_at)
    flash('Publicación actualizada correctamente')
    return redirect(url_for('posts.edit_post', post_id=post_id))

@bp.get('/delete/<int:post_id>')
def delete_post(post_id):
    print(post_id)
    if post.delete_post(post_id):
        flash('Publicación eliminada correctamente')
    else:
        flash('Error al eliminar la publicación', 'error')

    return redirect(url_for('posts.index_posts'))