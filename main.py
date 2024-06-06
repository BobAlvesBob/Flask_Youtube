from flask import Flask, request, render_template, redirect
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Video(name={self.name}, views={self.views}, likes={self.likes})"

# Outras definições de rotas e classes podem ir aqui

@app.route('/')
def index():
    videos = VideoModel.query.all()  # Pega todos os vídeos do banco de dados
    print(videos)  # Isto deve mostrar os objetos Video no console
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
        return redirect('/')  # Redireciona para a página inicial após adicionar
    
@app.route('/add')
def add():
    return render_template('add.html')

@app.route('/credits')
def credits():
    return render_template('credits.html')

# Certifique-se de que o app.run() esteja no final do arquivo
if __name__ == "__main__":
    app.run(debug=True)
