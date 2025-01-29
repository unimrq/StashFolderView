// 菜单按钮点击事件：切换目录栏的显示与隐藏
const menuBtn = document.getElementById('menu-btn');
const foldersContainer = document.getElementById('folders-container');
const filesContainer = document.getElementById('files-container');
let isHide = localStorage.getItem('isHide');
const isMobile = window.innerWidth <= 768;
isHide = isMobile;


menuBtn.addEventListener('click', function () {
    // {#foldersContainer.classList.toggle('hidden');  // 切换 hidden 类来显示/隐藏目录#}
    isHide = !isHide
    localStorage.setItem('isHide', isHide);

    if (isMobile) {
        if (isHide) {
            filesContainer.style.width = '100%';  // 设置宽度为100%
            foldersContainer.style.width = '0%'
            // {#breadcrumb.style.display = 'none'#}
            foldersContainer.style.overflowY = 'hidden'
            foldersContainer.style.paddingRight = '0'
        } else {
            filesContainer.style.width = '0%';   // 恢复为原来的宽度
            foldersContainer.style.width = '100%'
            // {#breadcrumb.style.display = 'block'#}
            foldersContainer.style.display = 'block'
            foldersContainer.style.overflowY = 'auto'
            foldersContainer.style.paddingRight = '10px'
        }
    } else {
        if (isHide) {
            filesContainer.style.width = '100%';  // 设置宽度为100%
            foldersContainer.style.width = '0%'
            // {#breadcrumb.style.display = 'none'#}
            foldersContainer.style.overflowY = 'hidden'
            foldersContainer.style.paddingRight = '0'
        } else {
            filesContainer.style.width = '80%';   // 恢复为原来的宽度
            foldersContainer.style.width = '20%'
            // {#breadcrumb.style.display = 'block'#}
            foldersContainer.style.display = 'block'
            foldersContainer.style.overflowY = 'auto'
            foldersContainer.style.paddingRight = '10px'
        }
    }
});
