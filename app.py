import sqlite3
from datetime import timedelta, datetime, timezone

import requests
import os
from flask import Flask, render_template, request, Response, jsonify, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# v3
app = Flask(__name__)
app.secret_key = 'stash-folder-view'
base_url = os.environ.get('base_url')
username = os.environ.get('username')
password = os.environ.get('password')
api_key = os.environ.get('api_key')
app.config['SESSION_COOKIE_NAME'] = 'stash-folder-view'
logged = False

# 配置SQLite数据库
if not os.path.exists('data'):
    os.makedirs('data')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///folders.db'  # SQLite数据库文件
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 禁用信号跟踪（提高性能）
SESSION_TIMEOUT = timedelta(minutes=30)
headers = {
    'Content-Type': 'application/json',
    'ApiKey': api_key,
}
# 初始化SQLAlchemy
db = SQLAlchemy(app)


# 获取某个目录的子目录
def get_folders_from_db(folder_id=None):
    conn = sqlite3.connect('stash-go.sqlite')
    cursor = conn.cursor()

    if folder_id is None:
        cursor.execute("SELECT id, path, parent_folder_id FROM folders WHERE parent_folder_id IS NULL")
    else:
        cursor.execute("SELECT id, path, parent_folder_id FROM folders WHERE parent_folder_id = ?", (folder_id,))

    rows = cursor.fetchall()
    conn.close()

    folders = []
    for row in rows:
        folder_id, folder_path, parent_folder_id = row
        folders.append({
            'folder_id': folder_id,
            'folder_path': folder_path,
            'parent_folder_id': parent_folder_id,
            'relative_path': folder_path.split('/')[-1]
        })

    return folders


# 根据parent_folder_id获取该文件夹下的所有文件id
def get_file_ids_from_folder(folder_id, offset=0, limit=50):
    conn = sqlite3.connect('stash-go.sqlite')
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM files WHERE parent_folder_id = ? LIMIT ? OFFSET ?", (folder_id, limit, offset))
    file_ids = cursor.fetchall()
    conn.close()
    return [file_id[0] for file_id in file_ids]


# 获取某个文件夹是否有子文件夹
def has_subfolders(folder_id):
    conn = sqlite3.connect('stash-go.sqlite')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM folders WHERE parent_folder_id = ?", (folder_id,))
    subfolder_count = cursor.fetchone()[0]
    conn.close()
    return subfolder_count > 0


# 根据文件id获取image_id和scene_id
def get_image_and_scene_ids(file_id):
    conn = sqlite3.connect('stash-go.sqlite')
    cursor = conn.cursor()
    cursor.execute("SELECT image_id FROM images_files WHERE file_id = ?", (file_id,))
    image_id = cursor.fetchone()

    cursor.execute("SELECT scene_id FROM scenes_files WHERE file_id = ?", (file_id,))
    scene_id = cursor.fetchone()

    conn.close()

    # 判断文件是否为视频：只要有scene_id就认为是视频
    is_video = bool(scene_id)

    return image_id[0] if image_id else None, scene_id[0] if scene_id else None, is_video


def get_image_status(image_id):
    conn = sqlite3.connect('stash-go.sqlite')
    cursor = conn.cursor()
    cursor.execute("SELECT title, rating FROM images WHERE id = ?", (image_id,))
    image_status = cursor.fetchone()
    conn.close()
    return image_status[0], image_status[1]


def get_scene_status(scene_id):
    conn = sqlite3.connect('stash-go.sqlite')
    cursor = conn.cursor()
    cursor.execute("SELECT title, rating FROM scenes WHERE id = ?", (scene_id,))
    scene_status = cursor.fetchone()
    conn.close()
    return scene_status[0], scene_status[1]


@app.route('/image/<path:image_id>')
async def get_image(image_id):
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
async def get_scene(scene_id):
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


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()  # 获取前端发送的JSON数据
    usn = data.get('username')
    pwd = data.get('password')

    # 验证用户名和密码
    if usn == username and pwd == password:
        session['logged_in'] = True
        session['login_time'] = datetime.now(timezone.utc)  # 记录登录时间
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'message': 'Invalid username or password'})


def check_login():
    if 'logged_in' not in session or not session['logged_in']:
        # 如果没有登录，则重定向到登录页面
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


def get_favorite_files(offset, per_page):
    conn = sqlite3.connect('stash-go.sqlite')
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM images WHERE rating >= 80 ORDER BY RANDOM()  LIMIT ? OFFSET ?", (per_page, offset))
    images_id = cursor.fetchall()
    cursor.execute("SELECT id FROM scenes WHERE rating >= 80 ORDER BY RANDOM()  LIMIT ? OFFSET ?", (per_page, offset))
    scenes_id = cursor.fetchall()
    conn.close()
    return [file_id[0] for file_id in images_id], [file_id[0] for file_id in scenes_id]


@app.route('/update_file_like_status', methods=['POST'])
def update_file_like_status():
    # 获取JSON数据
    data = request.get_json()

    file_id = data['file_id']
    rating = data['rating']
    is_video = data['is_video']

    if bool(is_video):
        payload = {
            "query": "mutation { sceneUpdate(input: {id: " + file_id + ", rating100: " + rating + "}){rating100}}",
        }
    else:
        payload = {
            "query": "mutation { imageUpdate(input: {id: " + file_id + ", rating100: " + rating + "}){rating100}}",
        }

    # 发起GraphQL请求
    response = requests.post(base_url + 'graphql', headers=headers, json=payload)
    # print(response.status_code)
    # print(response.json())
    if response.ok:
        return jsonify(success=True)
    else:
        return jsonify(success=False, message='更新失败'), 400


@app.route('/folders', methods=['GET'])
def index():
    if not check_login():
        return redirect(url_for('home'))

    folder_id = request.args.get('id', type=int)
    page = request.args.get('page', default=1, type=int)  # 当前页，默认第一页
    per_page = 50  # 每页显示的文件数量
    offset = (page - 1) * per_page  # 计算偏移量

    # 判断文件夹是否有子文件夹
    folder_has_subfolders = has_subfolders(folder_id)

    # 获取父目录的路径
    parent_folder_id = None
    if folder_id:
        cursor = sqlite3.connect('stash-go.sqlite').cursor()
        cursor.execute("SELECT parent_folder_id FROM folders WHERE id = ?", (folder_id,))
        parent_folder_id = cursor.fetchone()[0]
    else:
        folder_has_subfolders = True

    if folder_has_subfolders:
        # 获取文件夹结构
        root_folders = get_folders_from_db(folder_id)
    else:
        root_folders = get_folders_from_db(parent_folder_id)

    # 获取当前路径的各个部分
    current_path_parts = []
    current_folder_id = folder_id
    while current_folder_id:
        cursor = sqlite3.connect('stash-go.sqlite').cursor()
        cursor.execute("SELECT path, parent_folder_id FROM folders WHERE id = ?", (current_folder_id,))
        folder = cursor.fetchone()
        if folder:
            current_path_parts.insert(0, (folder[0], current_folder_id))
            current_folder_id = folder[1]
        else:
            break

    # 获取该文件夹下的所有文件ID（分页）
    if parent_folder_id is not None:
        file_ids = get_file_ids_from_folder(folder_id, offset, per_page)
        all_urls = []
        for file_id in file_ids:
            image_id, scene_id, is_video = get_image_and_scene_ids(file_id)
            # print(image_id, scene_id, is_video)
            if image_id:
                image_url = f"/image/{image_id}"
                image_link = base_url + f"images/{image_id}"
                image_title, image_rating = get_image_status(image_id)
                # print(image_title, image_rating)
                all_urls.append((image_url, image_link, is_video, image_id, image_rating))

            if scene_id:
                scene_url = f"/scene/{scene_id}"
                scene_link = base_url + f"scenes/{scene_id}"
                scene_title, scene_rating = get_scene_status(scene_id)
                all_urls.append((scene_url, scene_link, is_video, scene_id, scene_rating))
    else:
        files_ids = get_favorite_files(offset, per_page)
        all_urls = []
        for image_id in files_ids[0]:
            image_url = f"/image/{image_id}"
            image_link = base_url + f"images/{image_id}"
            image_title, image_rating = get_image_status(image_id)
            all_urls.append((image_url, image_link, False, image_id, image_rating))
        for scene_id in files_ids[1]:
            scene_url = f"/scene/{scene_id}"
            scene_link = base_url + f"scenes/{scene_id}"
            scene_title, scene_rating = get_scene_status(scene_id)
            all_urls.append((scene_url, scene_link, True, scene_id, scene_rating))

    if len(all_urls) == 0:
        folder_has_medias = False
    else:
        folder_has_medias = True

    # 文件夹状态处理
    folder_details = {}
    conn1 = sqlite3.connect('data/folders.db')
    cursor = conn1.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS folders (
        folder_id INTEGER PRIMARY KEY,
        read_status INTEGER CHECK (read_status IN (0, 1)),
        like_status INTEGER CHECK (like_status IN (0, 1)),
        delete_status INTEGER CHECK (delete_status IN (0, 1))
    )
    ''')

    # cursor.execute("PRAGMA table_info(folders)")
    # columns = [column[1] for column in cursor.fetchall()]
    #
    # if 'delete_status' not in columns:
    #     cursor.execute('''
    #         ALTER TABLE folders
    #         ADD COLUMN delete_status INTEGER CHECK (delete_status IN (0, 1)) DEFAULT 0
    #         ''')
    #     print("Column 'delete_status' added.")
    # else:
    #     print("Column 'delete_status' already exists.")

    # 处理 root_folders 中的每个文件夹
    for folder in root_folders:
        subfolder_id = folder['folder_id']
        cursor.execute("SELECT read_status, like_status, delete_status FROM folders WHERE folder_id = ?",
                       (subfolder_id,))
        folder_data = cursor.fetchone()

        # 如果 folder_data 为 None，则插入新数据
        if not folder_data:
            cursor.execute(
                "INSERT INTO folders (folder_id, read_status, like_status, delete_status) VALUES (?, ?, ?, ?)",
                (subfolder_id, 0, 0, 0))
            folder_details[subfolder_id] = {'read_status': 0, 'like_status': 0, 'delete_status': 0}
        else:
            folder_details[subfolder_id] = {
                'read_status': folder_data[0],
                'like_status': folder_data[1],
                'delete_status': folder_data[2]
            }

    if not folder_has_subfolders:
        cursor.execute("UPDATE folders SET read_status = 1 WHERE folder_id = ?", (folder_id,))

    # 查询当前 folder_id 的状态，如果没有数据则插入一条新数据
    cursor.execute("SELECT read_status, like_status, delete_status FROM folders WHERE folder_id = ?", (folder_id,))
    folder_data = cursor.fetchone()
    # 如果 folder_data 为 None，则插入新数据
    if not folder_data:
        cursor.execute("INSERT INTO folders (folder_id, read_status, like_status, delete_status) VALUES (?, ?, ?, ?)",
                       (folder_id, 0, 0, 0))
        folder_details[folder_id] = {'read_status': 1, 'like_status': 0, 'delete_status': 0}
    else:
        folder_details[folder_id] = {
            'read_status': folder_data[0],
            'like_status': folder_data[1],
            'delete_status': folder_data[2]
        }
    # print(folder_details[folder_id])
    # 提交更改并关闭连接
    conn1.commit()
    conn1.close()

    # 获取总的文件数量，用于计算总页数
    conn = sqlite3.connect('stash-go.sqlite')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM files WHERE parent_folder_id = ?", (folder_id,))
    total_files = cursor.fetchone()[0]
    conn.close()

    total_pages = (total_files // per_page) + (1 if total_files % per_page > 0 else 0)

    return render_template('index.html', root_folders=root_folders,
                           folder_id=folder_id, folder_details=folder_details,
                           current_path_parts=current_path_parts,
                           all_urls=all_urls, parent_folder_id=parent_folder_id,
                           page=page, total_pages=total_pages,
                           folder_has_subfolders=folder_has_subfolders,
                           folder_has_medias=folder_has_medias, base_url=base_url)


# 启动Flask应用
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
