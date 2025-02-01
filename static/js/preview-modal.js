// script.js
let currentImageIndex = 0;
let scale = 1;
let startDistance = 0;
let startScale = 1;
// 定义拖动的变量
let isLongPress = false;
let startX, startY;
let offsetX = 0, offsetY = 0;
let startOffsetX = 0;
let startOffsetY = 0;
let img_offsetX = 0, img_offsetY = 0;
let lastX = 0;
let lastY = 0;
let pressTimer;
let isTouch = false; // 标记是否为触摸事件
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
    img_offsetX = 0
    img_offsetY = 0
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

// 两指缩放
// 计算两点之间的距离
// function getDistance(touch1, touch2) {
//     const dx = touch2.pageX - touch1.pageX;
//     const dy = touch2.pageY - touch1.pageY;
//     return Math.sqrt(dx * dx + dy * dy);
// }

// 监听两指放大缩小
// previewImage.addEventListener('touchstart', (e) => {
//     if (e.touches.length === 2) {
//         // 当两指接触时，记录开始时的距离
//         startDistance = getDistance(e.touches[0], e.touches[1]);
//         startScale = scale;
//     }
// });

previewImage.addEventListener('dblclick', (e) => {

    const centerX = window.innerWidth / 2;
    const centerY = window.innerHeight / 2;
    // console.log("center", centerX, centerY)
    // startOffsetX *= scale
    // startOffsetY *= scale
    if (scale < 9) {
        // 向上滚动：放大
        // console.log("offset1", img_offsetX, img_offsetY)
        offsetX = (centerX - e.clientX) / scale;
        offsetY = (centerY - e.clientY) / scale;
        scale *= 3;

        img_offsetX += offsetX
        img_offsetY += offsetY
        // console.log("offset", img_offsetX, img_offsetY)
        previewImage.style.transform = `scale(${scale}) translate(${img_offsetX}px, ${img_offsetY}px)`;
    } else {
        // 向下滚动：缩小
        scale = 1
        img_offsetX = 0
        img_offsetY = 0
        previewImage.style.transform = `scale(${scale}) translate(${img_offsetX}px, ${img_offsetY}px)`;
    }

});

// previewImage.addEventListener('touchmove', (e) => {
//     if (e.touches.length === 2) {
//         const newDistance = getDistance(e.touches[0], e.touches[1]);
//         const distanceRatio = newDistance / startDistance;
//         scale = startScale * distanceRatio;
//
//         // 限制缩放范围
//         scale = Math.max(1, Math.min(scale, 3)); // 设定最小缩放为1，最大为3
//
//         // 更新图片的transform属性
//         previewImage.style.transform = `scale(${scale})`;
//         if (scale > 1.05){
//             previewImage.style.zIndex = 1000
//         }else {
//             previewImage.style.zIndex = 0
//         }
//     }
// });

// previewImage.addEventListener('touchend', (e) => {
//     if (e.touches.length < 2) {
//         startDistance = 0;
//         startScale = scale;
//     }
// });

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
        console.log("move", e.clientX, e.clientY)
        // 根据缩放比例调整偏移量，避免移动过大
        img_offsetX += deltaX;
        img_offsetY += deltaY;
        console.log("move", img_offsetX, img_offsetY)
        // 更新图片位置
        // previewImage.style.transform = `scale(${scale}) translate(${img_offsetX}px, ${img_offsetY}px)`;

        // // 更新 lastX 和 lastY，防止偏移量累加出现误差
        startX = e.clientX;
        startY = e.clientY;
        previewImage.style.transform = `scale(${scale}) translate(${img_offsetX}px, ${img_offsetY}px)`;
        // if (Math.abs(deltaX) > 10 || Math.abs(deltaY) > 10){
        //     // 更新图片位置
        //     previewImage.style.transform = `scale(${scale}) translate(${img_offsetX}px, ${img_offsetY}px)`;
        // }

    }
});


// 鼠标松开时停止拖动
modal.addEventListener('mouseup', () => {
    // 清除定时器
    clearTimeout(pressTimer);
    isLongPress = false;
    // 更新起始偏移值
    // startOffsetX = offsetX;
    // startOffsetY = offsetY;
    // previewImage.style.cursor = 'grab'; // 恢复为抓取样式
});

modal.addEventListener('mouseleave', () => {
    // 清除定时器
    clearTimeout(pressTimer);
    isLongPress = false;
    // 更新起始偏移值
    // startOffsetX = offsetX;
    // startOffsetY = offsetY;
    // previewImage.style.cursor = 'grab'; // 恢复为抓取样式
});

previewImage.addEventListener('touchend', function(e) {
    const currentTime = new Date().getTime();
    const timeDifference = currentTime - lastTouchTime;

    if (timeDifference < 300 && timeDifference > 0) {
        // 双击事件发生，时间间隔小于300ms视为双击
        const centerX = window.innerWidth / 2;
        const centerY = window.innerHeight / 2;
        // console.log("center", centerX, centerY)
        // startOffsetX *= scale
        // startOffsetY *= scale
        if (scale < 9) {
            // 向上滚动：放大
            // console.log("offset1", img_offsetX, img_offsetY)
            offsetX = (centerX - e.clientX) / scale;
            offsetY = (centerY - e.clientY) / scale;
            scale *= 3;

            img_offsetX += offsetX
            img_offsetY += offsetY
            // console.log("offset", img_offsetX, img_offsetY)
            previewImage.style.transform = `scale(${scale}) translate(${img_offsetX}px, ${img_offsetY}px)`;
        } else {
            // 向下滚动：缩小
            scale = 1
            img_offsetX = 0
            img_offsetY = 0
            previewImage.style.transform = `scale(${scale}) translate(${img_offsetX}px, ${img_offsetY}px)`;
        }
    }

    lastTouchTime = currentTime; // 更新上次触摸时间
});