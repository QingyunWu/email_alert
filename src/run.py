from src.app import app

__author__ = 'Qingyun Wu'

app.run(debug=app.config['DEBUG'], port=4990)
