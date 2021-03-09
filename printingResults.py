from reportlab.pdfgen import canvas
from reportlab.platypus import Image

#CONTENT: These variables just hold the information we'll be writing in the pdf
documentTitle = 'FBLA Quiz Results'
title = 'FBLA QUIZ RESULTS'
directory = "C:\\Users\\Casas Diamantina 1\\Desktop\\Coding"

# I used the ReportLab module to write PDFs. Writes each question and answer in a PDF and saves it
# in the desired directory. Pretty self-explanatory.
def runPrinting(question_list, user_answer_list, correct_answer_list, correct_status_list, directory, filename):
    pdf = canvas.Canvas(directory + "\\" + filename)
    pdf.setTitle(documentTitle)

    # Writes FBLA QUIZ RESULTS at the top
    pdf.setFont('Times-Roman', 35)
    pdf.drawCentredString(300, 770, title)
    
    # Writes score  under FBLA QUIZ RESULTS
    results = str(correct_status_list.count(True)) + "/" + str(len(correct_status_list))
    pdf.setFont('Times-Roman', 30)
    pdf.setFillColorRGB(0.8, 0, 0)
    pdf.drawCentredString(470, 720, results)

    # Writes each question.
    height = 700
    margin = 50
    qnumber = 1
    pdf.setFillColorRGB(0, 0, 0)
    pdf.setFont('Times-Roman', 15)
    for question, user_ans, corr_ans, corr in zip(question_list, user_answer_list, correct_answer_list, correct_status_list):

        if question_list.index(question) == 10:
            pdf.showPage()
            height = 770

        pdf.setFillColorRGB(0, 0, 0)
        pdf.drawString(margin, height, "Question " + str(qnumber) + ": " + (question if len(question) <= 71 else question[:72]))
        if len(question) >= 71:
            pdf.drawString(margin, height - 15, question[72:])
            height -= 15
        pdf.setFillColorRGB(0.6 if not corr else 0, 0.6 if corr else 0, 0) # Makes user answer green if correct and red if incorrect.
        pdf.drawString(margin, height - 15, "Your Answer: " + user_ans)
        pdf.setFillColorRGB(0, 0.6, 0)
        pdf.drawString(margin, height - 30, "Correct Answer: " + corr_ans)

        height -= 70
        qnumber += 1

    pdf.save()