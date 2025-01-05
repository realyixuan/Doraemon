"""
generate diary pdf named out.pdf in current directory 
from a folder, in which all files will be convert to pdf.

you should set `source folder` and `year` in entry function

"""
import os
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import letter

pdfmetrics.registerFont(TTFont('PingFang', './PingFang Regular.ttf'))
c = canvas.Canvas("out.pdf")

def split_line_to_word(line):
    words = []
    def is_ascii_word(char): return ord(char) < 128
    i = 0
    while i < len(line):
        if not is_ascii_word(line[i]):
            words.append(line[i])
        else:
            if line[i].isalnum():
                j = i
                while i < len(line):
                    if not line[i].isalnum():
                        i -= 1
                        break
                    i += 1
                words.append(line[j:i+1])
            else:
                words.append(line[i])

        i += 1
    return words


def generate_pdf(filepath):
    filename = filepath.split('/')[-1]
    c.bookmarkPage(filename)  # Create a bookmark for sidebar navigation
    c.addOutlineEntry(filename, filename, level=0)
    c.setFont("Helvetica", 22)
    y = 750  # 起始高度
    c.drawString(70, y, f"{filename}")
    y -= 50
    page_width, page_height = letter
    with open(filepath) as f:
        c.setFont("PingFang", 14)
        for line in f:
            if y < 50:  # 换页
                c.showPage()
                y = 800
                c.setFont("PingFang", 14)
            left_width = 70
            for word in split_line_to_word(line):
                word_width = c.stringWidth(word, "PingFang", 14)
                if left_width + word_width < page_width - 70:
                    c.drawString(left_width, y, word)
                    left_width += word_width
                else:
                    left_width = 70
                    y -= 20
                    if y < 50:  # 换页
                        c.showPage()
                        y = 800
                        c.setFont("PingFang", 14)
                    c.drawString(left_width, y, word)
                    left_width += word_width
            y -= 20
                    

def generate_pdf_by_dir(folder_path, year):
    c.setFont("Helvetica-Oblique", 30)
    x = 100
    y = 750 
    c.drawString(x, y, f"Diary {year}")

    y -= 30

    c.setFont("Helvetica-Oblique", 14)
    for filename in sorted(os.listdir(folder_path)):
        y -= 25 
        c.drawString(x, y, filename)
        c.linkRect(
            "",
            filename,
            Rect=(x - 5, y - 5, x + 50, y + 15),
            thickness=0,
            color=None,
        )
        if y < 100:  # 换页
            c.showPage()
            y = 750
            c.setFont("Helvetica-Oblique", 14)

    c.showPage()
    for filename in sorted(os.listdir(folder_path)):
        print(filename)
        file_path = os.path.join(folder_path, filename)
        generate_pdf(file_path)
        c.showPage()
    c.save()


if __name__ == '__main__':
    generate_pdf_by_dir("./2023", 2023)

