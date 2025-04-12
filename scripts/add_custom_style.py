import os
import glob

def inject_custom_styles():
    # documentation 폴더 내의 모든 HTML 파일 찾기
    html_files = glob.glob('book/**/*.html', recursive=True)
    
    # 추가할 CSS 내용
    custom_styles = """
    <style>
    @font-face {
        font-family: 'RIDIBatang';
        src: url('https://fastly.jsdelivr.net/gh/projectnoonnu/noonfonts_twelve@1.0/RIDIBatang.woff') format('woff');
        font-weight: normal;
        font-style: normal;
    }

    :root {
        --font-family-system: 'RIDIBatang', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    body {
        font-family: 'RIDIBatang', -apple-system, BlinkMacSystemFont, sans-serif !important;
        line-height: 180% !important;
    }

    h1, h2, h3, h4, h5, h6 {
        font-family: 'RIDIBatang', -apple-system, BlinkMacSystemFont, sans-serif !important;
        line-height: 180% !important;
    }

    div.abstract.content {
        font-family: 'RIDIBatang', -apple-system, BlinkMacSystemFont, sans-serif !important;
        line-height: 180% !important;
    }
    </style>
    """

    # 각 HTML 파일에 스타일 추가
    for html_file in html_files:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # body 태그 앞에 새로운 head 태그 삽입
        if '<body' in content:
            new_head = f'<head>{custom_styles}</head>'
            content = content.replace('<body', f'{new_head}<body')
            
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(content)

if __name__ == '__main__':
    inject_custom_styles() 