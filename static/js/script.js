// 等待DOM加载完成
document.addEventListener('DOMContentLoaded', function() {
    // 获取胶囊和表单元素
    const capsule = document.getElementById('timeCapsule');
    const mailForm = document.getElementById('mailForm');
    
    // 添加胶囊点击事件
    capsule.addEventListener('click', function() {
        // 添加胶囊打开动画
        this.classList.add('open-animation');
        
        // 动画结束后显示表单
        setTimeout(function() {
            capsule.style.display = 'none';
            document.querySelector('.click-hint').style.display = 'none';
            mailForm.classList.add('show-form');
        }, 800); // 与动画时长匹配
    });
    
    // 表单验证
    const form = document.querySelector('form');
    form.addEventListener('submit', function(event) {
        // 获取表单字段
        const title = document.getElementById('title').value;
        const content = document.getElementById('content').value;
        const recipient = document.getElementById('recipient').value;
        const password = document.getElementById('password').value;
        const deliveryDate = document.getElementById('delivery_date').value;
        
        // 简单验证
        if (!title || !content || !recipient || !password || !deliveryDate) {
            event.preventDefault();
            alert('请填写所有必填字段');
            return false;
        }
        
        // 验证邮箱格式
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(recipient)) {
            event.preventDefault();
            alert('请输入有效的邮箱地址');
            return false;
        }
        
        // 验证日期是否在未来
        const today = new Date();
        const selectedDate = new Date(deliveryDate);
        if (selectedDate <= today) {
            event.preventDefault();
            alert('请选择未来的日期');
            return false;
        }
        
        // 密码长度验证
        if (password.length < 6) {
            event.preventDefault();
            alert('密码长度至少为6个字符');
            return false;
        }
        
        // 添加表单提交动画效果
        mailForm.classList.add('submitting');
    });
    
    // 设置日期输入的最小值为今天
    const dateInput = document.getElementById('delivery_date');
    const today = new Date();
    const yyyy = today.getFullYear();
    const mm = String(today.getMonth() + 1).padStart(2, '0');
    const dd = String(today.getDate()).padStart(2, '0');
    const todayString = `${yyyy}-${mm}-${dd}`;
    dateInput.setAttribute('min', todayString);
});

// 添加像素风格效果
function addPixelEffect() {
    const pixelElements = document.querySelectorAll('.pixel-effect');
    pixelElements.forEach(element => {
        // 为像素风格元素添加特殊处理
        element.style.imageRendering = 'pixelated';
    });
}

// 页面加载完成后应用像素效果
window.onload = function() {
    addPixelEffect();
};
