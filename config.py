import os

class Config: 
    FLASK_APP=os.environ.get("FLASK_APP")
    FLASK_DEBUG=os.environ.get("FLASK_DEBUG")
    SECRET_KEY=os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI="postgresql://winvrdke:WnA8h655SRUqIme48bHcNcMhE73BaCH4@suleiman.db.elephantsql.com/winvrdke"
    SQLALCHEMY_TRACK_MODIFICATIONS=False 