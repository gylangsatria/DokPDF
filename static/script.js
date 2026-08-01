const API_BASE_URL = '/api';

// Modal functions
function openModal(id) {
    document.getElementById(id).style.display = 'flex';
}

function closeModal(id) {
    document.getElementById(id).style.display = 'none';
}

// Helper function to call API
async function callAPI(endpoint, formData) {
    showLoading();
    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Terjadi kesalahan pada server');
        }
        
        return response;
    } catch (error) {
        showToast('error', error.message);
        throw error;
    } finally {
        hideLoading();
    }
}

function downloadFile(blob, filename) {
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
}

function showLoading(text = 'Memproses...') {
    document.getElementById('loading-text').textContent = text;
    document.getElementById('loadingOverlay').style.display = 'flex';
}

function hideLoading() {
    document.getElementById('loadingOverlay').style.display = 'none';
}

function showToast(type, message) {
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = message;
    container.appendChild(toast);
    setTimeout(() => {
        toast.style.opacity = '0';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// Add/Remove dynamic merge inputs
function addMergeInput() {
    const list = document.getElementById('merge-dynamic-list');
    const item = document.createElement('div');
    item.className = 'merge-file-item';
    item.innerHTML = `
        <input type="file" accept=".pdf">
        <button type="button" style="width:auto; background:#666" onclick="this.parentElement.remove()">X</button>
    `;
    list.appendChild(item);
}

// Tool Operations
async function doMerge() {
    const inputs = document.querySelectorAll('#merge-dynamic-list input[type="file"]');
    const formData = new FormData();
    let count = 0;
    inputs.forEach(input => {
        if (input.files[0]) {
            formData.append('files', input.files[0]);
            count++;
        }
    });
    
    if (count < 2) return showToast('error', 'Pilih minimal 2 file');
    
    try {
        const res = await callAPI('/merge', formData);
        downloadFile(await res.blob(), 'merged.pdf');
        showToast('success', 'PDF berhasil digabungkan');
        closeModal('modal-merge');
    } catch(e) {}
}

async function doGeneric(endpoint, fileId, outputName, extraParams = {}) {
    const file = document.getElementById(fileId).files[0];
    if (!file) return showToast('error', 'Pilih file terlebih dahulu');
    
    const formData = new FormData();
    formData.append('file', file);
    for (const key in extraParams) {
        formData.append(key, extraParams[key]);
    }
    
    try {
        const res = await callAPI(endpoint, formData);
        downloadFile(await res.blob(), outputName);
        showToast('success', 'Proses berhasil');
        // Close all modals
        document.querySelectorAll('.modal').forEach(m => m.style.display = 'none');
    } catch(e) {}
}