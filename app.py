# app.py
from contains import app

# Will start wsgi app by running this script
if __name__ == '__main__':
    app.run(debug=True)