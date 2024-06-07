from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class VideoModel(db.Model):
    __tablename__ = 'video_model'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    video_id = db.Column(db.Integer, db.ForeignKey('video_model.id'), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=False)
    upvotes = db.Column(db.Integer, default=0)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

class VideoVote(db.Model):
    __tablename__ = 'video_votes'
    id = db.Column(db.Integer, primary_key=True)
    video_id = db.Column(db.Integer, db.ForeignKey('video_model.id'), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    vote = db.Column(db.Integer, nullable=False)  # 1 para upvote, -1 para downvote

@app.route('/')
def index():
    videos = VideoModel.query.all()
    return render_template('index.html', videos=videos)

@app.route('/add_video', methods=['POST'])
def add_video():
    if request.method == 'POST':
        video_name = request.form['name']
        video_views = request.form['views']
        video_likes = request.form['likes']
        new_video = VideoModel(name=video_name, views=video_views, likes=video_likes)
        db.session.add(new_video)
        db.session.commit()
        return redirect('/')
    
@app.route('/add')
def add():
    return render_template('add.html')

@app.route('/credits')
def credits():
    return render_template('credits.html')

@app.route('/video/<int:video_id>')
def video(video_id):
    video = VideoModel.query.get(video_id)
    if not video:
        return 'Vídeo não encontrado', 404

    video.views += 1
    db.session.commit()
    
    comments = Comment.query.filter_by(video_id=video_id).all()
    upvotes = sum(1 for vote in VideoVote.query.filter_by(video_id=video_id, vote=1))
    downvotes = sum(1 for vote in VideoVote.query.filter_by(video_id=video_id, vote=-1))

    return render_template('video.html', video=video, comments=comments, upvotes=upvotes, downvotes=downvotes)

@app.route('/add_comment/<int:video_id>', methods=['POST'])
def add_comment(video_id):
    user_id = request.form['user_id']
    comment_text = request.form['comment']
    comment = Comment(video_id=video_id, user_id=user_id, comment=comment_text)
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('video', video_id=video_id))

@app.route('/vote/<int:video_id>', methods=['POST'])
def vote(video_id):
    user_id = request.form['user_id']
    vote_type = int(request.form['vote'])
    vote = VideoVote(video_id=video_id, user_id=user_id, vote=vote_type)
    db.session.add(vote)
    db.session.commit()
    return redirect(url_for('video', video_id=video_id))

if __name__ == "__main__":
    app.run(debug=True)
