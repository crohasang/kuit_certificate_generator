import json
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import io
import os
import gc

def create_overlay(name, role, study_part, project_participation):
    """
    certificate.pdf에 삽입할 텍스트 오버레이를 생성합니다.
    """
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=A4)
    
    # 폰트 설정
    font_path = 'assets/fonts/Pretendard-Medium.ttf'
    font_name = 'Pretendard'
    if font_name not in pdfmetrics.getRegisteredFontNames():
        try:
            pdfmetrics.registerFont(TTFont(font_name, font_path))
        except OSError:
            print(f"Warning: Font file not found at {font_path}. Using a default font.")
            font_name = 'Helvetica' # 대체 폰트
    
    # 글씨 색상을 흰색으로 설정
    can.setFillColorRGB(1, 1, 1)
    
    # 새로운 템플릿에 맞춘 텍스트 위치 조정값
    # 더 아래로 이동하기 위해 y 좌표를 조정했습니다.
    # 이 값은 미세 조정이 필요할 수 있습니다.
    name_x, name_y = 84, 200
    role_x, role_y = 125, 295    # Role 필드
    study_part_x, study_part_y = 165, 273 # Study Part 필드
    project_x, project_y = 225, 252  # Project participation 필드

    # 이름 폰트 크기를 32으로 설정
    can.setFont(font_name, 32)
    can.drawString(name_x, name_y, name)
    
    # 나머지 필드는 폰트 크기를 14로 설정
    can.setFont(font_name, 14)
    can.drawString(role_x, role_y, role)
    can.drawString(study_part_x, study_part_y, study_part)
    
    # Project participation 텍스트가 길어질 경우를 대비해 폰트 크기를 조절하거나 줄 바꿈을 고려할 수 있습니다.
    can.drawString(project_x, project_y, project_participation)
    
    can.save()
    packet.seek(0)
    return PdfReader(packet)

def generate_certificate(template_path, name, role, study_part, project_participation, output_dir):
    """
    하나의 수료증을 생성하고 저장합니다.
    """
    try:
        # 각 멤버마다 새로운 template reader 생성
        template_reader = PdfReader(template_path)
        page = template_reader.pages[0]
        
        # 오버레이 생성 및 합치기
        overlay = create_overlay(name, role, study_part, project_participation)
        page.merge_page(overlay.pages[0])
        
        # 새로운 PDF writer 생성
        writer = PdfWriter()
        writer.add_page(page)
        
        # PDF 저장
        # 파일명에 공백, 쉼표를 제거하여 안전하게 만듭니다.
        safe_project_name = project_participation.replace(' ', '_').replace(',', '')
        output_path = os.path.join(output_dir, f"{name}_{safe_project_name}.pdf")
        with open(output_path, "wb") as output_file:
            writer.write(output_file)
        
        print(f"Generated certificate for {name} ({project_participation})")
        
    except Exception as e:
        print(f"Error processing certificate for {name}: {str(e)}")
    finally:
        # 메모리 정리
        del template_reader
        del overlay
        del writer
        gc.collect()

def generate_certificates():
    """
    JSON 데이터를 기반으로 모든 수료증을 생성합니다.
    """
    try:
        # output 디렉토리 생성
        output_dir = 'output/certificates'
        os.makedirs(output_dir, exist_ok=True)
        
        # JSON 파일 읽기
        with open('data/data.json', 'r', encoding='utf-8') as f:
            members_data = json.load(f)
        
        template_path = 'template/template.pdf'
        print("\nStarting certificate generation...")
        
        # 각 멤버의 데이터를 순회하며 수료증 생성
        for member in members_data:
            generate_certificate(
                template_path,
                member['name'].strip(),
                member['role'].strip(),
                member['study_part'].strip(),
                member['project_participation'].strip(),
                output_dir
            )
        
        print(f"\nAll certificates have been generated in {output_dir}")
        
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
    finally:
        gc.collect()

if __name__ == "__main__":
    generate_certificates()
