// {#const go_folderId = document.getElementById('folder-icon').getAttribute('data-folder-id');#}

const toggleReadCheckbox = document.getElementById('toggleRead');
const selectVideoCheckbox = document.getElementById('select-video');
const folderList = document.getElementById('folderList');

function updateFolderVisibility() {
    // 获取所有文件夹项
    const folders = folderList.getElementsByClassName('folder');

    for (let folder of folders) {
        const folderRead = folder.getAttribute('data-folder-read');
        const folderRelativePath = folder.getAttribute('data-folder-relative-path');

        // 判断复选框状态和文件夹的状态
        if (toggleReadCheckbox.checked === false) {
            // 如果 check_box 为 0，全部显示
            folder.style.display = 'block';
        } else {
            // 如果 check_box 为 1，且 folder.relative_path != '上一级'，隐藏 folder_read == 1 的项
            if (folderRelativePath !== '上一级' && folderRead === '1') {
                folder.style.display = 'none';
            } else {
                folder.style.display = 'block';
            }
        }
    }
}

// 监听复选框状态变化
selectVideoCheckbox.addEventListener('change', function (){
    localStorage.setItem('newWindowCheckbox', selectVideoCheckbox.checked);
});

toggleReadCheckbox.addEventListener('change', function (){
    updateFolderVisibility();
    localStorage.setItem('toggleReadState', toggleReadCheckbox.checked);

});


window.onload = function() {
    // 检查 localStorage 中是否有已保存的状态
    const savedState1 = localStorage.getItem('toggleReadState');
    const savedState2 = localStorage.getItem('newWindowCheckbox');
    const storedFolderId = localStorage.getItem('folder_id');
    if (savedState1 !== null && savedState2 !== null) {
        toggleReadCheckbox.checked = (savedState1 === 'true');
        selectVideoCheckbox.checked = (savedState2 === 'true');
        updateFolderVisibility();
    }
    if (storedFolderId) {
        // console.log(storedFolderId)
        // 获取对应的元素
        var element = document.getElementById(storedFolderId);
        var folder_icon = document.getElementById("icon-" + storedFolderId);
        // console.log(folder_icon)
        if (element){
            var folderRelativePath = element.getAttribute("data-folder-relative-path");

            // console.log(folder_icon.getAttribute("data-folder-id"))
            var folder_bar = element.querySelector(".folder-bar")
            var folder_icon_item = folder_icon.querySelector('i')
            // console.log(folder_icon_item)
            if (folderRelativePath !== '上一级') {
                // 滚动到该元素
                // console.log("定位中")
                element.scrollIntoView({ behavior: "smooth", block: "center" });
                folder_bar.style.backgroundColor = '#B0BEDE'
                folder_icon_item.style.color = '#07689f'
            }
        }

    }
    localStorage.setItem('folder_id', folder_id);
};