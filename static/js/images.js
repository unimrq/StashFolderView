const grid = document.querySelector('#masonry-grid');
// 初始化 Masonry
const masonryInstance = new Masonry(grid, {
    itemSelector: '.grid-item',  // 每个项目
    columnWidth: '.grid-item',    // 每列的宽度
    percentPosition: true,       // 使宽度为百分比
    gutter: 10,                  // 每个项目之间的间距
    fitWidth: true,              // 容器宽度自适应
    isResizable: true,           // 响应式调整
    horizontalOrder: false,       // 使 Masonry 容器按水平方向顺序排列
});

// 监听每个图片的加载事件
const images = document.querySelectorAll('.grid-item img');
images.forEach(function (img) {
    img.addEventListener('load', function () {
        // 图片加载完成后，显示相应的播放图标
        var parentItem = img.closest('.grid-item');
        if (parentItem.classList.contains('video')) {
            parentItem.querySelector('.play-icon').style.display = 'block';
        }
        // 图片加载完成后，触发 Masonry 布局
        masonryInstance.layout();  // 重新计算 Masonry 布局
    });
});

// 使用 imagesLoaded 插件监听图片加载完成
imagesLoaded(grid, function() {
    masonryInstance.layout();
});
window.addEventListener('resize', function() {
    masonryInstance.layout();
  });
