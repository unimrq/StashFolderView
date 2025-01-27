function toggleFileLike(file_id, is_video) {
    var likeIcon = document.getElementById('like-' + file_id);
    var icon = likeIcon.querySelector('i');
    var currentState = likeIcon.getAttribute('data-liked');
    var newState = currentState === '100' ? '0' : '100';

    if (newState === '100') {
        icon.classList.remove('far', 'fa-heart');
        icon.classList.add('fas', 'fa-heart');

    } else {
        icon.classList.remove('fas', 'fa-heart');
        icon.classList.add('far', 'fa-heart');
    }

    likeIcon.setAttribute('data-liked', newState);

    fetch('/update_file_like_status', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            file_id: file_id.toString(),
            rating: newState.toString(),
            is_video: is_video.toString()
        })
    }).then(response => {
        if (!response.ok) {
            return response.json().then(data => {
                // alert('更新失败: ' + (data.message || '未知错误'));
            });
        }
        // alert('更新成功');
    }).catch(error => {
        console.error('请求失败', error);
    });

}
