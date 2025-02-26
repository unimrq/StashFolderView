# 预览
![img.png](static/images/img.png)
![img_2.png](static/images/img_2.png)
![img_1.png](static/images/img_1.png)

# 特性
1. 文件夹式浏览，瀑布流显示图片，实现图片收藏；
2. 文件夹级别已读、收藏和删除标记；
3. 联动stash实现图片、视频收藏；
4. 实现简易的登录界面；
5. 适配移动端；
6. 支持docker部署；
7. 实现收藏图片展示、收藏文件夹展示；

# 部署
## 1. 部署stash
如果您没有部署stash，请先参考原仓库https://github.com/stashapp/stash
## 2. 获取stash_api
设置stash的账户凭证并生成stash_api

## 3. 部署stash-folder-view
``docker run --restart=always -v /app/data:/app/data -e base_url=[stash_url] -e jump_url=[stash_url] -e username=[username] -e password=[password] -e api_key=[stash_api] -p 8000:8000 -d unimrq/stash-folder-view``

stash_url: 容器访问stash的地址，需要保留"/"；例如"http://192.168.1.51:12001/"

jump_url: 图片跳转链接的stash地址，留空默认与stash_url相同

username: stash-folder-view登录用户名，不必与stash的凭证相同

password: stash-folder-view登录密码，不必与stash的凭证相同
# TODO
1. 优化悬浮按钮逻辑；完成
2. 瀑布流显示收藏按钮；完成
3. 收藏文件及文件夹在首页显示；完成
4. 登录功能完善；完成
5. 文件夹图标列表功能；完成
6. 左侧自动定位并高亮显示当前文件夹；完成
7. 分离收藏页面；完成
8. 新增收藏文件夹显示页面；完成
9. 新增左侧目录固定功能；已删除
10. 新增左侧目录缩起已读功能；完成
11. 新增路径栏可左右滑动功能；
12. 返回顶部时悬浮按钮功能修改为返回上一级