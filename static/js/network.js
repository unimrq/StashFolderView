function toggle_network_status(folder_id) {
    const icon = document.getElementById(`network-toggle`);
    // 获取当前图标的状态
    const currentNetworkStatus = icon.classList.contains('fas') ? 0 : 1;
    console.log(currentNetworkStatus)
    console.log(icon.classList)
    if (currentNetworkStatus === 0) {
        icon.classList.remove('fas', 'fa-desktop');
        icon.classList.add('fa', 'fa-globe');
        updateNetworkStatus(1);
    } else {
        // 如果当前是未点赞状态，点击后变为已点赞
        icon.classList.remove('fa', 'fa-globe');
        icon.classList.add('fas', 'fa-desktop');
        updateNetworkStatus(0);
    }
}

// 更新数据库中的 like 状态
function updateNetworkStatus(networkStatus) {
    fetch('/update_network_status', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ network_status: networkStatus })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log('网络状态更新成功');
        }
    })
    .catch(error => {
        console.error('更新失败', error);
    });
}
