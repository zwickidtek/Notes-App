# app.py
from contains import app, db

# Will start wsgi app by running this script
if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
