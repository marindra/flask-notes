from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Note


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    @app.cli.command('init-db')
    def init_db_command():
        db.create_all()
        print("Database initialized.")

    @app.route('/')
    def index():
        notes = Note.query.order_by(Note.id.desc()).all()
        return render_template('index.html', notes=notes)

    @app.route('/add', methods=['GET', 'POST'])
    def add():
        if request.method == 'POST':
            title = (request.form.get('title') or '').strip()
            text = (request.form.get('text') or '').strip()
            if not title or not text:
                flash('Заполни заголовок и текст.')
                return redirect(url_for('add'))
            db.session.add(Note(title=title, text=text))
            db.session.commit()
            flash('Заметка добавлена.')
            return redirect(url_for('index'))
        return render_template('add.html')

    @app.route('/delete/<int:note_id>', methods=['POST'])
    def delete(note_id):
        note = Note.query.get_or_404(note_id)
        db.session.delete(note)
        db.session.commit()
        flash('Заметка удалена.')
        return redirect(url_for('index'))

    return app


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)
