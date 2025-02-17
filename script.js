function openFormPage() {
    // 隐藏首页
    document.querySelector('.homepage').style.display = 'none';

    // 显示表单页面
    document.getElementById('formPage').classList.remove('hidden');
}

// 简单的表单提交处理
document.getElementById('contactForm').addEventListener('submit', function(event) {
    event.preventDefault();
    alert('你的信已成功发送到未来！');
    // 清空表单
    document.getElementById('contactForm').reset();
});
