function toggleLike(folderId) {
    // 获取爱心图标元素
    const icon = document.getElementById(`heart-icon-${folderId}`);

    // 获取当前图标的状态
    const currentLikeStatus = icon.classList.contains('fas') ? 1 : 0;

    // 如果当前是已点赞状态，点击后变为未点赞
    if (currentLikeStatus === 1) {
        // 切换到未点赞状态
        icon.classList.remove('fas', 'fa-heart');  // 移除已点赞图标
        icon.classList.add('far', 'fa-heart');     // 添加未点赞图标
        icon.style.color = 'gray';                  // 设置为灰色
        // 更新数据库状态为未点赞
        updateLikeStatus(folderId, 0);
    } else {
        // 如果当前是未点赞状态，点击后变为已点赞
        icon.classList.remove('far', 'fa-heart');  // 移除未点赞图标
        icon.classList.add('fas', 'fa-heart');     // 添加已点赞图标
        icon.style.color = 'red';                   // 设置为红色
        // 更新数据库状态为已点赞
        updateLikeStatus(folderId, 1);
    }
}

// 更新数据库中的 like 状态
function updateLikeStatus(folderId, likeStatus) {
    fetch('/update_like_status', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ folder_id: folderId, like_status: likeStatus })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log('点赞状态更新成功');
        }
    })
    .catch(error => {
        console.error('更新失败', error);
    });
}
