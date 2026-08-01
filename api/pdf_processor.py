# api/pdf_processor.py
# DokPDF - Core PDF Processing

import os
import subprocess
from PyPDF2 import PdfReader, PdfWriter, PdfMerger
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
import img2pdf
from PIL import Image
import pdf2image
import shutil

class PDFProcessor:
    """Core PDF processing class for DokPDF"""
    
    def __init__(self, upload_folder):
        self.upload_folder = upload_folder
        
    def merge_pdfs(self, file_paths):
        """Gabungkan beberapa PDF menjadi satu"""
        try:
            merger = PdfMerger()
            for path in file_paths:
                merger.append(path)
            
            output_path = os.path.join(self.upload_folder, f"merged_{os.urandom(4).hex()}.pdf")
            merger.write(output_path)
            merger.close()
            return output_path
        except Exception as e:
            raise Exception(f"Error menggabungkan PDF: {str(e)}")
    
    def split_pdf(self, file_path, pages=None):
        """Pisahkan PDF berdasarkan halaman"""
        try:
            reader = PdfReader(file_path)
            writer = PdfWriter()
            total_pages = len(reader.pages)
            
            if not pages:
                output_path = os.path.join(self.upload_folder, f"split_{os.urandom(4).hex()}.pdf")
                writer = PdfWriter()
                for page in reader.pages:
                    writer.add_page(page)
                writer.write(output_path)
                return output_path
            
            for page_num in pages:
                if 1 <= page_num <= total_pages:
                    writer.add_page(reader.pages[page_num - 1])
            
            output_path = os.path.join(self.upload_folder, f"split_{os.urandom(4).hex()}.pdf")
            writer.write(output_path)
            return output_path
            
        except Exception as e:
            raise Exception(f"Error memisahkan PDF: {str(e)}")
    
    def compress_pdf(self, file_path):
        """Kompres PDF"""
        try:
            output_path = os.path.join(self.upload_folder, f"compressed_{os.urandom(4).hex()}.pdf")
            
            # Try Ghostscript first
            try:
                cmd = [
                    'gs', '-sDEVICE=pdfwrite', '-dCompatibilityLevel=1.4',
                    '-dPDFSETTINGS=/ebook', '-dNOPAUSE', '-dQUIET', '-dBATCH',
                    f'-sOutputFile={output_path}', file_path
                ]
                subprocess.run(cmd, check=True, capture_output=True)
                return output_path
            except:
                # Fallback: PyPDF2
                reader = PdfReader(file_path)
                writer = PdfWriter()
                for page in reader.pages:
                    writer.add_page(page)
                writer.write(output_path)
                return output_path
                
        except Exception as e:
            raise Exception(f"Error mengompres PDF: {str(e)}")
    
    def pdf_to_images(self, file_path, format_type='png'):
        """Konversi PDF ke gambar"""
        try:
            images = pdf2image.convert_from_path(file_path)
            output_files = []
            
            for i, image in enumerate(images):
                output_path = os.path.join(
                    self.upload_folder, 
                    f"page_{i+1}_{os.urandom(4).hex()}.{format_type}"
                )
                image.save(output_path, format_type.upper())
                output_files.append(output_path)
            
            return output_files
            
        except Exception as e:
            raise Exception(f"Error konversi PDF ke gambar: {str(e)}")
    
    def pdf_to_word(self, file_path):
        """Konversi PDF ke Word"""
        try:
            output_dir = os.path.dirname(file_path)
            output_path = os.path.join(output_dir, f"word_{os.urandom(4).hex()}.docx")
            
            try:
                cmd = [
                    'libreoffice', '--headless', '--convert-to', 'docx',
                    '--outdir', output_dir, file_path
                ]
                subprocess.run(cmd, check=True, capture_output=True)
                
                base_name = os.path.splitext(os.path.basename(file_path))[0]
                generated_file = os.path.join(output_dir, f"{base_name}.docx")
                if os.path.exists(generated_file):
                    shutil.move(generated_file, output_path)
                    return output_path
            except:
                # Fallback: simple Word doc
                from docx import Document
                doc = Document()
                doc.add_heading('DokPDF - Konversi PDF', 0)
                doc.add_paragraph('Dokumen ini dikonversi dari PDF menggunakan DokPDF.')
                doc.save(output_path)
                return output_path
                
            raise Exception("Konversi Word gagal")
            
        except Exception as e:
            raise Exception(f"Error konversi PDF ke Word: {str(e)}")
    
    def pdf_to_excel(self, file_path):
        """Konversi PDF ke Excel"""
        try:
            output_dir = os.path.dirname(file_path)
            output_path = os.path.join(output_dir, f"excel_{os.urandom(4).hex()}.xlsx")
            
            try:
                cmd = [
                    'libreoffice', '--headless', '--convert-to', 'xlsx',