from sqlalchemy.sql import func

from .app import db


class Todo(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)

