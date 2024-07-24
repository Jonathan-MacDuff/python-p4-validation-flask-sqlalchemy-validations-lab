from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('name', 'phone_number')
    def validate_author(self, key, data):
        if key == 'name':
            if len(data) == 0:
                raise ValueError("Name must not be blank")
            else:
                for n in Author.query.all():
                    if n.name == data:
                        raise ValueError("Name must be unique")
        elif key == 'phone_number':
            if len(data) != 10:
                raise ValueError("Phone number must be 10 digits")
            else:
                for char in data:
                    if not char.isdigit():
                        raise ValueError("Phone number must not include any non-integer characters")
        return data

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('title', 'content', 'category', 'summary')
    def validate_post(self, key, data):
        if key == 'title':
            if not ("Won't Believe" in data or "Secret" in data or "Top" in data or "Guess" in data):
                raise ValueError("Title must conatain clickbait")
        elif key == 'content':
            if len(data) < 250:
                raise ValueError("Content must be at least 250 characters")
        elif key == 'category':
            if not (data == "Fiction" or data == "Non-Fiction"):
                raise ValueError("Category must be Fiction or Non-Fiction")
        elif key == 'summary':
            if len(data) > 250:
                raise ValueError("Summary must be no more than 250 characters")
        return data


    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
