import PyPDF2
from pathlib import Path
import math
import numpy
path_to_pdf="path-to-pdf"
number_of_pages_in_signature = 5  #needs to be an odd number, don't think this code works for even numbers
pdf_path= Path(path_to_pdf)

num_of_pdf_pages_in_signature = number_of_pages_in_signature*2*2
pdf_in = open(path_to_pdf, 'rb')
pdf_reader = PyPDF2.PdfReader(pdf_in)
pdf_writer = PyPDF2.PdfWriter()

doc_length_original = len(pdf_reader.pages)
doc_length = doc_length_original
if doc_length % 2 == 1:
    doc_length+=1

number_of_signature = math.floor((doc_length/num_of_pdf_pages_in_signature))

if (doc_length % num_of_pdf_pages_in_signature) > 0:
    number_of_signature = number_of_signature + 1


array_of_page_numbers=[]
for x in range(1, doc_length_original):
    array_of_page_numbers.append(x)

track_page_num = 1
new_sigs = []
new_page_order = []

for x in range(1, number_of_signature+1):
    page_order = []
    middle_num_left = track_page_num+(num_of_pdf_pages_in_signature/2)-1
    middle_num_right = track_page_num+(num_of_pdf_pages_in_signature/2)
    page_count = 0
    sig_track={}
    for y in range(number_of_pages_in_signature*2, 0, -1):
        if y%2 == 1:
            sig_track[y] = (middle_num_right+page_count, middle_num_left-page_count)
        else:
            sig_track[y] = (middle_num_left-page_count, middle_num_right+page_count)
        page_count +=1
    new_sigs.append(sig_track)
    track_page_num = track_page_num + num_of_pdf_pages_in_signature


for sig in new_sigs:
    for page in sorted(sig.keys()):
        new_page_order.append(int(sig[page][0]))
        new_page_order.append(int(sig[page][1]))




def reorder_pdf_pages(new_order, pdf_reader, pdf_writer, max_page_num):
    for page_num in new_order:
        if page_num > max_page_num-1:
            page = pdf_reader.pages[max_page_num-1]
        else:
            page = pdf_reader.pages[page_num-1]
        pdf_writer.add_page(page)
    pdf_out = open('rearranged_doc_5.pdf', 'wb')
    pdf_writer.write(pdf_out)
    pdf_out.close()
    return



reorder_pdf_pages(new_page_order, pdf_reader, pdf_writer, doc_length_original)

pdf_in.close()
print(f"""
Num of pages: {doc_length_original}
Num of pages(double page per side): {doc_length/2}
Num of pages per signature:  {num_of_pdf_pages_in_signature}
Sigs: {number_of_signature}

""")
