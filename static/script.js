const API_BASE_URL = '/api';

const translations = {
    id: {
        'hero-title': 'Apa yang ingin Anda lakukan dengan PDF?',
        'tool-merge-title': 'Gabungkan PDF',
        'tool-merge-desc': 'Gabungkan beberapa PDF menjadi satu',
        'tool-split-title': 'Pisahkan PDF',
        'tool-split-desc': 'Ambil halaman tertentu dari PDF',
        'tool-compress-title': 'Kompres PDF',
        'tool-compress-desc': 'Kecilkan ukuran file PDF',
        'tool-word-title': 'PDF ke Word',
        'tool-word-desc': 'Konversi PDF ke dokumen Word',
        'tool-excel-title': 'PDF ke Excel',
        'tool-excel-desc': 'Konversi PDF ke spreadsheet Excel',
        'tool-images-title': 'PDF ke Gambar',
        'tool-images-desc': 'Ubah halaman PDF jadi gambar',
        'tool-lock-title': 'Kunci PDF',
        'tool-lock-desc': 'Proteksi PDF dengan password',
        'tool-wm-title': 'Watermark',
        'tool-wm-desc': 'Tambahkan teks watermark',
        'modal-merge-title': 'Gabungkan PDF',
        'btn-add-file': 'Tambah File',
        'btn-merge-now': 'Gabungkan Sekarang',
        'modal-split-title': 'Pisahkan PDF',
        'ph-pages': 'Contoh: 1, 3, 5-10',
        'btn-split': 'Pisahkan',
        'modal-compress-title': 'Kompres PDF',
        'btn-compress': 'Kompres',
        'loading': 'Memproses...',
        'err-server': 'Terjadi kesalahan pada server',
        'err-min-files': 'Pilih minimal 2 file',
        'err-no-file': 'Pilih file terlebih dahulu',
        'success-process': 'Proses berhasil',
        'success-merge': 'PDF berhasil digabungkan'
    },
    en: {
        'hero-title': 'What would you like to do with PDF?',
        'tool-merge-title': 'Merge PDF',
        'tool-merge-desc': 'Combine multiple PDFs into one',
        'tool-split-title': 'Split PDF',
        'tool-split-desc': 'Extract specific pages from PDF',
        'tool-compress-title': 'Compress PDF',
        'tool-compress-desc': 'Reduce PDF file size',
        'tool-word-title': 'PDF to Word',
        'tool-word-desc': 'Convert PDF to Word document',
        'tool-excel-title': 'PDF to Excel',
        'tool-excel-desc': 'Convert PDF to Excel spreadsheet',
        'tool-images-title': 'PDF to Image',
        'tool-images-desc': 'Convert PDF pages to images',
        'tool-lock-title': 'Protect PDF',
        'tool-lock-desc': 'Protect PDF with password',
        'tool-wm-title': 'Watermark',
        'tool-wm-desc': 'Add watermark text',
        'modal-merge-title': 'Merge PDF',
        'btn-add-file': 'Add File',
        'btn-merge-now': 'Merge Now',
        'modal-split-title': 'Split PDF',
        'ph-pages': 'Example: 1, 3, 5-10',
        'btn-split': 'Split',
        'modal-compress-title': 'Compress PDF',
        'btn-compress': 'Compress',
        'loading': 'Processing...',
        'err-server': 'Server error occurred',
        'err-min-files': 'Select at least 2 files',
        'err-no-file': 'Please select a file first',
        'success-process': 'Success',
        'success-merge': 'PDF merged successfully'
    }
};

let currentLang = localStorage.getItem('lang') || 'id';
let currentTheme = localStorage.getItem('theme') || 'light';

function setLanguage(lang) {
    currentLang = lang;
    localStorage.setItem('lang', lang);
    document.getElementById('lang-toggle').textContent = lang === 'id' ? 'EN' : 'ID';
    
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        if (translations[lang][key]) el.textContent = translations[lang][key];
    });
    
    document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
        const key = el.getAttribute('data-i18n-placeholder');
        if (translations[lang][key]) el.placeholder = translations[lang][key];
    });
}

function setTheme(theme) {
    currentTheme = theme;
    localStorage.setItem('theme', theme);
    document.documentElement.setAttribute('data-theme', theme);
    const icon = document.querySelector('#theme-toggle i');
    icon.className = theme === 'light' ? 'fas fa-moon' : 'fas fa-sun';
}

document.addEventListener('DOMContentLoaded', () => {
    // Initial calls
    setLanguage(currentLang);
    setTheme(currentTheme);
    
    const langBtn = document.getElementById('lang-toggle');
    const themeBtn = document.getElementById('theme-toggle');

    if (langBtn) {
        langBtn.onclick = (e) => {
            e.preventDefault();
            setLanguage(currentLang === 'id' ? 'en' : 'id');
        };
    }
    
    if (themeBtn) {
        themeBtn.onclick = (e) => {
            e.preventDefault();
            setTheme(currentTheme === 'light' ? 'dark' : 'light');
        };
    }
});

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
            throw new Error(error.error || translations[currentLang]['err-server']);
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

function showLoading(text) {
    document.getElementById('loading-text').textContent = text || translations[currentLang]['loading'];
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
    
    if (count < 2) return showToast('error', translations[currentLang]['err-min-files']);
    
    try {
        const res = await callAPI('/merge', formData);
        downloadFile(await res.blob(), 'merged.pdf');
        showToast('success', translations[currentLang]['success-merge']);
        closeModal('modal-merge');
    } catch(e) {}
}

async function doGeneric(endpoint, fileId, outputName, extraParams = {}) {
    const file = document.getElementById(fileId).files[0];
    if (!file) return showToast('error', translations[currentLang]['err-no-file']);
    
    const formData = new FormData();
    formData.append('file', file);
    for (const key in extraParams) {
        formData.append(key, extraParams[key]);
    }
    
    try {
        const res = await callAPI(endpoint, formData);
        downloadFile(await res.blob(), outputName);
        showToast('success', translations[currentLang]['success-process']);
        // Close all modals
        document.querySelectorAll('.modal').forEach(m => m.style.display = 'none');
    } catch(e) {}
}