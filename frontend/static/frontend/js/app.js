// ===== API Helper =====
const API_BASE = '/api';

function getToken() {
    return localStorage.getItem('access_token');
}

function setTokens(access, refresh) {
    localStorage.setItem('access_token', access);
    localStorage.setItem('refresh_token', refresh);
}

function clearTokens() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('username');
}

function isLoggedIn() {
    return !!getToken();
}

async function apiRequest(url, method = 'GET', body = null) {
    const headers = { 'Content-Type': 'application/json' };
    const token = getToken();
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    const options = { method, headers };
    if (body) {
        options.body = JSON.stringify(body);
    }

    const response = await fetch(API_BASE + url, options);

    if (response.status === 401 && token) {
        clearTokens();
        window.location.href = '/login/';
        return { _status: 401, error: 'Session expired. Please login again.' };
    }

    if (response.status === 204) {
        return { _status: 204, success: true };
    }

    let data;
    try {
        data = await response.json();
    } catch (e) {
        return { _status: response.status, error: 'Server error. Please try again.' };
    }

    if (typeof data === 'object' && data !== null && !Array.isArray(data)) {
        data._status = response.status;
    } else {
        data = { _status: response.status, results: data };
    }
    return data;
}

// ===== Alert Helpers =====
function showAlert(elementId, message, type = 'error') {
    const el = document.getElementById(elementId);
    if (!el) return;
    el.className = `alert alert-${type}`;
    el.textContent = message;
    el.style.display = 'block';
    if (type === 'success') {
        setTimeout(() => { el.style.display = 'none'; }, 3000);
    }
}

function hideAlert(elementId) {
    const el = document.getElementById(elementId);
    if (el) el.style.display = 'none';
}

// ===== Logout =====
function logout() {
    clearTokens();
    window.location.href = '/login/';
}
