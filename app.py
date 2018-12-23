import os

from api.create import create_app
OS_PATH = os.path.dirname(__file__)
if __name__ == '__main__':
    app=create_app()
    app.run()
