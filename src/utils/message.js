// 简单的消息提示工具
export function showMessage(message, type = 'info') {
  const toast = document.createElement('div')
  toast.className = `toast toast-${type}`
  toast.textContent = message
  
  // 添加样式
  Object.assign(toast.style, {
    position: 'fixed',
    top: '20px',
    right: '20px',
    padding: '12px 24px',
    borderRadius: '6px',
    color: '#fff',
    fontSize: '14px',
    zIndex: '9999',
    boxShadow: '0 4px 12px rgba(0,0,0,0.15)',
    animation: 'slideIn 0.3s ease-out',
    maxWidth: '300px',
    wordWrap: 'break-word'
  })
  
  // 根据类型设置背景色
  const colors = {
    success: '#28a745',
    error: '#dc3545',
    warning: '#ffc107',
    info: '#17a2b8'
  }
  toast.style.background = colors[type] || colors.info
  
  document.body.appendChild(toast)
  
  // 3秒后自动移除
  setTimeout(() => {
    toast.style.animation = 'slideOut 0.3s ease-out'
    setTimeout(() => {
      document.body.removeChild(toast)
    }, 300)
  }, 3000)
}

// 添加CSS动画
if (!document.getElementById('toast-animations')) {
  const style = document.createElement('style')
  style.id = 'toast-animations'
  style.textContent = `
    @keyframes slideIn {
      from {
        transform: translateX(400px);
        opacity: 0;
      }
      to {
        transform: translateX(0);
        opacity: 1;
      }
    }
    @keyframes slideOut {
      from {
        transform: translateX(0);
        opacity: 1;
      }
      to {
        transform: translateX(400px);
        opacity: 0;
      }
    }
  `
  document.head.appendChild(style)
}
