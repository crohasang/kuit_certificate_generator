import json
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import io
import os
import gc

def create_overlay(name, part, project):
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=A4)
    
    # 폰트 설정
    font_path = 'assets/fonts/NanumMyeongjoBold.ttf'
    font_name = 'NanumMyeongjoBold'
    if font_name not in pdfmetrics.getRegisteredFontNames():
        pdfmetrics.registerFont(TTFont(font_name, font_path))
    
    can.setFont(font_name, 16)
    
    # 위치 조정값
    name_x, name_y = 178, 575  # 성명
    part_x, part_y = 178, 545  # 파트
    project_x, project_y = 178, 485  # 프로젝트
    
    # 텍스트 그리기
    can.drawString(name_x, name_y, name)
    can.drawString(part_x, part_y, part)
    can.drawString(project_x, project_y, project)
    
    can.save()
    packet.seek(0)
    return PdfReader(packet)

def generate_certificate(template_path, name, part, project, output_dir):
    try:
        # 각 멤버마다 새로운 template reader 생성
        template_reader = PdfReader(template_path)
        page = template_reader.pages[0]
        
        # 오버레이 생성 및 합치기
        overlay = create_overlay(name, part, project)
        page.merge_page(overlay.pages[0])
        
        # 새로운 PDF writer 생성
        writer = PdfWriter()
        writer.add_page(page)
        
        # PDF 저장
        output_path = os.path.join(output_dir, f"{name}_{project}.pdf")
        with open(output_path, "wb") as output_file:
            writer.write(output_file)
        
        print(f"Generated certificate for {name} - {project}")
        
    except Exception as e:
        print(f"Error processing certificate for {name}: {str(e)}")
    finally:
        # 메모리 정리
        del template_reader
        del overlay
        del writer
        gc.collect()

def generate_certificates():
    try:
        # output 디렉토리 생성
        output_dir = 'output/certificates'
        os.makedirs(output_dir, exist_ok=True)
        
        # JSON 파일 읽기
        with open('data/data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        template_path = 'template/template.pdf'
        print("\nStarting certificate generation...")
        
        for project in data:
            project_name = project['project']
            print(f"\n=== Processing Project: {project_name} ===")
            
            for member in project['members']:
                generate_certificate(
                    template_path,
                    member['name'].strip(),
                    member['part'].strip(),
                    project_name.strip(),
                    output_dir
                )
        
        print(f"\nAll certificates have been generated in {output_dir}")
        
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
    finally:
        gc.collect()

if __name__ == "__main__":
    generate_certificates()