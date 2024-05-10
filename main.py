from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Video(name={self.name}, views={self.views}, likes={self.likes})"

db.create_all()

video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name", type=str, help="Video name", required=True)
video_put_args.add_argument("views", type=int, help="Views", required=True)
video_put_args.add_argument("likes", type=int, help="Likes", required=True)

def abort_if_video_exists(video_id):
    if VideoModel.query.filter_by(id=video_id).first():
        abort(409, message="Video already exists with that ID...")

class Video(Resource):
    def get(self, video_id):
        video = VideoModel.query.filter_by(id=video_id).first()
        if not video:
            abort(404, message="Video doesn't exist...")
        return video.__dict__, 200

    def put(self, video_id):
        abort_if_video_exists(video_id)
        args = video_put_args.parse_args()
        video = VideoModel(id=video_id, name=args['name'], views=args['views'], likes=args['likes'])
        db.session.add(video)
        db.session.commit()
        return video.__dict__, 201

    def delete(self, video_id):
        video = VideoModel.query.filter_by(id=video_id).first()
        if not video:
            abort(404, message="Video doesn't exist...")
        db.session.delete(video)
        db.session.commit()
        return '', 204

api.add_resource(Video, "/video/<int:video_id>")

if __name__ == "__main__":
    app.run(debug=True)
