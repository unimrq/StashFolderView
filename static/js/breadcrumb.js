const breadcrumb = document.getElementById('breadcrumb');
let isDragging = false;
let b_startX, b_scrollLeft;

// 按下鼠标时
breadcrumb.addEventListener('mousedown', (e) => {
    isDragging = true;
    b_startX = e.pageX - breadcrumb.offsetLeft;  // 获取鼠标按下时的位置
    b_scrollLeft = breadcrumb.scrollLeft;  // 获取当前的滚动位置
    breadcrumb.classList.add('dragging');  // 改变光标样式为抓取中
});

// 移动鼠标时
breadcrumb.addEventListener('mousemove', (e) => {
    if (!isDragging) return;  // 如果没有按住鼠标，则不做处理
    const x = e.pageX - breadcrumb.offsetLeft;  // 获取鼠标当前位置
    const walk = (x - b_startX) * 2;  // 计算拖动的距离
    breadcrumb.scrollLeft = b_scrollLeft - walk;  // 更新滚动位置
});

// 鼠标松开时
breadcrumb.addEventListener('mouseup', () => {
    isDragging = false;
    breadcrumb.classList.remove('dragging');  // 恢复光标样式
});

// 离开时
breadcrumb.addEventListener('mouseleave', () => {
    isDragging = false;
    breadcrumb.classList.remove('dragging');  // 恢复光标样式
});