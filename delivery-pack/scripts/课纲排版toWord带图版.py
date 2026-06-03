"""
课纲排版 - Markdown 转 Word（带图片版）
自动在指定位置插入 images/ 文件夹中的图片

图片插入位置：
1. "主讲人介绍" 章节末尾 → 讲师照片
2. "课件展示" 或 "五、" 章节 → 课件截图（如有）
3. "课程现场" 或 "六、" 章节 → 现场照片（如有）
4. "现场准备" 或 "课前准备" 章节末尾 → 电脑配置

使用方法：
    python 课纲排版toWord带图版.py --input "课纲.md"
    # 生成：课纲_带图.docx
"""

import argparse
import os
import re
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn, nsdecls
from docx.oxml import parse_xml

# 路径配置
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(SCRIPT_DIR, '..', 'images')

# 图片文件名配置
IMAGE_FILES = {
    'lecturer': ['讲师照片1.jpg', '讲师照片1.png', '讲师照片1.jpeg'],
    'slides': ['课件展示1.jpg', '课件展示1.png', '课件展示1.jpeg'],
    'scene1': ['现场照片1.jpg', '现场照片1.png', '现场照片1.jpeg'],
    'scene2': ['现场照片2.jpg', '现场照片2.png', '现场照片2.jpeg'],
    'scene3': ['现场照片3.jpg', '现场照片3.png', '现场照片3.jpeg'],
    'scene4': ['现场照片4.jpg', '现场照片4.png', '现场照片4.jpeg'],
    'computer': ['讲师电脑.jpg', '讲师电脑.png', '讲师电脑.jpeg'],
}

# 图片说明文字配置
IMAGE_CAPTIONS = {
    'lecturer': '（讲师近照）',
    'slides': '（课件展示截图）',
    'scenes': '（培训现场照片）',
    'computer': '（老师使用自己的华为电脑演示课程，电脑接口如上图所示）',
}

# 颜色配置
ORANGE = RGBColor(0xFF, 0x6B, 0x35)
LIGHT_ORANGE_HEX = "FFF5EE"
BLACK = RGBColor(0x1A, 0x1A, 0x1A)
GRAY = RGBColor(0x66, 0x66, 0x66)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)

def find_image(key):
    """查找图片文件"""
    for filename in IMAGE_FILES.get(key, []):
        path = os.path.join(IMAGES_DIR, filename)
        if os.path.exists(path):
            return path
    return None

def set_font(run, name='微软雅黑', size=11, bold=False, color=BLACK):
    """设置字体样式"""
    run.font.name = name
    run._element.rPr.rFonts.set(qn('w:eastAsia'), name)
    run.font.size = Pt(size)
    run.font.bold = bold
    if color:
        run.font.color.rgb = color

def add_caption(doc, text):
    """添加居中小字图片说明"""
    para = doc.add_paragraph()
    para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    para.paragraph_format.space_before = Pt(2)
    para.paragraph_format.space_after = Pt(6)
    run = para.add_run(text)
    set_font(run, size=9, color=GRAY)

def add_centered_image(doc, image_path, width_cm, caption=None):
    """添加居中图片，可选说明文字"""
    if not image_path or not os.path.exists(image_path):
        return False
    para = doc.add_paragraph()
    para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = para.add_run()
    run.add_picture(image_path, width=Cm(width_cm))
    if caption:
        add_caption(doc, caption)
    else:
        doc.add_paragraph()  # 间距
    return True

def add_image_row(doc, image_paths, width_cm_each, caption=None):
    """添加一行并排图片，可选说明文字"""
    valid_paths = [p for p in image_paths if p and os.path.exists(p)]
    if not valid_paths:
        return False
    
    table = doc.add_table(rows=1, cols=len(valid_paths))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    
    for cell, img_path in zip(table.row_cells(0), valid_paths):
        para = cell.paragraphs[0]
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = para.add_run()
        run.add_picture(img_path, width=Cm(width_cm_each))
    
    if caption:
        add_caption(doc, caption)
    else:
        doc.add_paragraph()
    return True

def parse_markdown(md_content):
    """解析 Markdown 内容"""
    lines = md_content.split('\n')
    elements = []
    current_table = []
    in_table = False
    
    for line in lines:
        line = line.rstrip('\r')
        
        # 表格处理
        if line.startswith('|'):
            in_table = True
            current_table.append(line)
            continue
        elif in_table:
            elements.append(('table', current_table))
            current_table = []
            in_table = False
        
        # 空行
        if not line.strip():
            continue
        
        # 分隔线
        if line.strip() == '---':
            continue
        
        # 标题
        if line.startswith('# '):
            elements.append(('h1', line[2:].strip()))
        elif line.startswith('## ——'):
            elements.append(('subtitle', line[3:].strip()))
        elif line.startswith('## '):
            elements.append(('h2', line[3:].strip()))
        elif line.startswith('### '):
            elements.append(('h3', line[4:].strip()))
        elif line.startswith('##### '):
            elements.append(('h5', line[6:].strip()))
        elif line.startswith('#### '):
            elements.append(('h4', line[5:].strip()))
        # 引用块
        elif line.startswith('> '):
            elements.append(('quote', line[2:].strip()))
        # 列表
        elif line.startswith('- '):
            elements.append(('bullet', line[2:].strip()))
        elif re.match(r'^\d+\. ', line):
            elements.append(('numbered', re.sub(r'^\d+\. ', '', line).strip()))
        # 普通段落
        else:
            elements.append(('paragraph', line.strip()))
    
    # 处理最后的表格
    if current_table:
        elements.append(('table', current_table))
    
    return elements

def add_h1(doc, text):
    """橙色横幅标题"""
    para = doc.add_paragraph()
    para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="FF6B35"/>')
    para._p.get_or_add_pPr().append(shading)
    para.paragraph_format.space_before = Pt(12)
    para.paragraph_format.space_after = Pt(12)
    run = para.add_run(text)
    set_font(run, size=18, bold=True, color=WHITE)

def add_subtitle(doc, text):
    """灰色右对齐副标题"""
    para = doc.add_paragraph()
    para.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run = para.add_run(text)
    set_font(run, size=11, color=GRAY)

def add_h2(doc, text):
    """橙色加粗二级标题"""
    para = doc.add_paragraph()
    para.paragraph_format.space_before = Pt(18)
    para.paragraph_format.space_after = Pt(6)
    run = para.add_run(text)
    set_font(run, size=16, bold=True, color=ORANGE)

def add_h3(doc, text):
    """左侧橙色竖线三级标题"""
    para = doc.add_paragraph()
    para.paragraph_format.space_before = Pt(12)
    para.paragraph_format.space_after = Pt(6)
    pPr = para._p.get_or_add_pPr()
    pBdr = parse_xml(
        f'<w:pBdr {nsdecls("w")}>'
        f'<w:left w:val="single" w:sz="24" w:space="4" w:color="FF6B35"/>'
        f'</w:pBdr>'
    )
    pPr.append(pBdr)
    run = para.add_run(text)
    set_font(run, size=14, bold=True, color=BLACK)

def add_h4(doc, text):
    """黑色加粗四级标题"""
    para = doc.add_paragraph()
    para.paragraph_format.space_before = Pt(18)
    para.paragraph_format.space_after = Pt(3)
    run = para.add_run(text)
    set_font(run, size=12, bold=True, color=BLACK)

def add_h5(doc, text):
    """黑色加粗五级标题（模块标题）"""
    para = doc.add_paragraph()
    para.paragraph_format.space_before = Pt(18)
    para.paragraph_format.space_after = Pt(3)
    run = para.add_run(text)
    set_font(run, size=11, bold=True, color=BLACK)

def add_quote(doc, text):
    """灰色背景引用块"""
    para = doc.add_paragraph()
    shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="F7F7F7"/>')
    para._p.get_or_add_pPr().append(shading)
    para.paragraph_format.space_before = Pt(6)
    para.paragraph_format.space_after = Pt(6)
    para.paragraph_format.left_indent = Cm(0.5)
    run = para.add_run(text)
    set_font(run, size=10, color=GRAY)
    run.italic = True

def add_bullet(doc, text):
    """无序列表"""
    para = doc.add_paragraph(style='List Bullet')
    para.paragraph_format.space_before = Pt(3)
    para.paragraph_format.space_after = Pt(3)
    # 处理加粗文本
    parts = re.split(r'(\*\*[^*]+\*\*)', text)
    for part in parts:
        if part.startswith('**') and part.endswith('**'):
            run = para.add_run(part[2:-2])
            set_font(run, size=11, bold=True, color=BLACK)
        else:
            run = para.add_run(part)
            set_font(run, size=11, color=BLACK)

def add_numbered(doc, text):
    """有序列表"""
    para = doc.add_paragraph(style='List Number')
    para.paragraph_format.space_before = Pt(3)
    para.paragraph_format.space_after = Pt(3)
    # 处理加粗文本
    parts = re.split(r'(\*\*[^*]+\*\*)', text)
    for part in parts:
        if part.startswith('**') and part.endswith('**'):
            run = para.add_run(part[2:-2])
            set_font(run, size=11, bold=True, color=BLACK)
        else:
            run = para.add_run(part)
            set_font(run, size=11, color=BLACK)

def add_paragraph(doc, text):
    """普通段落"""
    para = doc.add_paragraph()
    para.paragraph_format.space_before = Pt(3)
    para.paragraph_format.space_after = Pt(3)
    # 处理加粗文本
    parts = re.split(r'(\*\*[^*]+\*\*)', text)
    for part in parts:
        if part.startswith('**') and part.endswith('**'):
            run = para.add_run(part[2:-2])
            set_font(run, size=11, bold=True, color=BLACK)
        else:
            run = para.add_run(part)
            set_font(run, size=11, color=BLACK)

def add_table(doc, table_lines):
    """添加表格（飞书风格）"""
    # 解析表格
    rows = []
    for line in table_lines:
        if '---' in line:
            continue
        cells = [c.strip() for c in line.strip('|').split('|')]
        if cells:
            rows.append(cells)
    
    if not rows:
        return
    
    # 创建表格
    table = doc.add_table(rows=len(rows), cols=len(rows[0]))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    
    for i, row_data in enumerate(rows):
        for j, cell_text in enumerate(row_data):
            cell = table.cell(i, j)
            para = cell.paragraphs[0]
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER if i == 0 else WD_ALIGN_PARAGRAPH.LEFT
            
            # 设置单元格样式
            tc = cell._tc
            tcPr = tc.get_or_add_tcPr()
            
            if i == 0:  # 表头：橙色背景
                shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="FF6B35"/>')
                tcPr.append(shading)
                run = para.add_run(cell_text)
                set_font(run, size=10, bold=True, color=WHITE)
            elif j == 0:  # 首列：浅橙色背景
                shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{LIGHT_ORANGE_HEX}"/>')
                tcPr.append(shading)
                run = para.add_run(cell_text)
                set_font(run, size=10, bold=True, color=BLACK)
            else:  # 其他单元格
                run = para.add_run(cell_text)
                set_font(run, size=10, color=BLACK)
    
    doc.add_paragraph()  # 表格后间距

def convert_md_to_docx(input_path, output_path):
    """转换 Markdown 到 Word"""
    print("=" * 50)
    print("课纲排版 - Markdown 转 Word（带图片版）")
    print("=" * 50)
    
    # 读取 Markdown
    with open(input_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # 解析 Markdown
    elements = parse_markdown(md_content)
    
    # 创建 Word 文档
    doc = Document()
    
    # 设置页面边距
    for section in doc.sections:
        section.top_margin = Cm(2.5)
        section.bottom_margin = Cm(2)
        section.left_margin = Cm(2.5)
        section.right_margin = Cm(2.5)
    
    # 图片插入标记
    inserted_images = {
        'lecturer': False,
        'slides': False,
        'scenes': False,
        'computer': False,
    }
    current_section = ""
    
    # 渲染内容
    for elem_type, content in elements:
        # 跟踪当前章节
        if elem_type == 'h2':
            current_section = content
            
            # 在进入新章节前，检查是否需要插入图片
            if '主讲人介绍' in current_section and not inserted_images['lecturer']:
                pass  # 在章节内容后插入
        
        # 渲染元素
        if elem_type == 'h1':
            add_h1(doc, content)
        elif elem_type == 'subtitle':
            add_subtitle(doc, content)
        elif elem_type == 'h2':
            # 在章节标题前，检查上一章节是否需要插入图片
            add_h2(doc, content)
        elif elem_type == 'h3':
            # 检查上一个 h3 是否是特定章节，需要插入图片
            add_h3(doc, content)
        elif elem_type == 'h4':
            add_h4(doc, content)
        elif elem_type == 'h5':
            add_h5(doc, content)
        elif elem_type == 'quote':
            add_quote(doc, content)
        elif elem_type == 'bullet':
            add_bullet(doc, content)
            # 在主讲人介绍的列表后插入讲师照片
            if '主讲人介绍' in current_section and not inserted_images['lecturer']:
                # 检查是否是最后一个列表项（通过内容判断）
                if '有成果' in content or '愿景' in content or '交付' in content:
                    pass  # 等列表结束后插入
            # 在"电脑"相关内容后插入电脑配置图片
            if ('电脑' in content or 'HDMI' in content) and not inserted_images['computer']:
                print("\n📷 插入电脑配置...")
                if add_centered_image(doc, find_image('computer'), 12, IMAGE_CAPTIONS.get('computer')):
                    inserted_images['computer'] = True
                    print("  ✓ 电脑配置已插入")
        elif elem_type == 'numbered':
            add_numbered(doc, content)
        elif elem_type == 'paragraph':
            add_paragraph(doc, content)
            # 在主讲人介绍的段落后插入讲师照片
            if '主讲人介绍' in current_section and not inserted_images['lecturer']:
                if '交付' in content or '好评率' in content or '客户' in content:
                    print("\n📷 插入讲师照片...")
                    if add_centered_image(doc, find_image('lecturer'), 10, IMAGE_CAPTIONS.get('lecturer')):
                        inserted_images['lecturer'] = True
                        print("  ✓ 讲师照片已插入")
        elif elem_type == 'table':
            add_table(doc, content)
        
        # 检查是否需要在章节后插入图片
        if elem_type == 'h2':
            # 课件展示章节
            if '课件展示' in content or '五、' in content:
                print("\n📷 插入课件展示...")
                if add_centered_image(doc, find_image('slides'), 14, IMAGE_CAPTIONS.get('slides')):
                    inserted_images['slides'] = True
                    print("  ✓ 课件展示已插入")
            
            # 课程现场章节
            if '课程现场' in content or '六、' in content:
                print("\n📷 插入课程现场照片...")
                row1 = add_image_row(doc, [find_image('scene1'), find_image('scene2')], 7)
                row2 = add_image_row(doc, [find_image('scene3'), find_image('scene4')], 7, IMAGE_CAPTIONS.get('scenes'))
                if row1 or row2:
                    inserted_images['scenes'] = True
                    print("  ✓ 课程现场照片已插入")
            
            # 培训准备/课前准备章节
            if '培训准备' in content or '现场准备' in content or '课前准备' in content:
                # 电脑配置图片放在章节末尾，后面处理
                pass
    
    # 在文档末尾检查是否还有未插入的图片（备用，正常情况下应已在“电脑”内容后插入）
    if not inserted_images['computer']:
        print("\n📷 插入电脑配置（备用位置）...")
        if add_centered_image(doc, find_image('computer'), 12, IMAGE_CAPTIONS.get('computer')):
            inserted_images['computer'] = True
            print("  ✓ 电脑配置已插入")
    
    # 保存文档
    doc.save(output_path)
    
    print("\n" + "=" * 50)
    print(f"✅ 转换完成：{output_path}")
    print("=" * 50)
    
    # 汇总插入的图片
    print("\n图片插入情况：")
    for key, inserted in inserted_images.items():
        status = "✓" if inserted else "✗"
        print(f"  {status} {key}")

def main():
    parser = argparse.ArgumentParser(description='课纲排版 - Markdown 转 Word（带图片版）')
    parser.add_argument('--input', '-i', required=True, help='输入的 Markdown 文件路径')
    parser.add_argument('--output', '-o', help='输出的 Word 文件路径（默认为同名_带图.docx）')
    
    args = parser.parse_args()
    
    input_path = args.input
    if not os.path.exists(input_path):
        print(f"❌ 文件不存在：{input_path}")
        return
    
    if args.output:
        output_path = args.output
    else:
        base = os.path.splitext(input_path)[0]
        output_path = f"{base}_带图.docx"
    
    convert_md_to_docx(input_path, output_path)

if __name__ == "__main__":
    main()
