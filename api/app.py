# api/app.py
# DokPDF - Kelola PDF Jadi Mudah
# Backend API Service

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import uuid
import json
import shutil
from datetime import datetime
from pdf_processor import PDFProcessor
from utils import allowed_file, get_file_size, cleanup_temp_files

app = Flask(__name__)
CORS(app)

# Configuration
app.config['MAX_CONTENT_LENGTH'] = 150 * 1024 * 1024  # 150MB
app.config['UPLOAD_FOLDER'] = 'uploads/temp'
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'png', 'jpg', 'jpeg'}

# Create upload folder
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

pdf_processor = PDFProcessor(app.config['UPLOAD_FOLDER'])

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'app': 'DokPDF',
        'version': '1.0.0',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/info', methods=['GET'])
def app_info():
    """Get application info"""
    return jsonify({
        'name': 'DokPDF',
        'tagline': 'Kelola PDF Jadi Mudah',
        'version': '1.0.0',
        'features': [
            'Gabungkan PDF',
            'Pisahkan PDF',
            'Kompres PDF',
            'PDF ke Word',
            'PDF ke Excel',
            'PDF ke PPT',
            'PDF ke Gambar',
            'Kunci PDF',
            'Buka Kunci PDF',
            'Watermark PDF',
            'Atur Halaman',
            'Tanda Tangan'
        ]
    })

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Upload file for processing"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'Tidak ada file yang diunggah'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'Tidak ada file yang dipilih'}), 400
        
        if not allowed_file(file.filename, app.config['ALLOWED_EXTENSIONS']):
            return jsonify({'error': 'Format file tidak didukung'}), 400
        
        original_filename = file.filename
        ext = original_filename.rsplit('.', 1)[1].lower()
        filename = f"{uuid.uuid4().hex}.{ext}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        file.save(filepath)
        size = get_file_size(filepath)
        
        return jsonify({
            'success': True,
            'filename': filename,
            'original_name': original_filename,
            'size': size,
            'message': 'File berhasil diunggah'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============== PDF OPERATIONS ==============

@app.route('/api/merge', methods=['POST'])
def merge_pdfs():
    """Gabungkan PDF"""
    try:
        files = request.files.getlist('files')
        if not files or len(files) < 2:
            return jsonify({'error': 'Minimal 2 file PDF untuk digabungkan'}), 400
        
        saved_files = []
        for file in files:
            if file and allowed_file(file.filename, app.config['ALLOWED_EXTENSIONS']):
                filename = f"{uuid.uuid4().hex}.pdf"
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                saved_files.append(filepath)
        
        output_file = pdf_processor.merge_pdfs(saved_files)
        
        return send_file(
            output_file,
            as_attachment=True,
            download_name='gabungan.pdf',
            mimetype='application/pdf'
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cleanup_temp_files(app.config['UPLOAD_FOLDER'], 
                          saved_files if 'saved_files' in locals() else [])

@app.route('/api/split', methods=['POST'])
def split_pdf():
    """Pisahkan PDF"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'Tidak ada file yang diunggah'}), 400
        
        file = request.files['file']
        pages = request.form.get('pages', '')
        
        if not file or file.filename == '':
            return jsonify({'error': 'Tidak ada file yang dipilih'}), 400
        
        filename = f"{uuid.uuid4().hex}.pdf"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Parse pages
        page_list = []
        if pages:
            for part in pages.split(','):
                part = part.strip()
                if '-' in part:
                    start, end = part.split('-')
                    page_list.extend(range(int(start), int(end) + 1))
                else:
                    page_list.append(int(part))
        
        output_file = pdf_processor.split_pdf(filepath, page_list)
        
        return send_file(
            output_file,
            as_attachment=True,
            download_name='pisahan.pdf',
            mimetype='application/pdf'
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cleanup_temp_files(app.config['UPLOAD_FOLDER'], 
                          [filepath] if 'filepath' in locals() else [])

@app.route('/api/compress', methods=['POST'])
def compress_pdf():
    """Kompres PDF"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'Tidak ada file yang diunggah'}), 400
        
        file = request.files['file']
        if not file or file.filename == '':
            return jsonify({'error': 'Tidak ada file yang dipilih'}), 400
        
        filename = f"{uuid.uuid4().hex}.pdf"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        output_file = pdf_processor.compress_pdf(filepath)
        
        return send_file(
            output_file,
            as_attachment=True,
            download_name='dikompres.pdf',
            mimetype='application/pdf'
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cleanup_temp_files(app.config['UPLOAD_FOLDER'], 
                          [filepath] if 'filepath' in locals() else [])

@app.route('/api/pdf-to-images', methods=['POST'])
def pdf_to_images():
    """PDF ke Gambar"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'Tidak ada file yang diunggah'}), 400
        
        file = request.files['file']
        format_type = request.form.get('format', 'png')
        
        if not file or file.filename == '':
            return jsonify({'error': 'Tidak ada file yang dipilih'}), 400
        
        filename = f"{uuid.uuid4().hex}.pdf"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        output_files = pdf_processor.pdf_to_images(filepath, format_type)
        
        # Create zip
        import zipfile
        zip_filename = f"{uuid.uuid4().hex}.zip"
        zip_path = os.path.join(app.config['UPLOAD_FOLDER'], zip_filename)
        
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for img_path in output_files:
                zipf.write(img_path, os.path.basename(img_path))
        
        return send_file(
            zip_path,
            as_attachment=True,
            download_name='gambar-pdf.zip',
            mimetype='application/zip'
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/pdf-to-word', methods=['POST'])
def pdf_to_word():
    """PDF ke Word"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'Tidak ada file yang diunggah'}), 400
        
        file = request.files['file']
        if not file or file.filename == '':
            return jsonify({'error': 'Tidak ada file yang dipilih'}), 400
        
        filename = f"{uuid.uuid4().hex}.pdf"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        output_file = pdf_processor.pdf_to_word(filepath)
        
        return send_file(
            output_file,
            as_attachment=True,
            download_name='dokumen.docx',
            mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cleanup_temp_files(app.config['UPLOAD_FOLDER'], 
                          [filepath] if 'filepath' in locals() else [])

@app.route('/api/pdf-to-excel', methods=['POST'])
def pdf_to_excel():
    """PDF ke Excel"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'Tidak ada file yang diunggah'}), 400
        
        file = request.files['file']
        if not file or file.filename == '':
            return jsonify({'error': 'Tidak ada file yang dipilih'}), 400
        
        filename = f"{uuid.uuid4().hex}.pdf"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        output_file = pdf_processor.pdf_to_excel(filepath)
        
        return send_file(
            output_file,
            as_attachment=True,
            download_name='spreadsheet.xlsx',
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cleanup_temp_files(app.config['UPLOAD_FOLDER'], 
                          [filepath] if 'filepath' in locals() else [])

@app.route('/api/pdf-to-ppt', methods=['POST'])
def pdf_to_ppt():
    """PDF ke PPT"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'Tidak ada file yang diunggah'}), 400
        
        file = request.files['file']
        if not file or file.filename == '':
            return jsonify({'error': 'Tidak ada file yang dipilih'}), 400
        
        filename = f"{uuid.uuid4().hex}.pdf"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        output_file = pdf_processor.pdf_to_ppt(filepath)
        
        return send_file(
            output_file,
            as_attachment=True,
            download_name='presentasi.pptx',
            mimetype='application/vnd.openxmlformats-officedocument.presentationml.presentation'
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cleanup_temp_files(app.config['UPLOAD_FOLDER'], 
                          [filepath] if 'filepath' in locals() else [])

@app.route('/api/lock-pdf', methods=['POST'])
def lock_pdf():
    """Kunci PDF dengan Password"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'Tidak ada file yang diunggah'}), 400
        
        file = request.files['file']
        password = request.form.get('password', '')
        
        if not password or len(password) < 8:
            return jsonify({'error': 'Password minimal 8 karakter'}), 400
        
        if not file or file.filename == '':
            return jsonify({'error': 'Tidak ada file yang dipilih'}), 400
        
        filename = f"{uuid.uuid4().hex}.pdf"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        output_file = pdf_processor.lock_pdf(filepath, password)
        
        return send_file(
            output_file,
            as_attachment=True,
            download_name='terkunci.pdf',
            mimetype='application/pdf'
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cleanup_temp_files(app.config['UPLOAD_FOLDER'], 
                          [filepath] if 'filepath' in locals() else [])

@app.route('/api/unlock-pdf', methods=['POST'])
def unlock_pdf():
    """Buka Kunci PDF"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'Tidak ada file yang diunggah'}), 400
        
        file = request.files['file']
        password = request.form.get('password', '')
        
        if not password:
            return jsonify({'error': 'Password diperlukan'}), 400
        
        if not file or file.filename == '':
            return jsonify({'error': 'Tidak ada file yang dipilih'}), 400
        
        filename = f"{uuid.uuid4().hex}.pdf"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        output_file = pdf_processor.unlock_pdf(filepath, password)
        
        return send_file(
            output_file,
            as_attachment=True,
            download_name='terbuka.pdf',
            mimetype='application/pdf'
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cleanup_temp_files(app.config['UPLOAD_FOLDER'], 
                          [filepath] if 'filepath' in locals() else [])

@app.route('/api/add-watermark', methods=['POST'])
def add_watermark():
    """Tambahkan Watermark"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'Tidak ada file yang diunggah'}), 400
        
        file = request.files['file']
        text = request.form.get('text', 'DokPDF')
        pages = request.form.get('pages', '')
        
        if not file or file.filename == '':
            return jsonify({'error': 'Tidak ada file yang dipilih'}), 400
        
        filename = f"{uuid.uuid4().hex}.pdf"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Parse pages
        page_list = []
        if pages:
            for part in pages.split(','):
                part = part.strip()
                if '-' in part:
                    start, end = part.split('-')
                    page_list.extend(range(int(start), int(end) + 1))
                else:
                    page_list.append(int(part))
        
        output_file = pdf_processor.add_watermark(filepath, text, page_list)
        
        return send_file(
            output_file,
            as_attachment=True,
            download_name='berwatermark.pdf',
            mimetype='application/pdf'
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cleanup_temp_files(app.config['UPLOAD_FOLDER'], 
                          [filepath] if 'filepath' in locals() else [])

@app.route('/api/organize-pdf', methods=['POST'])
def organize_pdf():
    """Atur Halaman PDF"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'Tidak ada file yang diunggah'}), 400
        
        file = request.files['file']
        operations = request.form.get('operations', '{}')
        
        if not file or file.filename == '':
            return jsonify({'error': 'Tidak ada file yang dipilih'}), 400
        
        filename = f"{uuid.uuid4().hex}.pdf"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        ops = json.loads(operations)
        output_file = pdf_processor.organize_pdf(filepath, ops)
        
        return send_file(
            output_file,
            as_attachment=True,
            download_name='teratur.pdf',
            mimetype='application/pdf'
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cleanup_temp_files(app.config['UPLOAD_FOLDER'], 
                          [filepath] if 'filepath' in locals() else [])

@app.route('/api/add-signature', methods=['POST'])
def add_signature():
    """Tambahkan Tanda Tangan"""
    try:
        if 'pdf' not in request.files or 'signature' not in request.files:
            return jsonify({'error': 'PDF dan gambar tanda tangan diperlukan'}), 400
        
        pdf_file = request.files['pdf']
        sig_file = request.files['signature']
        position = request.form.get('position', 'bottom-right')
        
        if not pdf_file or pdf_file.filename == '':
            return jsonify({'error': 'Tidak ada PDF yang dipilih'}), 400
        
        pdf_filename = f"{uuid.uuid4().hex}.pdf"
        pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf_filename)
        pdf_file.save(pdf_path)
        
        sig_filename = f"{uuid.uuid4().hex}.png"
        sig_path = os.path.join(app.config['UPLOAD_FOLDER'], sig_filename)
        sig_file.save(sig_path)
        
        output_file = pdf_processor.add_signature(pdf_path, sig_path, position)
        
        return send_file(
            output_file,
            as_attachment=True,
            download_name='bertandatangan.pdf',
            mimetype='application/pdf'
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cleanup_temp_files(app.config['UPLOAD_FOLDER'], 
                          [pdf_path, sig_path] if 'pdf_path' in locals() and 'sig_path' in locals() else [])

if __name__ == '__main__':
    print("=" * 50)
    print("📄 DokPDF - Kelola PDF Jadi Mudah")
    print("=" * 50)
    print(f"🚀 API Server running on http://0.0.0.0:5000")
    print(f"📁 Upload folder: {app.config['UPLOAD_FOLDER']}")
    print("=" * 50)
    app.run(host='0.0.0.0', port=5000, debug=False)