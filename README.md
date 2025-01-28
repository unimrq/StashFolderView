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
docker run --restart=always -v /app/data:/app/data -e base_url=[stash url] -e username=[username] -e password=[password] -e api_key=[stashApi] -p 8000:8000 -d unimrq/stash-folder-view
# TODO
1. 优化悬浮按钮逻辑；完成
2. 瀑布流显示收藏按钮；完成
3. 收藏文件及文件夹在首页显示；完成
4. 登录功能完善；
5. 文件夹图标列表功能；完成
6. 左侧自动定位并高亮显示当前文件夹；完成
# BUG
1. 翻页功能逻辑不完善；已修改