import datetime
import os
import random

import cv2
from flask import send_from_directory, make_response, url_for, request, jsonify

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



@app.route('/ckupload/', methods=['POST', 'OPTIONS'])
def ckupload():
    """CKEditor file upload"""
    error = ''
    url = ''
    rnd_name=''#新文件名
    # r=request
    # callback = request.args.get("CKEditorFuncNum")

    if request.method == 'POST' and 'upload' in request.files:
        fileobj = request.files['upload']
        fname, fext = os.path.splitext(fileobj.filename)#获取
        rnd_name = '%s%s' % (gen_rnd_filename(), fext)

        filepath = os.path.join(app.static_folder, 'upload', rnd_name)

        # 检查路径是否存在，不存在则创建
        dirname = os.path.dirname(filepath)
        if not os.path.exists(dirname):
            try:
                os.makedirs(dirname)
            except:
                error = 'ERROR_CREATE_DIR'
        elif not os.access(dirname, os.W_OK):
            error = 'ERROR_DIR_NOT_WRITEABLE'

        if not error:
            fileobj.save(filepath)
            url = url_for('static', filename='%s/%s' % ('upload', rnd_name))
    else:
        error = 'post error'
    if rnd_name!='' and url!='':
        #压缩图片
        relative_location='./static/upload/'+rnd_name
        compress_img(relative_location)

        res_dict={
            'fileName':rnd_name,
            'url':url,
            'uploaded':1
        }
    else:
        res_dict={
            'fileName':rnd_name,
            'url':url,
            'uploaded':0
        }

    response = jsonify(res_dict)
    response.headers["Content-Type"] = "text/html"
    return response

def gen_rnd_filename():
    filename_prefix = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    return '%s%s' % (filename_prefix, str(random.randrange(1000, 10000)))



def compress_img(relative_location):
    # 压缩代码
    img = cv2.imread(relative_location)
    sp = img.shape
    width_index = 1
    height_index = 0
    height = sp[height_index]
    width = sp[width_index]

    width_after = 600.0
    size_index = width / width_after
    height_after = int(height / size_index)

    res = cv2.resize(img, (int(width_after), height_after), interpolation=cv2.INTER_LINEAR)
    print('高度：' + str(height_after))
    print('宽度：' + str(width_after))
    cv2.imwrite(relative_location, res)