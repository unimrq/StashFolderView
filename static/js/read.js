// 切换已读/未读状态
function toggleReadStatus(folderId) {
    // 获取对勾图标元素
    const icon = document.getElementById(`check-icon-${folderId}-icon`);

    // 获取当前图标的状态（已读状态）
    const currentReadStatus = icon.classList.contains('fas') ? 1 : 0;

    // 如果当前是已读状态，点击后变为未读
    if (currentReadStatus === 1) {
        // 切换到未读状态
        icon.classList.remove('fas', 'fa-check-square');  // 移除已读图标
        icon.classList.add('far', 'fa-check-square');     // 添加未读图标
        icon.style.color = 'white';                         // 设置为灰色
        // 更新数据库状态为未读
        updateReadStatus(folderId, 0);
    } else {
        // 如果当前是未读状态，点击后变为已读
        icon.classList.remove('far', 'fa-check-square');  // 移除未读图标
        icon.classList.add('fas', 'fa-check-square');     // 添加已读图标
        icon.style.color = 'lightgreen';                        // 设置为绿色
        // 更新数据库状态为已读
        updateReadStatus(folderId, 1);
    }
}

// 更新数据库中的 read 状态
function updateReadStatus(folderId, readStatus) {
    fetch('/update_read_status', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ folder_id: folderId, read_status: readStatus })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log('已读状态更新成功');
        }
    })
    .catch(error => {
        console.error('更新失败', error);
    });
}
