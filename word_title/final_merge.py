import os
from PyPDF2 import PdfMerger

wdFormatPDF = 17

in_file = os.getcwd()
out_file = os.path.abspath("title_part")

merger = PdfMerger()
merger.append("title.pdf", pages=(0, 2))
merger.append("example.pdf")
merger.write("final_report.pdf")
merger.close()
