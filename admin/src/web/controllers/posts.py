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
from src.web.forms.PostForm import NewPostForm, EditPostForm
from src.core import post
from src.core.models.post import states_enum
from src.web.handlers.auth import login_required
from src.web.handlers.users import check_permissions

bp = Blueprint('posts', __name__, url_prefix='/posts')

@bp.get('/')
@check_permissions("post_index")
@login_required
def post_index():
    title = request.args.get('title')
    state = request.args.get('state')
    order_by = request.args.get('order_by')
    page = request.args.get("page", 1, type=int)
    posts, max_pages = post.find_all_posts(title, state, order_by, page=page)
    
    return render_template('posts/index_posts.html', posts=posts, page=page, max_pages=max_pages, states=states_enum.enums)

@bp.get('/new')
@check_permissions("post_new")
@login_required
def post_new():
    states = states_enum.enums
    return render_template('posts/new_post.html', states=states)

@bp.post('/create')
@check_permissions("post_create")
@login_required
def post_create():
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

    post.create_post(title, content, author, summary, state)
    flash('Publicación creada correctamente')
    return redirect(url_for('posts.post_new'))

@bp.get('/edit/<int:post_id>')
@check_permissions("post_edit")
@login_required
def post_edit(post_id):
    post_to_edit = post.get_post(post_id)
    states = states_enum.enums
    return render_template('posts/edit_post.html', post=post_to_edit, states=states)

@bp.post('/update/<int:post_id>')
@check_permissions("post_update")
@login_required
def post_update(post_id):
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

    post.update_post(post_id, title, content, summary, state)
    flash('Publicación actualizada correctamente')
    return redirect(url_for('posts.post_edit', post_id=post_id))

@bp.get('/delete/<int:post_id>')
@check_permissions("post_delete")
@login_required
def post_delete(post_id):
    if post.delete_post(post_id):
        flash('Publicación eliminada correctamente')
    else:
        flash('Error al eliminar la publicación', 'error')

    return redirect(url_for('posts.post_index'))