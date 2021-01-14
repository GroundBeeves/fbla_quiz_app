# python -m PyInstaller --name FBLA --icon resources\icon.ico main.py
# python -m PyInstaller FBLA.spec

copyright_information = """
The following languages and libraries were used in this project:
Python 
Copyright (c) 1991-1995 by Stichting Mathematisch Centrum, Amsterdam, The Netherlands.

Kivy
Copyright (c) 2006-2021, Georg Brandl and Pygments contributors

The OpenGL Extension Wrangler Library
Copyright (c) 2008-2016, Nigel Stewart <nigels[]users sourceforge net>
Copyright (c) 2002-2008, Milan Ikits <milan ikits[]ieee org>
Copyright (c) 2002-2008, Marcelo E. Magallon <mmagallo[]debian org>
Copyright (c) 2002, Lev Povalahev


KivyMD
Copyright (c) 2015 Andrés Rodríguez and other contributors - KivyMD library up to version 0.1.2
Copyright (c) 2020 KivyMD Team and other contributors - KivyMD library version 0.1.3 and higher

Reportlab
Copyright (c) 2000-2014, ReportLab Inc.

Future Business Leaders of America
Copyright (c) 2019 FBLA-PBL
"""

# BUILT-IN IMPORTS
from os.path import join, isdir
import json
from random import choice, shuffle
import win32timezone

import os, sys
from kivy.resources import resource_add_path, resource_find

# VANILLA KIVY IMPORTS
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.modalview import ModalView
from kivy.uix.filechooser import FileChooserListView

# KIVYMD IMPORTS
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from kivymd.toast import toast

# CUSTOM MODULES
import printingResults

# Will store answers in a three-part tuple: (UserAnswer, Correct Boolean, Screen the question belongs to)
chosen_answers = []

# Opens question data and extracts random questions for each type (Multiple Choice, FITB, ToF, etc.). App will access a QuestionSet()'s data for these questions.  
class QuestionSet():
    def createQuestions(self):
        with open('questions/questions.json') as f:
            question_data = json.load(f)
            self.mc1 = choice(question_data["Multiple Choice 1"])
            self.mc2 = choice(question_data["Multiple Choice 2"])
            self.fitb = choice(question_data["Fill In The Blank"])
            self.tof = choice(question_data["True or False"])
            self.slct = choice(question_data["Select"])

# Global QuestionSet()
question_set = QuestionSet()
question_set.createQuestions()

# If you're not sure how Kivy works, it's a GUI module.
# You create the widgets in .kv file and code how they interact in a Python file.
# This is the Main Menu screen widget class. All the different question screens and
# result screens will have a 'Screen' at the end of the class name and will inherit
# from the MDScreen class.
class StartScreen(MDScreen):
    pass

class MuchScreen(MDScreen):

    global chosen_answers

    def __init__(self, question, order, **kw):
        super(MuchScreen, self).__init__(**kw)

        self.question = question

        # Sets question and question number values in .kv file.
        self.qnumber.text = str(order)
        self.question_text.text = self.question["Question"]
        # Creates lists of button .kv ids and answer choices for shuffling of choices and easy iteration.
        id_list = [self.choice1, self.choice2, self.choice3, self.choice4]
        ac_list = [self.question["Choice1"], self.question["Choice2"], self.question["Choice3"], self.question["Choice4"]]
        shuffle(ac_list)

        for id, choice in zip(id_list, ac_list):
            id.text = choice

    # Continues to the next screen and adds question results to chosen_answers list.
    def answerChosen(self, btn):
        app.sm.current = app.sm.next()
        correct = True if btn.text == self.question["Choice1"] else False
        chosen_answers.append((btn.text, correct, self))

class FITBScreen(MDScreen):

    global chosen_answers

    def __init__(self, question, order, **kw):
        super(FITBScreen, self).__init__(**kw)

        self.question = question

        # Sets question and question number values in .kv file.
        # Also reads and stores correct FITB answer from question data.
        self.qnumber.text = str(order)
        self.question_text.text = self.question["Question"]
        self.correct_answer = self.question["Choice1"]

    def answerChosen(self):
        if self.answer_given.text == "": # Only proceeds to the next screen if the answer given is not blank.
            self.answer_given.error = True 
        else: # Continues to the next screen and adds question results to chosen_answers list.
            answer = self.answer_given.text
            
            app.sm.current = app.sm.next()
            
            correct = True if answer.lower() == self.correct_answer.lower() else False
            chosen_answers.append((answer, correct, self))

class TOFScreen(MDScreen):

    global chosen_answers

    def __init__(self, question, order, **kw):
        super(TOFScreen, self).__init__(**kw)

        self.question = question

        # Sets question, question number, and true/false choice values in .kv file.
        self.qnumber.text = str(order)
        self.question_text.text = self.question["Question"]
        self.trueChoice.text = 'TRUE'
        self.falseChoice.text = 'FALSE'

    def answerChosen(self, btn):
        # Continues to the next screen and adds question results to chosen_answers list.
        app.sm.current = app.sm.next()
        correct = True if btn.text == self.question["Choice1"] else False
        chosen_answers.append((btn.text, correct, self))

class SelectScreen(MDScreen):
    def __init__(self, question, order, **kw):
        super(SelectScreen, self).__init__(**kw)

        self.question = question

        # Sets question and question number values in .kv file.
        self.qnumber.text = str(order)
        self.question_text.text = self.question["Question"]
        # Creates lists of checkbox .kv ids, label .kv ids, and answer choices for shuffling of choices and easy iteration.
        self.box_list = [self.box1, self.box2, self.box3, self.box4, self.box5, self.box6]
        self.label_list = [self.answer1, self.answer2, self.answer3, self.answer4, self.answer5, self.answer6]
        self.ac_list = self.question["Right Answers"] + self.question["Wrong Answers"]
        shuffle(self.ac_list)

        for label, choice in zip(self.label_list, self.ac_list):
            label.text = choice

    def answerChosen(self):
        # Compares the labels of active checkboxes to the question's "Right Answers" list.
        selected_choices = []
        for checkbox, label in zip(self.box_list, self.label_list):
            if checkbox.active:
                selected_choices.append(label.text)
        correct = all(item in self.question["Right Answers"] for item in selected_choices)
        if len(selected_choices) != len(self.question["Right Answers"]):
            correct = False
        
        # Continues to the next screen and adds question results to chosen_answers list.
        chosen_answers.append((selected_choices, correct, self))
        app.sm.current = app.sm.next()

class ResultsScreen(MDScreen):
    def __init__(self, **kw):
        super(ResultsScreen, self).__init__(**kw)
        self.correct_count = 0
        self.current = 0

    def calculateResults(self):
        if len(chosen_answers) > 3: # This prevents the code from running prematurely. Had trouble with that...
            # Counts up correct answers!
            for ans, corr, scrn in chosen_answers:
                if corr:
                    self.correct_count += 1
            
            # Displays results.
            self.results_disp.text = str(self.correct_count) + "/" + str(len(chosen_answers))
            
            # Displays the first question on the card.
            self.question_number.text = "Question " + str(self.current + 1)
            self.question_text.text = "QUESTION: " + chosen_answers[self.current][2].question["Question"]
            if isinstance(chosen_answers[self.current][0], list): # Checks if it is a FITB question.
                self.your_answer.text = "YOUR ANSWER: " + ', '.join(chosen_answers[self.current][0])
                self.correct_answer.text = "CORRECT ANSWER: " + ', '.join(chosen_answers[self.current][2].question["Right Answers"])
            else:
                self.your_answer.text = "YOUR ANSWER: " + chosen_answers[self.current][0]
                self.correct_answer.text = "CORRECT ANSWER: " + chosen_answers[self.current][2].question["Choice1"]

    # Updates the content of the card in the results screen. Allows for cycling through the list.
    def updateQuestionCard(self, direction='next'):

        # This function is used for the previous AND the next button.
        # It uses a kwarg to determine whether to go forwards or backwards.
        if direction == 'next':
            if self.current == (len(chosen_answers) - 1):
                self.current = 0
            else:
                self.current += 1
        elif direction == 'previous':
            if self.current == 0:
                self.current = (len(chosen_answers) - 1)
            else:
                self.current -= 1

        # Updates the content of the card depending on the current question.
        self.question_number.text = "Question " + str(self.current + 1)
        self.question_text.text = "QUESTION: " + chosen_answers[self.current][2].question["Question"]
        if isinstance(chosen_answers[self.current][0], list):
            self.your_answer.text = "YOUR ANSWER: " + ', '.join(chosen_answers[self.current][0])
            self.correct_answer.text = "CORRECT ANSWER: " + ', '.join(chosen_answers[self.current][2].question["Right Answers"])
        else:
            self.your_answer.text = "YOUR ANSWER: " + chosen_answers[self.current][0]
            self.correct_answer.text = "CORRECT ANSWER: " + chosen_answers[self.current][2].question["Choice1"]

class FileChooserWindow(FileChooserListView):

    # This runs when a directory is chosen by the file manager modal view.
    # It generates the PDF, dismisses the window, and shows a little pop-up 
    # showing where it was saved.
    def saveToComputer(self, directory):
        # Saves the PDF to the computer but if permission is denied, then it's saved to 
        try:
            self.generatePDF(directory[0])
            self.parent.dismiss()
            toast("Saved to " + directory[0] + ".")
        except PermissionError:
            self.parent.dismiss()
            toast("Permission Denied.")
        except:
            self.parent.dismiss()
            toast("Something went wrong!")

    # Uses the printingResults module to create a PDF with a module called reportlab.
    # Saves it to wherever the user chose in the file manager modal view.
    def generatePDF(self, directory):

        # Puts the chosen_answers list into a format used by the runPrinting function.
        question_list = []
        user_answer_list = []
        correct_answer_list = []
        correct_status_list = []
        for usr_ans, corr, scrn in chosen_answers:
            question_list.append(scrn.question["Question"])
            correct_status_list.append(corr)
            if not isinstance(usr_ans, list):
                correct_answer_list.append(scrn.question["Choice1"])
                user_answer_list.append(usr_ans)
            else:
                correct_answer_list.append(', '.join(scrn.question["Right Answers"]))
                user_answer_list.append(', '.join(usr_ans))
        
        # Creates a pdf and saves it in the desired directory
        printingResults.runPrinting(question_list, user_answer_list, correct_answer_list, correct_status_list, directory)

class CopyrightInfo(MDLabel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = copyright_information

class FBLAApp(MDApp):

    def build(self):

        self.theme_cls.primary_palette = 'Blue'

        # Initialization of the screenmanager. This class manages the order
        # of the screens. This snippet also sets the main menu as the starting 
        # screen.
        self.sm = ScreenManager()
        self.root_screen = StartScreen(name='start')
        self.sm.add_widget(self.root_screen)
        return self.sm

    def resetQuiz(self):

        # Resets the stored answers and rolls for new questions.
        global chosen_answers
        chosen_answers = []
        question_set.createQuestions()
        self.sm.clear_widgets()

        # Adds fresh screens to the ScreenManager.
        mc1_screen = MuchScreen(question_set.mc1, 1, name='mc1_screen')
        mc2_screen = MuchScreen(question_set.mc2, 2, name='mc2_screen')
        fitb_screen = FITBScreen(question_set.fitb, 3, name='fitb_screen')
        tof_screen = TOFScreen(question_set.tof, 4, name='tof_screen')
        slct_screen = SelectScreen(question_set.slct, 5, name='slct_screen')
        results_screen = ResultsScreen(name='results_screen')

        self.sm.add_widget(self.root_screen)
        self.sm.add_widget(mc1_screen)
        self.sm.add_widget(mc2_screen)
        self.sm.add_widget(fitb_screen)
        self.sm.add_widget(tof_screen)
        self.sm.add_widget(slct_screen)
        self.sm.add_widget(results_screen)

    # Opens a file manager modal view (a little overlay window).
    def open_file(self):
        view = ModalView(size_hint=(.5, .5))
        view.add_widget(FileChooserWindow())
        view.open()

    def open_copyright(self):
        view = ModalView(size_hint=(.75, .8))
        view.add_widget(CopyrightInfo())
        view.open()

    # This is just a filter so that the file manager can only display and
    # select directories, not just any file.
    def is_dir(self, directory, filename):
        return isdir(join(directory, filename))

if __name__ == "__main__":
    if hasattr(sys, '_MEIPASS'):
        resource_add_path(os.path.join(sys._MEIPASS))
    app = FBLAApp()
    app.run()