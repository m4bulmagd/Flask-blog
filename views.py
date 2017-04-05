from index import *
from models import *
from flask_login import login_user, current_user, login_required, logout_user


_categories = session.query(Categories)
_popular = session.query(Posts).order_by(Posts.post_id).limit(3)


@app.route('/')
def index():
    _posts = session.query(Posts, Users, Categories).filter(Posts.user_id == Users.user_id,
                                                            Posts.cat_id == Categories.cat_id)
    _posts = _posts.order_by(Posts.post_id.desc()).all()
    commentscount = session.query(Posts.post_id, Comments.comment_id).filter(Posts.post_id==Comments.post_id)
    commentscount = commentscount.group_by(Posts.post_id,Comments.comment_id)
    return render_template("blog.html", posts=_posts, categories=_categories, popular=_popular,commentscount = commentscount)

@app.route('/category/<cat_name>')
def cat_posts(cat_name):
    _posts = session.query(Posts, Users, Categories).filter(Posts.user_id == Users.user_id,
                                                            Posts.cat_id == Categories.cat_id,
                                                            Categories.cat_name == cat_name)
    _posts = _posts.order_by(Posts.post_id.desc())
    return render_template("blog.html", posts=_posts, categories=_categories, popular=_popular)


@app.route('/new')
@login_required
def newpost():
    return render_template("newpost.html", post="", categories=_categories, popular=_popular)


@app.route('/new', methods=["POST"])
@login_required
def showpost():
    markdown = mistune.Markdown(escape=False, hard_wrap=True)
    _postcontent = markdown(request.form["postcontent"])
    _post = Posts(title=request.form["posttitle"], content=_postcontent, user_id=current_user.user_id,
                  cat_id=request.form["category"])
    session.add(_post)
    session.commit()
    return redirect(url_for("view_post", id=_post.post_id))


@app.route("/post/<int:id>")
def view_post(id):
    _post = session.query(Posts, Users, Categories).filter(Posts.post_id == id, Posts.user_id == Users.user_id,
                                                           Posts.cat_id == Categories.cat_id)
    _post.markdown_content = mistune.markdown(_post[0][0].content)
    _related = session.query(Posts).filter(Posts.cat_id == _post[0][2].cat_id).order_by(func.random()).limit(3)
    _comments = session.query(Comments,Users).filter(Comments.post_id == id, Comments.user_id == Users.user_id)
    _comments = _comments.order_by(Comments.created.asc()).all()
    firsr_final = session.query(Posts.post_id).filter(Posts.post_id > id)

    return render_template("post.html", post=_post, categories=_categories, popular=_popular, related_post=_related,
                           _comments=_comments)


@app.route("/post/<int:id>/edit")
def edit_post(id):
    _post = session.query(Posts).get(id)
    if not current_user.is_authenticated:
        flash("login First to start edit you Post","edit_post_erorr")
        return redirect(url_for("view_post", id=_post.post_id))

    if current_user.user_id != _post.user_id:
        flash("you are not the owner for this post to edit it","edit_post_erorr")
        return redirect(url_for("view_post", id=_post.post_id))

    _post.markdown_content = mistune.markdown(_post.content)
    return render_template("newpost.html", post=_post, categories=_categories, popular=_popular)


@app.route("/post/<int:id>/edit", methods=["POST"])
@login_required
def update_post(id):
    markdown = mistune.Markdown(escape=False, hard_wrap=True)
    _postcontent = markdown(request.form["postcontent"])
    _post = session.query(Posts).filter(Posts.post_id == id).update(
        {"title": (request.form["posttitle"]), "content": (_postcontent), "cat_id": (request.form["category"])})
    session.commit()
    return redirect(url_for("view_post", id=id))


@app.route("/post/next/<int:id>")
def next_post(id):
    try:
        _post = session.query(Posts.post_id).filter(Posts.post_id > id)
        _post = _post.order_by(Posts.post_id.desc())
        return redirect(url_for("view_post", id=_post[0].post_id))
    except:
        return redirect(url_for("index"))


@app.route("/post/previous/<int:id>")
def previous_post(id):
    try:
        _post = session.query(Posts.post_id).filter(Posts.post_id < id)
        _post = _post.order_by(Posts.post_id.desc())
        return redirect(url_for("view_post", id=_post[0].post_id))
    except:
        return redirect(url_for("index"))


@app.route("/post/<int:id>/newcomment", methods=["POST"])
def add_comment(id):
    if not current_user.is_authenticated:
        flash("You Should login to Comment","comment_erorr")
        return redirect(url_for("view_post", id=id))
    _comment_content = request.form["comment"]
    _comment = Comments(content=_comment_content, post_id=id, user_id=current_user.user_id)
    session.add(_comment)
    session.commit()
    return redirect(url_for("view_post", id=id))


@app.route("/post/<int:id>/delete")
@login_required
def delete_post(id):
    _post = session.query(Posts).get(id)
    session.delete(_post)
    session.commit()
    return redirect(url_for("index"))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', categories=_categories, popular=_popular), 404


@app.route("/login", methods=["GET"])
def login_get():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login_post():
    username = request.form["username"]
    password = request.form["password"]
    _user = session.query(Users).filter_by(user_name=username).first()

    if not _user or not check_password_hash(_user.hash_pwd, password):
        flash("Incorrect username or password","login_erorr")
        return redirect(url_for("login_get"))

    login_user(_user)
    return redirect(url_for("index"))


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/signup", methods=["GET"])
def signup_get():
    return render_template("signup.html")


@app.route("/signup", methods=["POST"])
def signup_post():
    user_name = request.form["username"]
    if session.query(Users).filter_by(user_name=user_name).first():
        flash("User with that Username already exists","signup_erorr")
        return redirect(url_for("signup_get"))

    password = request.form["password"]
    while not password:
        password = getpass()

    hash_pwd = generate_password_hash(password)

    _user = Users(user_name=user_name, hash_pwd=hash_pwd, active=1,
                  full_name=request.form["fullname"])
    session.add(_user)

    session.commit()
    return redirect(url_for("index"))

