const total_pages = document.getElementById('total_pages').getAttribute('data-folder-id');
const page = document.getElementById('page').getAttribute('data-folder-id');
const folder_id = document.getElementById('folder_id').getAttribute('data-folder-id');
const parent_folder_id = document.getElementById('parent_folder_id').getAttribute('data-folder-id');

const actionButton = document.getElementById('actionButton');
const menu = document.getElementById('floating-btn-menu');
const goPrevious = document.getElementById('goPrevious');
const goNext = document.getElementById('goNext');
const goTop = document.getElementById('goTop');
const goParentFolder = document.getElementById('goParentFolder');
const myContainer = document.getElementById('files-container');

// 控制菜单显示/隐藏
let isMenuVisible = false;
let menu_need_show = false;
if(parseInt(total_pages) > 1){
    menu_need_show = true
}

const showMenu = () => {
    if(parseInt(total_pages) > 1){
        isMenuVisible = true;
        menu.style.display = 'block';
        // 根据总页数和当前页数显示菜单项
        if (page > 1) {
            document.getElementById('goPrevious').style.display = 'block';
        } else {
            document.getElementById('goPrevious').style.display = 'none';
        }

        if (parseInt(page) < parseInt(total_pages)) {
            document.getElementById('goNext').style.display = 'block';
        } else {
            document.getElementById('goNext').style.display = 'none';
        }
    }

};

const hideMenu = () => {
    isMenuVisible = false;
    menu.style.display = 'none';
};

actionButton.onclick = () => {
    if(menu_need_show){
        if(isMenuVisible){
            hideMenu()
        } else {
            showMenu();
        }
    } else {
        console.log("点击按钮")
        myContainer.scrollTo({ top: 0, behavior: 'smooth' });
    }
};
// 菜单项点击事件
goPrevious.onclick = () => {
    // console.log("上一页");
    window.location.href = '/folders?id=' + folder_id + '&page=' + (parseInt(page) - 1);
    hideMenu();
};
goNext.onclick = () => {
    // console.log("下一页");
    window.location.href = '/folders?id=' + folder_id + '&page=' + (parseInt(page) + 1);
    hideMenu();
};
goTop.onclick = () => {
    myContainer.scrollTo({ top: 0, behavior: 'smooth' });
    hideMenu();
};
goParentFolder.onclick = () => {
    window.location.href = '/folders?id=' + parent_folder_id;
    hideMenu();
};


// 点击页面其他地方隐藏菜单
document.addEventListener('mousedown', function (e) {
    // 检查点击的是否为按钮或菜单项
        if (!actionButton.contains(e.target) && !menu.contains(e.target)) {
        hideMenu();
    }
});