
function logout() {
    fetch('/logout', {
        method: 'GET',
        credentials: 'same-origin' // 保证请求时带上当前的 session 信息
    })
    .then(response => {
        if (response.ok) {
            window.location.href = '/'; // 重定向到登录页面
        } else {
            alert('退出失败，请稍后再试');
        }
    })
    .catch(error => {
        console.error('退出时发生错误:', error);
        alert('退出失败，请稍后再试');
    });
}