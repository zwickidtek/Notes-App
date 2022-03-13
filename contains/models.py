from contains import db
from datetime import datetime


# Deserialize datetime object into string form for JSON processing.
def dump_datetime(value):
    if value is None:
        return None
    return [value.strftime("%Y-%m-%d"), value.strftime("%H:%M:%S")]


class Note(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    text = db.Column(db.String(240), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())

    # change the datetime class stored in db to Month day format
    @property
    def prettierTime(self):
        tmpString = self.created_at.strftime(f"%b %d   %I:%m%p")
        print(tmpString)
        return tmpString

    # Return note data in easily serializable format
    @property
    def serialize(self):
        return {
            'id': self.id,
            'created_at': dump_datetime(self.created_at),
            'text': self.text
        }