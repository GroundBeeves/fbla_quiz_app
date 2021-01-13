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
