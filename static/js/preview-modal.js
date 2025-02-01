// script.js
let currentImageIndex = 0;
let scale = 1;

const previewImage = document.getElementById('preview-image');
const modal = document.getElementById('preview-modal');
const closeBtn = document.querySelector('.close');
const prevBtn = document.querySelector('.prev-btn');
const nextBtn = document.querySelector('.next-btn');
const imageCount = document.getElementById('image-count');

function openPreview(index0, is_video){
    if (is_video === 'False'){
        console.log("image_click")
        currentImageIndex = index0;
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
    currentImageIndex = (currentImageIndex - 1 + links.length) % links.length;
    previewImage.src = links[currentImageIndex];
    scale = 1;
    previewImage.style.transform = `scale(${scale})`;
    imageCount.textContent = `${currentImageIndex + 1} / ${links.length}`;
});

// 下一张图片
nextBtn.addEventListener('click', () => {
    currentImageIndex = (currentImageIndex + 1) % links.length;
    previewImage.src = links[currentImageIndex];
    scale = 1;
    previewImage.style.transform = `scale(${scale})`;
    imageCount.textContent = `${currentImageIndex + 1} / ${links.length}`;
});