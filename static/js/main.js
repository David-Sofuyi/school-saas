/**
 * Nigerian School Management SaaS - Main Client JavaScript
 */

document.addEventListener('DOMContentLoaded', () => {
  // 1. PWA Service Worker Registration
  if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
      navigator.serviceWorker
        .register('/static/js/service-worker.js')
        .then((reg) => {
          console.log('[PWA] Service Worker registered successfully with scope:', reg.scope);
        })
        .catch((err) => {
          console.warn('[PWA] Service Worker registration failed:', err);
        });
    });
  }

  // 2. Sidebar Toggle for Mobile Devices
  const sidebarToggleBtn = document.getElementById('sidebarToggleBtn');
  const sidebar = document.getElementById('appSidebar');
  const sidebarBackdrop = document.getElementById('sidebarBackdrop');

  function openSidebar() {
    if (sidebar) sidebar.classList.add('show');
    if (sidebarBackdrop) sidebarBackdrop.classList.add('show');
  }

  function closeSidebar() {
    if (sidebar) sidebar.classList.remove('show');
    if (sidebarBackdrop) sidebarBackdrop.classList.remove('show');
  }

  if (sidebarToggleBtn) {
    sidebarToggleBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      if (sidebar && sidebar.classList.contains('show')) {
        closeSidebar();
      } else {
        openSidebar();
      }
    });
  }

  if (sidebarBackdrop) {
    sidebarBackdrop.addEventListener('click', closeSidebar);
  }

  // 3. Auto-dismiss Bootstrap Alerts after 5 seconds
  const autoDismissAlerts = document.querySelectorAll('.alert-dismissible:not(.alert-permanent)');
  autoDismissAlerts.forEach((alertEl) => {
    setTimeout(() => {
      if (typeof bootstrap !== 'undefined' && bootstrap.Alert) {
        const alertInstance = bootstrap.Alert.getOrCreateInstance(alertEl);
        alertInstance.close();
      } else {
        alertEl.style.transition = 'opacity 0.5s ease';
        alertEl.style.opacity = '0';
        setTimeout(() => alertEl.remove(), 500);
      }
    }, 5000);
  });

  // 4. CSRF Token Helper for AJAX Fetch Requests
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  window.getCsrfToken = function() {
    const metaCsrf = document.querySelector('meta[name="csrf-token"]');
    if (metaCsrf) return metaCsrf.getAttribute('content');
    return getCookie('csrftoken');
  };

  // 5. Delete Confirmation Modal Trigger
  const confirmModalEl = document.getElementById('confirmDeleteModal');
  let confirmModalInstance = null;
  if (confirmModalEl && typeof bootstrap !== 'undefined') {
    confirmModalInstance = new bootstrap.Modal(confirmModalEl);
  }

  document.querySelectorAll('[data-confirm-delete]').forEach((btn) => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      const targetUrl = btn.getAttribute('data-delete-url') || btn.getAttribute('href');
      const itemName = btn.getAttribute('data-item-name') || 'this item';
      const formId = btn.getAttribute('data-form-id');

      const modalItemSpan = document.getElementById('confirmDeleteModalItemName');
      const confirmBtn = document.getElementById('confirmDeleteModalBtn');
      const formTarget = document.getElementById('confirmDeleteForm');

      if (modalItemSpan) modalItemSpan.textContent = itemName;

      if (confirmBtn) {
        confirmBtn.onclick = function() {
          if (formId) {
            const form = document.getElementById(formId);
            if (form) form.submit();
          } else if (formTarget && targetUrl) {
            formTarget.action = targetUrl;
            formTarget.submit();
          } else if (targetUrl) {
            window.location.href = targetUrl;
          }
        };
      }

      if (confirmModalInstance) {
        confirmModalInstance.show();
      } else if (confirm(`Are you sure you want to delete ${itemName}?`)) {
        if (formId) {
          const form = document.getElementById(formId);
          if (form) form.submit();
        } else if (targetUrl) {
          window.location.href = targetUrl;
        }
      }
    });
  });

  // 6. Notification Polling (Fetch unread count every 60s)
  function pollNotifications() {
    const badge = document.getElementById('notificationUnreadBadge');
    if (!badge) return;

    fetch('/api/v1/notifications/unread-count/', {
      headers: {
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest'
      }
    })
      .then((res) => {
        if (res.ok) return res.json();
        throw new Error('Notification fetch failed');
      })
      .then((data) => {
        const count = data.unread_count || data.count || 0;
        if (count > 0) {
          badge.textContent = count > 99 ? '99+' : count;
          badge.classList.remove('d-none');
        } else {
          badge.textContent = '0';
          badge.classList.add('d-none');
        }
      })
      .catch(() => {
        // Silently fail if endpoint is not implemented or user logged out
      });
  }

  // Start polling if unread badge exists
  if (document.getElementById('notificationUnreadBadge')) {
    pollNotifications();
    setInterval(pollNotifications, 60000);
  }

  // 7. Dynamic Form Field Toggling
  document.querySelectorAll('[data-toggle-target]').forEach((trigger) => {
    const targetSelector = trigger.getAttribute('data-toggle-target');
    const targetElement = document.querySelector(targetSelector);
    if (!targetElement) return;

    function evaluateToggle() {
      if (trigger.type === 'checkbox') {
        targetElement.style.display = trigger.checked ? '' : 'none';
      } else if (trigger.tagName === 'SELECT') {
        const expectedValue = trigger.getAttribute('data-toggle-value');
        targetElement.style.display = trigger.value === expectedValue ? '' : 'none';
      }
    }

    trigger.addEventListener('change', evaluateToggle);
    evaluateToggle(); // Initial check
  });

  // 8. Simple Chart Setup Placeholders
  window.initSimpleBarChart = function(canvasId, labels, dataPoints, title) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;
    console.log(`[Chart Placeholder] Initializing bar chart on #${canvasId}:`, { labels, dataPoints, title });
    // If Chart.js is present on window, render it, else draw a lightweight fallback
    if (typeof Chart !== 'undefined') {
      new Chart(canvas, {
        type: 'bar',
        data: {
          labels: labels,
          datasets: [{
            label: title || 'Data',
            data: dataPoints,
            backgroundColor: '#1a73e8',
            borderRadius: 6
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false
        }
      });
    }
  };
});
