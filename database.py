from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Competition(db.Model):
    __tablename__ = 'competitions'

    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(200), nullable=False)
    category    = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    deadline    = db.Column(db.String(100))
    eligibility = db.Column(db.String(200))
    organizer   = db.Column(db.String(200))
    link        = db.Column(db.String(500))
    level       = db.Column(db.String(100))
    featured    = db.Column(db.Boolean, default=False)
    approved    = db.Column(db.Boolean, default=True)
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id':          self.id,
            'name':        self.name,
            'category':    self.category,
            'description': self.description,
            'deadline':    self.deadline,
            'eligibility': self.eligibility,
            'organizer':   self.organizer,
            'link':        self.link,
            'level':       self.level,
            'featured':    self.featured,
            'created_at':  self.created_at.isoformat(),
        }


class Submission(db.Model):
    __tablename__ = 'submissions'

    id           = db.Column(db.Integer, primary_key=True)
    name         = db.Column(db.String(200), nullable=False)
    category     = db.Column(db.String(50))
    description  = db.Column(db.Text)
    deadline     = db.Column(db.String(100))
    eligibility  = db.Column(db.String(200))
    link         = db.Column(db.String(500), nullable=False)
    organizer    = db.Column(db.String(200))
    submitted_by = db.Column(db.String(200))
    approved     = db.Column(db.Boolean, default=False)
    created_at   = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id':           self.id,
            'name':         self.name,
            'category':     self.category,
            'description':  self.description,
            'deadline':     self.deadline,
            'eligibility':  self.eligibility,
            'link':         self.link,
            'organizer':    self.organizer,
            'submitted_by': self.submitted_by,
            'approved':     self.approved,
            'created_at':   self.created_at.isoformat(),
        }


class Subscriber(db.Model):
    __tablename__ = 'subscribers'

    id         = db.Column(db.Integer, primary_key=True)
    email      = db.Column(db.String(200), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    active     = db.Column(db.Boolean, default=True)

    def to_dict(self):
        return {
            'id':         self.id,
            'email':      self.email,
            'created_at': self.created_at.isoformat(),
            'active':     self.active,
        }
