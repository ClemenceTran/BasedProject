#from flask import redirect, url_for
#from app import create_app

#app = create_app()

#if __name__ == "__main__":
#    app.run(debug=True)
from dotenv import load_dotenv
load_dotenv()

from flask import redirect, url_for
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)