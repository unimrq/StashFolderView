import sqlite3


def folder_status_process(folder_id, root_folders, folder_has_subfolders):
    # 文件夹状态处理
    folder_details = {}
    conn1 = sqlite3.connect('data/folders.db')
    cursor = conn1.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS folders (
            folder_id TEXT PRIMARY KEY,
            read_status INTEGER CHECK (read_status IN (0, 1)),
            like_status INTEGER CHECK (like_status IN (0, 1)),
            delete_status INTEGER CHECK (delete_status IN (0, 1))
        )
        ''')

    # cursor.execute('''
    #     CREATE TABLE IF NOT EXISTS new_folders (
    #         folder_id TEXT PRIMARY KEY,
    #         read_status INTEGER CHECK (read_status IN (0, 1)),
    #         like_status INTEGER CHECK (like_status IN (0, 1)),
    #         delete_status INTEGER CHECK (delete_status IN (0, 1))
    #     )
    # ''')
    #
    # # 复制数据到新表
    # cursor.execute('''
    #     INSERT INTO new_folders (folder_id, read_status, like_status, delete_status)
    #     SELECT folder_id, read_status, like_status, delete_status FROM folders
    # ''')
    #
    # # 删除原表
    # cursor.execute('DROP TABLE folders')
    #
    # # 重命名新表为原表名称
    # cursor.execute('ALTER TABLE new_folders RENAME TO folders')

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

    # 处理子文件夹的已读状态
    read_status = True
    # print(root_folders[1:])
    subfolder_id = root_folders[0]['folder_id']
    cursor.execute("SELECT read_status, like_status, delete_status FROM folders WHERE folder_id = ?",
                   (subfolder_id,))
    folder_data = cursor.fetchone()
    folder_details[subfolder_id] = {
        'read_status': folder_data[0],
        'like_status': folder_data[1],
        'delete_status': folder_data[2]
    }
    for folder in root_folders[1:]:
        subfolder_id = folder['folder_id']
        cursor.execute("SELECT read_status, like_status, delete_status FROM folders WHERE folder_id = ?",
                       (subfolder_id,))
        folder_data = cursor.fetchone()

        # 如果 folder_data 为 None，则插入新数据
        if not folder_data:
            read_status = read_status and False
            cursor.execute(
                "INSERT INTO folders (folder_id, read_status, like_status, delete_status) VALUES (?, ?, ?, ?)",
                (subfolder_id, 0, 0, 0))
            folder_details[subfolder_id] = {'read_status': 0, 'like_status': 0, 'delete_status': 0}
        else:
            read_status = read_status and bool(int(folder_data[0]))
            folder_details[subfolder_id] = {
                'read_status': folder_data[0],
                'like_status': folder_data[1],
                'delete_status': folder_data[2]
            }

    # 查询当前 folder_id 的状态，如果没有数据则插入一条新数据
    cursor.execute("SELECT read_status, like_status, delete_status FROM folders WHERE folder_id = ?", (folder_id,))
    folder_data = cursor.fetchone()
    # print(read_status)
    # 如果 folder_data 为 None，则插入新数据
    if not folder_data:
        if read_status:
            cursor.execute(
                "INSERT INTO folders (folder_id, read_status, like_status, delete_status) VALUES (?, ?, ?, ?)",
                (folder_id, 1, 0, 0))
            folder_details[folder_id] = {'read_status': 1, 'like_status': 0, 'delete_status': 0}
        else:
            cursor.execute("INSERT INTO folders (folder_id, read_status, like_status, delete_status) VALUES (?, ?, ?, ?)",
                           (folder_id, 0, 0, 0))
            folder_details[folder_id] = {'read_status': 0, 'like_status': 0, 'delete_status': 0}
    else:
        # 如果没有子文件夹则更新状态为已读
        if read_status:
            cursor.execute("UPDATE folders SET read_status = 1 WHERE folder_id = ?", (folder_id,))
            folder_details[folder_id] = {
                'read_status': 1,
                'like_status': folder_data[1],
                'delete_status': folder_data[2]
            }
        else:
            folder_details[folder_id] = {
                'read_status': folder_data[0],
                'like_status': folder_data[1],
                'delete_status': folder_data[2]
            }
    # print(folder_details[folder_id])
    # print(folder_details)
    # 提交更改并关闭连接
    conn1.commit()
    conn1.close()
    return folder_details
