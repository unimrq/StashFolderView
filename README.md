# 预览
![img.png](static/images/img.png)
# 特性
1. 文件夹式浏览，瀑布流显示图片；
2. 新增已读、收藏和删除文件夹标记；
3. 返回顶部、翻页等功能集成在悬浮按钮中；
4. 实现简易的登录界面；
5. 适配移动端；
6. 支持docker部署；
# 部署
docker run --restart=always -v [替换为本docker目录]:/app/data -v [替换为stash数据库]:/app/stash-go.sqlite -e base_url=[stash的地址，不要去掉“/”] -e username=[登录用户名] -e password=[登录密码] -e api_key=[stashApi] -p 8000:8000 -d unimrq/stash-folder-view
# TODO
1. 优化悬浮按钮逻辑；
2. 瀑布流显示文件名以及收藏按钮；
3. 收藏文件及文件夹在首页显示；完成
4. 登录功能完善；
