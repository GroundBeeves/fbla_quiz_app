# FBLA Quiz! App

The FBLA Quiz! App is a trivia application that tests the user on different factoids about the Future Business Leaders of America's history (founding, directors, current national officers, sponsors, etc.). It asks four different kinds of questions: Multiple Choice, Fill-in-the-Blank, True or False, and Multiple Selection.

## Installation

The game runs on Python and the [Kivy NUI framework](https://kivy.org/#home). More importantly, it also utilizes [KivyMD](https://github.com/kivymd/KivyMD). Make sure you have both of those installed including all dependencies that may be needed for running (including reportlab for PDF generation). After all dependencies are installed, you can run the main.py file.

Or... you can skip all that and download the fbla_app.zip file. This contains a [PyInstaller](https://www.pyinstaller.org/)-made  .exe file. Once the folder is extracted, DO NOT MOVE THE EXE FILE. It won't run without the surrounding dependencies and resources. If you run the fbla.exe file, the game will run.

While a single .exe file could be made with PyInstaller, it doesn't allow for access to the questions.json file. It creates and deletes a temporary version of the .json file, so any changes to it would be deleted.

## PyInstaller Compilation

Once you have made your changes, you can compile the project once more by running the following command in the same directory as the repository.
```bash
python -m PyInstaller fbla.spec -y
```
This compiles a new distribution in a 'dist' folder in the same folder as the main.py folder.

## Works Cited
“About FBLA-PBL” Future Business Leaders of America-Phi Beta Lambda. Accessed 9 Jan. 2021, https://www.fbla-pbl.org/about/.
“FBLA National Officers” Future Business Leaders of America-Phi Beta Lambda. Accessed 9 Jan. 2021, https://www.fbla-pbl.org/fbla/officers/.
“History of FBLA-PBL” Future Business Leaders of America-Phi Beta Lambda. Accessed 9 Jan. 2021, https://www.fbla-pbl.org/about/history/.
"FBLA-PBL Fact Sheet" Future Business Leaders of America-Phi Beta Lambda. Web. Accessed 9 Jan. 2021, https://www.fbla-pbl.org/media/2019%E2%80%9320-FBLA-Fact-Sheets.pdf

The following languages and libraries were used in this project: Copyright (c) 1991-1995 by Stichting Mathematisch Centrum, Amsterdam, The Netherlands - Python; Copyright (c) 2010-2020 Kivy Team and other contributors - Kivy; Copyright (c) 2008-2016; Nigel Stewart <nigels[]users sourceforge net> - The OpenGL Extension Wrangler Library; Copyright (c) 2002-2008, Milan Ikits <milan ikits[]ieee org> - The OpenGL Extension Wrangler Library; Copyright (c) 2002-2008, Marcelo E. Magallon <mmagallo[]debian org> - The OpenGL Extension Wrangler Library; Copyright (c) 2002, Lev Povalahev - The OpenGL Extension Wrangler Library; Copyright (c) 2015 Andrés Rodríguez and other contributors - KivyMD library up to version 0.1.2; Copyright (c) 2020 KivyMD Team and other contributors - KivyMD library version 0.1.3 and higher; Reportlab Copyright (c) 2000-2014, ReportLab Inc.

