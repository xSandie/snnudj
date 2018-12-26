import os

from flask import send_from_directory

from api.create import create_app

OS_PATH = os.path.dirname(__file__)
# OS_PATH=os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

app=create_app()

if __name__ == '__main__':

    app.run()

@app.route('/static/<my_dir>/<filename>',methods=['GET'])
def get_image(my_dir,filename):
    print("get img")
    return send_from_directory(OS_PATH+'/static/'+my_dir,filename)


