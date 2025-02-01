// script.js
let currentImageIndex = 0;
let scale = 1;
// 定义拖动的变量
let isLongPress = false;
let startX, startY;
let offsetX = 0, offsetY = 0;
let img_offsetX = 0, img_offsetY = 0;
let pressTimer;
let lastTouchTime = 0;

const previewImage = document.getElementById('preview-image');
const modal = document.getElementById('preview-modal');
const closeBtn = document.querySelector('.close');
const prevBtn = document.querySelector('.prev-btn');
const nextBtn = document.querySelector('.next-btn');
const imageCount = document.getElementById('image-count');

function openPreview(index0, is_video){
    currentImageIndex = index0;
    if (is_video === 'False'){
        // console.log("image_click")
        previewImage.src = links[currentImageIndex];
        modal.style.display = 'flex';
        scale = 1;
        previewImage.style.transform = `scale(${scale})`;
        imageCount.textContent = `${currentImageIndex + 1} / ${links.length}`;
    }else {
        window.open(links[currentImageIndex], '_blank');
    }
}
// 关闭预览框
closeBtn.addEventListener('click', () => {
    modal.style.display = 'none';
    img_offsetX = 0;
    img_offsetY = 0;
    scale = 1;
});

// 上一张图片
prevBtn.addEventListener('click', () => {
    do {
        currentImageIndex = (currentImageIndex - 1 + links.length) % links.length;
        } while (!links[currentImageIndex].includes('big_image'));

        // 满足条件后执行相应逻辑
        previewImage.src = links[currentImageIndex];
        scale = 1;
        previewImage.style.transform = `scale(${scale})`;
        imageCount.textContent = `${currentImageIndex + 1} / ${links.length}`;
});

// 下一张图片
nextBtn.addEventListener('click', () => {
    do {
        currentImageIndex = (currentImageIndex + 1) % links.length;
        } while (!links[currentImageIndex].includes('big_image'));

        // 满足条件后执行相应逻辑
        previewImage.src = links[currentImageIndex];
        scale = 1;
        previewImage.style.transform = `scale(${scale})`;
        imageCount.textContent = `${currentImageIndex + 1} / ${links.length}`;
});

previewImage.addEventListener('dblclick', (e) => {

    const centerX = window.innerWidth / 2;
    const centerY = window.innerHeight / 2;
    if (scale < 9) {
        // 向上滚动：放大
        // console.log("offset1", img_offsetX, img_offsetY)
        offsetX = (centerX - e.clientX) / scale;
        offsetY = (centerY - e.clientY) / scale;
        scale *= 3;

        img_offsetX += offsetX
        img_offsetY += offsetY
        // console.log("offset", img_offsetX, img_offsetY)
        previewImage.style.transition = 'transform 0.3s ease';
        previewImage.style.transform = `scale(${scale}) translate(${img_offsetX}px, ${img_offsetY}px)`;
    } else {
        // 向下滚动：缩小
        scale = 1
        img_offsetX = 0
        img_offsetY = 0
        previewImage.style.transition = 'transform 0.3s ease';
        previewImage.style.transform = `scale(${scale}) translate(${img_offsetX}px, ${img_offsetY}px)`;
    }

});

// 监听鼠标滚轮缩放
previewImage.addEventListener('wheel', (e) => {
    // 如果没有按住 Ctrl 键，则不进行缩放
    if (!e.ctrlKey) {
        return;
    }

    e.preventDefault(); // 防止页面滚动

    if (e.deltaY < 0) {
        // 向上滚动：放大
        scale *= 1.1;
    } else {
        // 向下滚动：缩小
        scale /= 1.1;
    }

    // 限制缩放范围
    scale = Math.max(1, Math.min(scale, 5)); // 设定最小缩放为1，最大为3

    // 更新图片的transform属性
    previewImage.style.transition = 'transform 0.3s ease';
    previewImage.style.transform = `scale(${scale})`;
});


modal.addEventListener('mousedown', (e) => {
    // 防止图片的默认拖动行为
    e.preventDefault();

    startX = e.clientX;
    startY = e.clientY;

    // 设置一个定时器判断是否为长按
    pressTimer = setTimeout(() => {
        isLongPress = true;
        // previewImage.style.cursor = 'grabbing'; // 改为抓取样式
    }, 100);  // 500毫秒判断为长按，可以调整这个值

});

// 鼠标移动时拖动图片
modal.addEventListener('mousemove', (e) => {
    if (isLongPress) {
        // 计算鼠标的相对移动
        let deltaX = e.clientX - startX;
        let deltaY = e.clientY - startY;
        // 根据缩放比例调整偏移量，避免移动过大
        img_offsetX += deltaX / scale;
        img_offsetY += deltaY / scale;

        // // 更新 lastX 和 lastY，防止偏移量累加出现误差
        startX = e.clientX;
        startY = e.clientY;
        previewImage.style.transition = 'none';
        previewImage.style.transform = `scale(${scale}) translate(${img_offsetX}px, ${img_offsetY}px)`;

    }
});

previewImage.addEventListener('touchmove', function(e) {
    if (e.touches.length === 1) {
        // 获取滑动的距离
        const moveX = e.touches[0].clientX - startX;
        const moveY = e.touches[0].clientY - startY;

        // 更新偏移量
        img_offsetX += moveX / scale;
        img_offsetY += moveY / scale;

        startX = e.touches[0].clientX
        startY = e.touches[0].clientY

        // 更新图片位置
        previewImage.style.transition = 'none';
        previewImage.style.transform = `scale(${scale}) translate(${img_offsetX}px, ${img_offsetY}px)`;

        // 防止默认的触摸滚动行为
        e.preventDefault();
    }
});

// 鼠标松开时停止拖动
modal.addEventListener('mouseup', () => {
    // 清除定时器
    clearTimeout(pressTimer);
    isLongPress = false;
});

modal.addEventListener('mouseleave', () => {
    // 清除定时器
    clearTimeout(pressTimer);
    isLongPress = false;
});


previewImage.addEventListener('touchstart', function(e) {
    // 记录触摸起始位置
    if (e.touches.length === 1) {
      startX = e.touches[0].clientX;
      startY = e.touches[0].clientY;
    }
});

previewImage.addEventListener('touchend', function(e) {
    const currentTime = new Date().getTime();
    const timeDifference = currentTime - lastTouchTime;

    if (timeDifference < 500 && timeDifference > 0) {
        // 双击事件发生，时间间隔小于300ms视为双击
        const centerX = window.innerWidth / 2;
        const centerY = window.innerHeight / 2;
        if (scale < 10) {
            // 向上滚动：放大
            // console.log("offset1", img_offsetX, img_offsetY)
            offsetX = (centerX - e.touches[0].clientX);
            offsetY = (centerY - e.touches[0].clientY);
            scale *= 3;

            img_offsetX += offsetX
            img_offsetY += offsetY
            // console.log("offset", img_offsetX, img_offsetY)
            previewImage.style.transition = 'transform 0.3s ease';
            previewImage.style.transform = `scale(${scale}) translate(${img_offsetX}px, ${img_offsetY}px)`;
        } else {
            // 向下滚动：缩小
            scale = 1
            img_offsetX = 0
            img_offsetY = 0
            previewImage.style.transition = 'transform 0.3s ease';
            previewImage.style.transform = `scale(${scale}) translate(${img_offsetX}px, ${img_offsetY}px)`;
        }
    }
    lastTouchTime = currentTime; // 更新上次触摸时间
});