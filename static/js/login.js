document.getElementById('loginForm').addEventListener('submit', function(event) {
  event.preventDefault();  // 防止表单默认提交

  const username = document.getElementById('username').value;
  const password = document.getElementById('password').value;

  // 发送 POST 请求到后端
  fetch('/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ username, password }),
  })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        // alert('Login successful!');
        window.location.href = '/folders';  // 假设登录成功后跳转到仪表板页面
      } else {
        document.getElementById('error-message').style.display = 'block';
      }
    })
    .catch(err => console.error('Error:', err));
});
