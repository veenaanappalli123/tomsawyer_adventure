from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database configuration (SQLite)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nahb.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
class Story(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default="draft")  # draft / published / suspended
    start_page_id = db.Column(db.Integer, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "start_page_id": self.start_page_id
        }
class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    story_id = db.Column(db.Integer, db.ForeignKey('story.id'), nullable=False)
    text = db.Column(db.Text, nullable=False)
    is_ending = db.Column(db.Boolean, default=False)
    ending_label = db.Column(db.String(100), nullable=True)

    story = db.relationship('Story', backref=db.backref('pages', lazy=True))

    def to_dict(self):
        return {
            "id": self.id,
            "story_id": self.story_id,
            "text": self.text,
            "is_ending": self.is_ending,
            "ending_label": self.ending_label
        }
class Choice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    page_id = db.Column(db.Integer, db.ForeignKey('page.id'), nullable=False)
    text = db.Column(db.String(200), nullable=False)
    next_page_id = db.Column(db.Integer, nullable=False)

    page = db.relationship('Page', backref=db.backref('choices', lazy=True))

    def to_dict(self):
        return {
            "id": self.id,
            "page_id": self.page_id,
            "text": self.text,
            "next_page_id": self.next_page_id
        }
    
@app.route("/api/stories", methods=["POST"])
def create_story():
    data = request.get_json()

    new_story = Story(
        title=data.get("title"),
        description=data.get("description"),
        status=data.get("status", "draft"),
        start_page_id=data.get("start_page_id")
    )

    db.session.add(new_story)
    db.session.commit()

    return jsonify(new_story.to_dict()), 201


@app.route("/api/stories", methods=["GET"])
def get_stories():
    stories = Story.query.all()
    return jsonify([story.to_dict() for story in stories])

@app.route("/api/stories/<int:story_id>/pages", methods=["POST"])
def create_page(story_id):
    data = request.get_json()

    new_page = Page(
        story_id=story_id,
        text=data.get("text"),
        is_ending=data.get("is_ending", False),
        ending_label=data.get("ending_label")
    )

    db.session.add(new_page)
    db.session.commit()

    return jsonify(new_page.to_dict()), 201

@app.route("/api/pages/<int:page_id>", methods=["GET"])
def get_page(page_id):
    page = Page.query.get_or_404(page_id)

    page_data = page.to_dict()
    page_data["choices"] = [choice.to_dict() for choice in page.choices]

    return jsonify(page_data)

    

@app.route("/api/pages/<int:page_id>/choices", methods=["POST"])
def create_choice(page_id):
    data = request.get_json()

    new_choice = Choice(
        page_id=page_id,
        text=data.get("text"),
        next_page_id=data.get("next_page_id")
    )

    db.session.add(new_choice)
    db.session.commit()

    return jsonify(new_choice.to_dict()), 201

@app.route("/api/choices/<int:choice_id>", methods=["DELETE"])
def delete_choice(choice_id):
    choice = Choice.query.get_or_404(choice_id)
    db.session.delete(choice)
    db.session.commit()
    return jsonify({"message": "Choice deleted"})


# Test route
@app.route("/api/status")
def status():
    return jsonify({
        "service": "Flask API",
        "status": "running with database"
    })

if __name__ == "__main__":
    app.run(debug=True)
