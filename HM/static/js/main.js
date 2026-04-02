// MediCare HMS - Main JavaScript - Professional Edition

// ==================== SIDEBAR MANAGEMENT ====================
const sidebarToggle = document.getElementById('sidebarToggle');
const sidebar = document.getElementById('sidebar');
const mainContent = document.getElementById('main-content');

if (sidebarToggle && sidebar) {
  sidebarToggle.addEventListener('click', () => {
    sidebar.classList.toggle('collapsed');
    mainContent?.classList.toggle('sidebar-collapsed');
    localStorage.setItem('sidebar-collapsed', sidebar.classList.contains('collapsed'));
  });

  // Restore sidebar state on page load
  if (localStorage.getItem('sidebar-collapsed') === 'true') {
    sidebar.classList.add('collapsed');
    mainContent?.classList.add('sidebar-collapsed');
  }
}

// ==================== AUTO-DISMISS ALERTS ====================
function initializeAlerts() {
  document.querySelectorAll('.alert.fade.show').forEach(el => {
    const autoClose = el.dataset.autoclose !== 'false';
    if (autoClose) {
      setTimeout(() => {
        dismissAlert(el);
      }, 5000);
    }
  });
}

function dismissAlert(el) {
  el.style.transition = 'opacity 0.3s ease';
  el.style.opacity = '0';
  setTimeout(() => {
    el.style.transition = 'transform 0.3s ease, opacity 0.3s ease';
    el.style.transform = 'translateY(-10px)';
    el.style.opacity = '0';
    setTimeout(() => el.remove(), 300);
  }, 300);
}

// ==================== TOAST NOTIFICATION SYSTEM ====================
class Toast {
  constructor(message, type = 'info', duration = 4000) {
    this.message = message;
    this.type = type;
    this.duration = duration;
    this.element = null;
  }

  show() {
    // Get or create container
    let container = document.querySelector('.toast-container');
    if (!container) {
      container = document.createElement('div');
      container.className = 'toast-container';
      document.body.appendChild(container);
    }

    // Create toast element
    this.element = document.createElement('div');
    this.element.className = `toast ${this.type}`;
    this.element.innerHTML = `
      <div style="flex: 1;">
        <strong style="font-weight: 700;">${this.getTitle()}</strong>
        <div style="font-size: 13px; margin-top: 4px; opacity: 0.85;">${this.message}</div>
      </div>
      <button style="background: none; border: none; color: inherit; cursor: pointer; padding: 0; font-size: 18px; opacity: 0.6;" onclick="this.parentElement.remove()">×</button>
    `;

    container.appendChild(this.element);

    // Auto-dismiss
    if (this.duration > 0) {
      setTimeout(() => {
        if (this.element?.parentElement) {
          this.element.style.animation = 'slideOutRight 0.3s ease-out forwards';
          setTimeout(() => this.element?.remove(), 300);
        }
      }, this.duration);
    }

    return this.element;
  }

  getTitle() {
    const titles = {
      success: '✓ Success',
      error: '✕ Error',
      warning: '⚠ Warning',
      info: 'ℹ Info'
    };
    return titles[this.type] || 'Notification';
  }
}

// Toast shortcuts
window.showToast = {
  success: (msg, duration = 4000) => new Toast(msg, 'success', duration).show(),
  error: (msg, duration = 5000) => new Toast(msg, 'error', duration).show(),
  warning: (msg, duration = 4000) => new Toast(msg, 'warning', duration).show(),
  info: (msg, duration = 4000) => new Toast(msg, 'info', duration).show(),
};

// ==================== CONFIRMATION DIALOG ====================
function confirmAction(message, onConfirm, onCancel = null) {
  const dialog = document.createElement('div');
  dialog.style.cssText = `
    position: fixed;
    top: 0; left: 0;
    right: 0; bottom: 0;
    background: rgba(15,23,42,0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 10000;
    animation: fadeIn 0.2s ease;
  `;

  const content = document.createElement('div');
  content.style.cssText = `
    background: white;
    border-radius: 16px;
    padding: 28px;
    max-width: 400px;
    box-shadow: 0 16px 48px rgba(15,23,42,0.12);
    animation: slideUp 0.3s ease;
  `;

  content.innerHTML = `
    <h3 style="font-family: 'Sora', sans-serif; font-size: 18px; font-weight: 700; margin: 0 0 12px; color: #0f172a;">Confirm Action</h3>
    <p style="font-size: 14px; color: #64748b; margin: 0 0 24px; line-height: 1.6;">${message}</p>
    <div style="display: flex; gap: 10px; justify-content: flex-end;">
      <button onclick="this.parentElement.parentElement.parentElement.remove()" style="padding: 9px 18px; border: 1px solid #e2e8f0; background: white; border-radius: 8px; cursor: pointer; font-weight: 700; font-size: 14px; color: #64748b; transition: all 0.2s ease;" onmouseover="this.style.background='#f8fafc'" onmouseout="this.style.background='white'">Cancel</button>
      <button id="confirm-btn" style="padding: 9px 18px; background: #ef4444; color: white; border: none; border-radius: 8px; cursor: pointer; font-weight: 700; font-size: 14px; transition: all 0.2s ease; box-shadow: 0 2px 12px rgba(239,68,68,0.3);" onmouseover="this.style.background='#dc2626'" onmouseout="this.style.background='#ef4444'">Confirm</button>
    </div>
  `;

  dialog.appendChild(content);
  document.body.appendChild(dialog);

  // Add styles for animations
  const style = document.createElement('style');
  style.innerHTML = `
    @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
    @keyframes slideUp { from { transform: translateY(20px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }
  `;
  if (!document.querySelector('style[data-confirm-dialog]')) {
    style.setAttribute('data-confirm-dialog', '');
    document.head.appendChild(style);
  }

  document.getElementById('confirm-btn').addEventListener('click', () => {
    dialog.remove();
    if (typeof onConfirm === 'function') onConfirm();
  });

  dialog.addEventListener('click', (e) => {
    if (e.target === dialog) {
      dialog.remove();
      if (typeof onCancel === 'function') onCancel();
    }
  });
}

// ==================== FORM VALIDATION ====================
class FormValidator {
  constructor(formSelector) {
    this.form = document.querySelector(formSelector);
    if (this.form) {
      this.form.addEventListener('submit', (e) => this.validate(e));
    }
  }

  validate(e) {
    let isValid = true;
    const inputs = this.form.querySelectorAll('input, textarea, select');

    inputs.forEach(input => {
      const errorMsg = this.validateField(input);
      if (errorMsg) {
        isValid = false;
        this.showError(input, errorMsg);
      } else {
        this.clearError(input);
      }
    });

    if (!isValid) {
      e.preventDefault();
      showToast.error('Please fix the errors in the form');
    }

    return isValid;
  }

  validateField(field) {
    const value = field.value.trim();
    const type = field.type;
    const name = field.name;

    // Required field
    if (field.required && !value) {
      return `${this.getFieldLabel(field)} is required`;
    }

    // Email
    if (type === 'email' && value) {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(value)) {
        return 'Please enter a valid email address';
      }
    }

    // Phone
    if (type === 'tel' && value && !/^\d{10,}$/.test(value.replace(/\D/g, ''))) {
      return 'Please enter a valid phone number';
    }

    // Password
    if (type === 'password' && value && value.length < 6) {
      return 'Password must be at least 6 characters';
    }

    // Number
    if (type === 'number' && value && isNaN(value)) {
      return 'Please enter a valid number';
    }

    return null;
  }

  getFieldLabel(field) {
    const label = document.querySelector(`label[for="${field.id}"]`);
    return label ? label.textContent.replace('*', '').trim() : field.name;
  }

  showError(field, message) {
    field.style.borderColor = '#ef4444';
    let errorDiv = field.parentElement.querySelector('.error-message');
    if (!errorDiv) {
      errorDiv = document.createElement('div');
      errorDiv.className = 'error-message';
      errorDiv.style.cssText = 'color: #ef4444; font-size: 12px; margin-top: 4px; font-weight: 500;';
      field.parentElement.appendChild(errorDiv);
    }
    errorDiv.textContent = message;
  }

  clearError(field) {
    field.style.borderColor = '';
    const errorDiv = field.parentElement.querySelector('.error-message');
    if (errorDiv) errorDiv.remove();
  }
}

// ==================== KEYBOARD SHORTCUTS ====================
document.addEventListener('keydown', (e) => {
  // Ctrl/Cmd + K: Focus search
  if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
    e.preventDefault();
    document.querySelector('.search-global')?.focus();
  }

  // Escape: Close modals
  if (e.key === 'Escape') {
    document.querySelectorAll('.modal.show').forEach(modal => {
      modal.style.display = 'none';
    });
  }
});

// ==================== DELETE CONFIRMATION ====================
document.addEventListener('click', (e) => {
  const deleteBtn = e.target.closest('[data-delete]');
  if (deleteBtn) {
    e.preventDefault();
    const url = deleteBtn.href || deleteBtn.dataset.delete;
    const itemName = deleteBtn.dataset.itemName || 'this item';

    confirmAction(
      `Are you sure you want to delete ${itemName}? This action cannot be undone.`,
      () => window.location.href = url
    );
  }
});

// ==================== ACTIVE NAV LINK ====================
function highlightActiveNavLink() {
  const currentPath = window.location.pathname;
  document.querySelectorAll('.nav-link').forEach(link => {
    const href = link.getAttribute('href');
    if (href && currentPath.startsWith(href) && href !== '/') {
      link.classList.add('active');
    } else {
      link.classList.remove('active');
    }
  });
}

// ==================== PAGE LOAD ANIMATIONS ====================
function initializePageAnimations() {
  // Fade in cards with stagger
  const cards = document.querySelectorAll('.card, .stat-card');
  cards.forEach((card, index) => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(10px)';
    card.style.transition = `all 0.3s ease ${index * 50}ms`;
    setTimeout(() => {
      card.style.opacity = '1';
      card.style.transform = 'translateY(0)';
    }, 50);
  });
}

// ==================== RESPONSIVE SIDEBAR MOBILE ====================
function initializeMobileSidebar() {
  if (window.innerWidth <= 768) {
    sidebar?.classList.add('collapsed');
    mainContent?.classList.add('sidebar-collapsed');
  }

  window.addEventListener('resize', () => {
    if (window.innerWidth <= 768) {
      sidebar?.classList.add('collapsed');
    } else {
      const isCollapsed = localStorage.getItem('sidebar-collapsed') === 'true';
      if (isCollapsed) {
        sidebar?.classList.add('collapsed');
      } else {
        sidebar?.classList.remove('collapsed');
      }
    }
  });
}

// ==================== COPY TO CLIPBOARD ====================
window.copyToClipboard = function(text) {
  navigator.clipboard.writeText(text).then(() => {
    showToast.success('Copied to clipboard!', 2000);
  }).catch(() => {
    showToast.error('Failed to copy');
  });
};

// ==================== INITIALIZATION ====================
document.addEventListener('DOMContentLoaded', () => {
  initializeAlerts();
  highlightActiveNavLink();
  initializePageAnimations();
  initializeMobileSidebar();

  // Initialize form validation on form elements
  document.querySelectorAll('form').forEach(form => {
    new FormValidator(form.className ? '.' + form.className.split(' ')[0] : form.tagName);
  });
});

// ==================== GLOBAL ERROR HANDLER ====================
window.addEventListener('error', (e) => {
  console.error('Global error:', e.error);
  showToast.error('An unexpected error occurred');
});
