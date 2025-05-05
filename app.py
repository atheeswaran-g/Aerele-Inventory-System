from aerele import create_app
from flask import session, redirect

app = create_app()

@app.route('/logout')
def logout():
    session.clear()  # Clear the session data
    return redirect('/login')  # Redirect to the login page

if __name__ == '__main__':
    app.run(debug=True)
