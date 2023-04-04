# Packaging and Distro

Here's a step-by-step guide on how to package and distribute Snake 'n Hamster:

Install PyInstaller:
If you don't have PyInstaller installed, open your terminal or command prompt and run:

pip install pyinstaller

Navigate to the directory containing your snake_game.py script. In the terminal or command prompt, run the following command:

pyinstaller --onefile --add-data "squeak.wav;." snake_game.py

This command will create a standalone executable from your snake_game.py script and include the squeak.wav file as data. The --onefile option tells PyInstaller to package everything into a single file. The --add-data option specifies additional data files to include in the package.

After running the PyInstaller command, you will find the packaged executable in the dist folder inside the directory containing your snake_game.py script. The executable file will be named snake_game.exe on Windows, or snake_game on macOS and Linux.

To distribute, share the standalone executable you found in the dist folder. Users should be able to run the game by double-clicking the file or executing it from the command line.