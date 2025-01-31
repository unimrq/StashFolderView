import hashlib
import logging
import sqlite3
from datetime import timedelta, datetime, timezone
from utils import stash_query
import requests
import os
from flask import Flask, render_template, request, Response, jsonify, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from utils.folder_db_query import folder_status_process

# v3
app = Flask(__name__)
app.secret_key = 'stash-folder-view'
base_url = os.environ.get('base_url')
jump_url = os.environ.get('jump_url', base_url)
username = os.environ.get('username')
password = os.environ.get('password')
api_key = os.environ.get('api_key')
app.config['SESSION_COOKIE_NAME'] = 'stash-folder-view'
logged = False
network_status = 0  # 默认为内网模式

# 配置SQLite数据库
if not os.path.exists('data'):
    os.makedirs('data')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///folders.db'  # SQLite数据库文件
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 禁用信号跟踪（提高性能）
SESSION_TIMEOUT = timedelta(days=1)
headers = {
    'Content-Type': 'application/json',
    'ApiKey': api_key,
}
# 初始化SQLAlchemy
db = SQLAlchemy(app)
app.debug = True

@app.route('/image/<path:image_id>')
def get_image(image_id):
    # 图片的外部URL
    full_url = base_url + f"image/{image_id}/thumbnail"

    # 使用 requests 获取图片，携带cookie
    response = requests.get(full_url, headers=headers)

    if response.status_code == 200:
        # 返回获取的图片内容
        return Response(response.content, mimetype='images/jpeg')
    else:
        return "Failed to retrieve images", 404

@app.route('/scene/<path:scene_id>')
def get_scene(scene_id):
    # 图片的外部URL
    full_url = base_url + f"scene/{scene_id}/screenshot"

    # 使用 requests 获取图片，携带cookie
    response = requests.get(full_url, headers=headers)

    if response.status_code == 200:
        # 返回获取的图片内容
        return Response(response.content, mimetype='images/jpeg')
    else:
        return "Failed to retrieve images", 404

@app.route('/update_like_status', methods=['POST'])
def update_like_status():
    data = request.get_json()
    folder_id = data['folder_id']
    like_status = data['like_status']

    conn = sqlite3.connect('data/folders.db')
    cursor = conn.cursor()

    cursor.execute("UPDATE folders SET like_status = ? WHERE folder_id = ?", (like_status, folder_id))
    conn.commit()
    conn.close()

    return jsonify({'success': True})

@app.route('/update_read_status', methods=['POST'])
def update_read_status():
    data = request.get_json()
    folder_id = data['folder_id']
    read_status = data['read_status']

    # 连接数据库
    conn = sqlite3.connect('data/folders.db')
    cursor = conn.cursor()

    # 更新 read_status 字段
    cursor.execute("UPDATE folders SET read_status = ? WHERE folder_id = ?", (read_status, folder_id))
    conn.commit()
    conn.close()

    # 返回成功响应
    return jsonify({'success': True})

@app.route('/update_delete_status', methods=['POST'])
def update_delete_status():
    data = request.get_json()
    folder_id = data['folder_id']
    delete_status = data['delete_status']

    conn = sqlite3.connect('data/folders.db')
    cursor = conn.cursor()

    # 更新 delete_status
    cursor.execute("UPDATE folders SET delete_status = ? WHERE folder_id = ?", (delete_status, folder_id))
    conn.commit()
    conn.close()

    return jsonify({'success': True})


@app.route('/update_network_status', methods=['POST'])
def update_network_status():
    global network_status
    data = request.get_json()
    network_status = int(data['network_status'])
    # print("network_status", network_status)

    return jsonify({'success': True})

def generate_encrypted_string(username, password):
    combined_string = username + password
    encrypted_string = hashlib.sha256(combined_string.encode('utf-8')).hexdigest()  # 使用 SHA-256 加密
    return encrypted_string

def check_login():
    if 'logged_in' not in session or not session['logged_in']:
        # 如果没有登录，则重定向到登录页面
        return False
    else:
        logged_in = session['logged_in']
        if logged_in != generate_encrypted_string(username, password):
            return False

    # 获取登录时间，并确保它是带时区的时间对象
    login_time = session.get('login_time')

    if login_time:
        current_time = datetime.now(timezone.utc)  # 使用 UTC 时区的当前时间
        if abs(current_time - login_time) > SESSION_TIMEOUT:
            session.pop('logged_in', None)
            session.pop('login_time', None)
            return False
    return True

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()  # 获取前端发送的JSON数据
    usn = data.get('username')
    pwd = data.get('password')
    hashed = generate_encrypted_string(usn, pwd)
    # 验证用户名和密码
    if hashed == generate_encrypted_string(username, password):
        session['logged_in'] = hashed
        session['login_time'] = datetime.now(timezone.utc)  # 记录登录时间
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'message': 'Invalid username or password'})


@app.route('/')
def home():
    if check_login():
        return redirect(url_for('index'))
    return render_template('login.html')  # 返回登录页面

@app.route('/logout')
def logout():
    # 注销登录，清除 session
    session.pop('logged_in', None)
    session.pop('login_time', None)
    return redirect(url_for('home'))  # 重定向到登录页面

@app.route('/update_file_like_status', methods=['POST'])
def update_file_like_status():
    # 获取JSON数据
    data = request.get_json()

    file_id = data['file_id']
    rating = data['rating']
    is_video = data['is_video']
    # print(is_video)
    # print(rating)

    if is_video == "True":
        payload = {
            "query": "mutation { sceneUpdate(input: {id: " + file_id + ", rating100: " + rating + "}){rating100}}",
        }
    else:
        payload = {
            "query": "mutation { imageUpdate(input: {id: " + file_id + ", rating100: " + rating + "}){rating100}}",
        }

    # 发起GraphQL请求
    response = requests.post(base_url + 'graphql', headers=headers, json=payload)
    if response.ok:
        return jsonify(success=True)
    else:
        return jsonify(success=False, message='更新失败'), 400

@app.route('/folders', methods=['GET'])
def index():
    # 处理登录逻辑
    if not check_login():
        return redirect(url_for('home'))
    # 本页面参数
    folder_id = request.args.get('id')
    if not folder_id:
        folder_id = 'home'
    page = request.args.get('page', default=1, type=int)  # 当前页，默认第一页
    per_page = 50
    offset = (page - 1) * per_page  # 计算偏移量

    # 判断文件夹是否有子文件夹
    # folder_has_subfolders = has_subfolders(folder_id)
    parent_folder_id = 'home'
    # 查询z文件夹以及本文件夹路径
    folder_path, parent_folder_id = stash_query.find_directory_by_id(folder_id)
    if folder_id != 'home':

        folder_name = folder_path.split('/')[-1]
        # 查询子文件夹
        subdirectories = stash_query.find_subdirectory_by_id(folder_id)

        folder_has_subfolders = False if len(subdirectories) == 0 else True
        subdirectories.insert(0, {'folder_id': parent_folder_id, 'relative_path': '上一级'})
        root_folders = subdirectories
        # if folder_has_subfolders:
        #     subdirectories.insert(0, {'folder_id': parent_folder_id, 'relative_path': '上一级'})
        #     root_folders = subdirectories
        #     # print(root_folders)
        # else:
        #     root_folders = stash_query.find_subdirectory_by_id(parent_folder_id)
        #     root_folders.insert(0, {'folder_id': parent_folder_id, 'relative_path': '上一级'})
    else:
        folder_has_subfolders = True
        root_folders = stash_query.find_subdirectory_by_id(folder_id)
        # print(root_folders)
        root_folders.insert(0, {'folder_id': 'favorites', 'relative_path': '收藏', 'parent_folder_id': 'home'})
        folder_name = '根目录'

    # 获取当前路径的各个部分
    current_path_parts = []
    current_folder_id = folder_id
    count = 0
    while current_folder_id != 'home' and count < 5:
        folder_path, parent_folder_id = stash_query.find_directory_by_id(current_folder_id)
        relative_path = folder_path.split('/')[-1]
        if len(relative_path) > 15:
            relative_path = relative_path[:5] + "..." + relative_path[-5:]
        # print(relative_path)
        # relative_path += '/'
        if parent_folder_id != 'home':
            current_path_parts.insert(0, (relative_path, current_folder_id))
            current_folder_id = parent_folder_id
        else:
            current_path_parts.insert(0, (relative_path, current_folder_id))
            break
        count += 1
    if count < 5:
        current_path_parts.insert(0, ('根目录', 'home'))
    else:
        current_path_parts.insert(0, ('根目录...', 'home'))
    # if len(current_path_parts) > 2:
    #     current_path_parts = current_path_parts[-3:0]
    # if folder_id:
    #     folder_path, parent_folder_id = stash_query.find_directory_by_id(folder_id)
    # print(parent_folder_id)
    # print("current_path" + str(current_path_parts))

    # 收藏
    if folder_id:
        if folder_id == 'favorite_files':
            # print("Im in folder_id 2")
            file_ids = stash_query.get_favorite_files(int(per_page / 2), int(offset / 2))
            total_files = stash_query.get_favorite_num()
            total_pages = (total_files // per_page) + (1 if total_files % per_page > 0 else 0)
            all_urls = []
            for scene_id in file_ids[1]:
                scene_url = f"/scene/{scene_id}"
                if network_status == 0:
                    scene_link = base_url + f"scenes/{scene_id}"
                else:
                    scene_link = jump_url + f"scenes/{scene_id}"
                # scene_title, scene_rating = get_scene_status(scene_id)
                scene_rating = stash_query.get_file_status(scene_id, True)
                all_urls.append((scene_url, scene_link, True, scene_id, scene_rating))
            for image_id in file_ids[0]:
                image_url = f"/image/{image_id}"
                if network_status == 0:
                    image_link = base_url + f"images/{image_id}"
                else:
                    image_link = jump_url + f"images/{image_id}"
                # image_title, image_rating = get_image_status(image_id)
                image_rating = stash_query.get_file_status(image_id, False)
                all_urls.append((image_url, image_link, False, image_id, image_rating))
        # 获取该文件夹下的所有文件ID（分页）
        elif folder_id == 'favorites' or folder_id == 'favorite_folders' or folder_id == 'home':
            all_urls = []
            total_pages = 0
        else:
            file_ids = stash_query.find_file_id_by_folder_id(folder_id, per_page, offset)
            total_files = stash_query.find_file_num_by_folder_id(folder_id)
            total_pages = (total_files // per_page) + (1 if total_files % per_page > 0 else 0)
            all_urls = []
            for file_id in file_ids:
                content_id, is_video = stash_query.find_image_id_or_scene_id_by_file_id(file_id)

                if not is_video:
                    image_url = f"/image/{content_id}"
                    if network_status == 0:
                        image_link = base_url + f"images/{content_id}"
                    else:
                        image_link = jump_url + f"images/{content_id}"
                    image_rating = stash_query.get_file_status(content_id, is_video)
                    all_urls.append((image_url, image_link, is_video, content_id, image_rating))
                else:
                    scene_url = f"/scene/{content_id}"
                    if network_status == 0:
                        scene_link = base_url + f"scenes/{content_id}"
                    else:
                        scene_link = jump_url + f"scenes/{content_id}"
                    scene_rating = stash_query.get_file_status(content_id, is_video)
                    all_urls.append((scene_url, scene_link, is_video, content_id, scene_rating))
    else:
        all_urls = []
        total_pages = 0

    # 辅助变量
    folder_has_medias = len(all_urls) > 0

    folder_details = folder_status_process(folder_id, root_folders, folder_has_subfolders)
    # print(folder_details)
    # print(root_folders)
    return render_template('index.html', root_folders=root_folders,
                           folder_id=folder_id, folder_details=folder_details,
                           current_path_parts=current_path_parts, network_status = network_status,
                           all_urls=all_urls, parent_folder_id=parent_folder_id,
                           page=page, total_pages=total_pages, folder_name=folder_name,
                           folder_has_subfolders=folder_has_subfolders,
                           folder_has_medias=folder_has_medias, base_url=base_url)


if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

# 启动Flask应用
if __name__ == '__main__':
    # app.debug = True
    app.run(host='0.0.0.0', port=8000)
