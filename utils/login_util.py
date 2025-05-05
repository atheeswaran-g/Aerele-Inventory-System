from functools import wraps

def login_required(view_func):
    @wraps(view_func)
    def wrapped_view(**kwargs):
        if 'user_id' not in session:
            flash('You must be logged in to view this page.', 'warning')
            return redirect(url_for('main.login'))
        return view_func(**kwargs)
    return wrapped_view
