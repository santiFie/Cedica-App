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
from src.web.forms import NewPostForm
from src.core import post
from src.core.models.post import states_enum

bp = Blueprint('posts', __name__, url_prefix='/posts')

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