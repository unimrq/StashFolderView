import requests
import os

base_url = os.environ.get('base_url')
api_url = base_url + 'graphql'
api_key = os.environ.get('api_key')

headers = {
    'Content-Type': 'application/json',
    'ApiKey': api_key,
}


def find_images_by_rating(page, per_page, ):
    json = {
        "query": f"query{{ "
                 f"findImages("
                 f"filter:{{page:{page}, per_page:{per_page}, sort:}}, "
                 f"image_filter:{{rating100:{{value:100, modifier:EQUALS}}}})"
                 f"{{count images{{id}}}}"
                 f"}}"
    }
    response = requests.post(api_url, headers=headers, json=json)
    if response.status_code == 200:
        # print(response.json())
        return [item['id'] for item in response.json()['data']['findImages']['images']]
    else:
        return None


def find_scenes_by_rating(page, per_page, ):
    json = {
        "query": f"query{{ "
                 f"findScenes("
                 f"filter:{{page:{page}, per_page:{per_page}}}, "
                 f"scene_filter:{{rating100:{{value:100, modifier:EQUALS}}}})"
                 f"{{count scenes{{id}}}}"
                 f"}}"
    }
    response = requests.post(api_url, headers=headers, json=json)
    if response.status_code == 200:
        # print(response.json())
        return [item['id'] for item in response.json()['data']['findScenes']['scenes']]
    else:
        return None


def find_images_by_path(page, per_page, path):
    json = {
        "query": f"query{{ "
                 f"findImages("
                 f"filter:{{page:{page}, per_page:{per_page}}}, "
                 f"image_filter:{{path:{{value:\"{path}\", modifier:INCLUDES}}}})"
                 f"{{count images{{id rating100}}}}"
                 f"}}"
    }
    response = requests.post(api_url, headers=headers, json=json)
    if response.status_code == 200:
        # print(response.json())
        return response.json()['data']['findImages']
    else:
        return None


def find_scenes_by_path(page, per_page, path):
    json = {
        "query": f"query{{ "
                 f"findScenes("
                 f"filter:{{page:{page}, per_page:{per_page}}}, "
                 f"scene_filter:{{path:{{value:\"{path}\", modifier:INCLUDES}}}})"
                 f"{{count scenes{{id rating100}}}}"
                 f"}}"
    }
    response = requests.post(api_url, headers=headers, json=json)
    if response.status_code == 200:
        print(response.json()['data']['findScenes'])
        return response.json()['data']['findScenes']
    else:
        return None


def find_directory_by_path(path):
    json = {
        "query": f"query{{ directory(path:\"{path}\") {{ path parent directories}} }}"
    }
    response = requests.post(api_url, headers=headers, json=json)
    # print(response.json())
    if response.status_code == 200:
        return response.json()['data']['directory']
    else:
        return None


def find_directory_by_id(folder_id):
    json = {
        "query": f"""
                mutation {{
                  querySQL(
                    sql: \"SELECT path, parent_folder_id FROM folders WHERE id = {folder_id};\"
                  ) {{
                    columns
                    rows
                  }}
                }}
                """
    }
    response = requests.post(api_url, headers=headers, json=json)
    # print(response.json())
    if response.status_code == 200:
        return response.json()['data']['querySQL']['rows'][0]
    else:
        return None


def find_subdirectory_by_id(folder_id=None):
    if folder_id is None:
        json = {
            "query": f"""
                    mutation {{
                      querySQL(
                        sql: \"SELECT id, path, parent_folder_id FROM folders WHERE parent_folder_id IS NULL;\"
                      ) {{
                        columns
                        rows
                      }}
                    }}
                    """
        }
    else:
        json = {
            "query": f"""
                    mutation {{
                      querySQL(
                        sql: \"SELECT id, path, parent_folder_id FROM folders WHERE parent_folder_id = {folder_id};\"
                      ) {{
                        columns
                        rows
                      }}
                    }}
                    """
        }
    response = requests.post(api_url, headers=headers, json=json)
    # print(response.text)
    # print(response.status_code)

    if response.status_code == 200:
        folders = []
        rows = response.json()['data']['querySQL']['rows']
        for row in rows:
            folder_id, folder_path, parent_folder_id = row
            folders.append({
                'folder_id': folder_id,
                'folder_path': folder_path,
                'parent_folder_id': parent_folder_id,
                'relative_path': folder_path.split('/')[-1]
            })
        return folders
    else:
        return None


def find_file_id_by_folder_id(folder_id, limit, offset):
    json = {
        "query": f"""
                    mutation {{
                      querySQL(
                        sql: \"SELECT id FROM files WHERE parent_folder_id = {folder_id} LIMIT {limit} OFFSET {offset};\"
                      ) {{
                        columns
                        rows
                      }}
                    }}
                    """
    }
    response = requests.post(api_url, headers=headers, json=json)
    if response.status_code == 200:
        # print(response.json()['data']['querySQL']['rows'])
        return [item[0] for item in response.json()['data']['querySQL']['rows']]
    else:
        return None


def find_file_num_by_folder_id(folder_id):
    json = {
        "query": f"""
                    mutation {{
                      querySQL(
                        sql: \"SELECT COUNT(*) FROM files WHERE parent_folder_id = {folder_id};\"
                      ) {{
                        columns
                        rows
                      }}
                    }}
                    """
    }
    response = requests.post(api_url, headers=headers, json=json)
    if response.status_code == 200:
        # print(response.json()['data']['querySQL']['rows'])
        return response.json()['data']['querySQL']['rows'][0][0]
    else:
        return None

def find_image_id_or_scene_id_by_file_id(file_id):
    json1 = {
        "query": f"""
                    mutation {{
                      querySQL(
                        sql: \"SELECT image_id FROM images_files WHERE file_id = {file_id} ;\"
                      ) {{
                        columns
                        rows
                      }}
                    }}
                    """
    }
    json2 = {
        "query": f"""
                    mutation {{
                      querySQL(
                        sql: \"SELECT scene_id FROM scenes_files WHERE file_id = {file_id};\"
                      ) {{
                        columns
                        rows
                      }}
                    }}
                    """
    }
    response1 = requests.post(api_url, headers=headers, json=json1)
    response2 = requests.post(api_url, headers=headers, json=json2)
    if response1.status_code == 200 and response2.status_code == 200:
        image_id = response1.json()['data']['querySQL']['rows']
        scene_id = response2.json()['data']['querySQL']['rows']
        if len(image_id) == 0:
            return scene_id[0][0], True
        else:
            return image_id[0][0], False
    else:
        return None


def get_file_status(file_id, is_video):
    # print(is_video)
    if is_video:
        payload = {
            "query": f"query{{ findScene(id: {file_id}){{rating100}}}}"
            # "query": "mutation { sceneUpdate(input: {id: " + str(file_id) + "}){rating100}}",
        }
        response = requests.post(api_url, headers=headers, json=payload)
        # print("video")
        # print(response.status_code)
        # print(response.text)
        rating100 = response.json()['data']['findScene']['rating100']
    else:
        payload = {
            "query": f"query{{ findImage(id: {file_id}){{rating100}}}}"
            # "query": "mutation { imageUpdate(input: {id: " + str(file_id) + "}){rating100}}",
        }
        response = requests.post(api_url, headers=headers, json=payload)
        # print("pic")
        # print(response.status_code)
        # print(response.text)
        rating100 = response.json()['data']['findImage']['rating100']
    return rating100


def get_favorite_files(per_page, offset):
    json1 = {
        "query": f"""
                    mutation {{
                      querySQL(
                        sql: \"SELECT id FROM images WHERE rating = 100 ORDER BY RANDOM() LIMIT {per_page} OFFSET {offset};\"
                      ) {{
                        columns
                        rows
                      }}
                    }}
                    """
    }
    json2 = {
        "query": f"""
                    mutation {{
                      querySQL(
                        sql: \"SELECT id FROM scenes WHERE rating = 100 ORDER BY RANDOM() LIMIT {per_page} OFFSET {offset};\"
                      ) {{
                        columns
                        rows
                      }}
                    }}
                    """
    }
    response1 = requests.post(api_url, headers=headers, json=json1)
    response2 = requests.post(api_url, headers=headers, json=json2)
    # print(response1.text)
    image_ids = [item[0] for item in response1.json()['data']['querySQL']['rows']]
    scene_ids = [item[0] for item in response2.json()['data']['querySQL']['rows']]
    return image_ids, scene_ids

def get_favorite_num():
    json1 = {
        "query": f"""
                mutation {{
                  querySQL(
                    sql: \"SELECT COUNT(*) FROM images WHERE rating = 100;\"
                  ) {{
                    columns
                    rows
                  }}
                }}
                """
    }
    json2 = {
        "query": f"""
                mutation {{
                  querySQL(
                    sql: \"SELECT COUNT(*) FROM scenes WHERE rating = 100;\"
                  ) {{
                    columns
                    rows
                  }}
                }}
                """
    }
    response1 = requests.post(api_url, headers=headers, json=json1)
    response2 = requests.post(api_url, headers=headers, json=json2)

    if response1.status_code == 200 and response2.status_code == 200:
        num = response1.json()['data']['querySQL']['rows'][0][0] + response2.json()['data']['querySQL']['rows'][0][0]
        return num
    else:
        return None


if __name__ == '__main__':
    # folder_path, parent_folder_id = find_path_by_id(64)
    # print(folder_path)
    # sub_directories = directory_results['directories']
    # print(sub_directories)
    # sub = find_subdirectory_by_id()
    # print(sub)

    # print(subdirectory_id)
    # print(find_file_id_by_folder_id(12113, 50, 0))
    # print(find_image_id_or_scene_id_by_file_id(2845))
    # print(find_file_num_by_folder_id(2845))
    # print(get_favorite_files(1, 50))
    # print(get_favorite_num())
    # print(find_directory_by_id())
    # print( get_favorite_files(5, 20))
    pass