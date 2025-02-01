// script.js
let currentImageIndex = 0;
let scale = 1;
let startDistance = 0;
let startScale = 1;

const previewImage = document.getElementById('preview-image');
const modal = document.getElementById('preview-modal');
const closeBtn = document.querySelector('.close');
const prevBtn = document.querySelector('.prev-btn');
const nextBtn = document.querySelector('.next-btn');
const imageCount = document.getElementById('image-count');

function openPreview(index0, is_video){
    currentImageIndex = index0;
    if (is_video === 'False'){
        console.log("image_click")
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
function getDistance(touch1, touch2) {
    const dx = touch2.pageX - touch1.pageX;
    const dy = touch2.pageY - touch1.pageY;
    return Math.sqrt(dx * dx + dy * dy);
}

// 监听两指放大缩小
previewImage.addEventListener('touchstart', (e) => {
    if (e.touches.length === 2) {
        // 当两指接触时，记录开始时的距离
        startDistance = getDistance(e.touches[0], e.touches[1]);
        startScale = scale;
    }
});

previewImage.addEventListener('touchmove', (e) => {
    if (e.touches.length === 2) {
        const newDistance = getDistance(e.touches[0], e.touches[1]);
        const distanceRatio = newDistance / startDistance;
        scale = startScale * distanceRatio;

        // 限制缩放范围
        scale = Math.max(1, Math.min(scale, 3)); // 设定最小缩放为1，最大为3

        // 更新图片的transform属性
        previewImage.style.transform = `scale(${scale})`;
        if (scale > 1.05){
            previewImage.style.zIndex = 1000
        }else {
            previewImage.style.zIndex = 0
        }
    }
});

previewImage.addEventListener('touchend', (e) => {
    if (e.touches.length < 2) {
        startDistance = 0;
        startScale = scale;
    }
});

// 监听鼠标滚轮缩放
previewImage.addEventListener('wheel', (e) => {
    e.preventDefault(); // 防止页面滚动

    if (e.deltaY < 0) {
        // 向上滚动：放大
        scale *= 1.1;
    } else {
        // 向下滚动：缩小
        scale /= 1.1;
    }

    // 限制缩放范围
    scale = Math.max(1, Math.min(scale, 3)); // 设定最小缩放为1，最大为3

    // 更新图片的transform属性
    previewImage.style.transform = `scale(${scale})`;
    if (scale > 1.05){
        previewImage.style.zIndex = 1000
    }else {
        previewImage.style.zIndex = 0
    }
});