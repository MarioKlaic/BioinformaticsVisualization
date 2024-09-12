# BioinformaticsVisualization
This project visualizes some of the algorithms from the FER course: bioinformatics 1

The folder Bioinformatics_vis contains both the source code and the distribution version of the tool.

The distribution version is a web page that is run locally through an .exe file which will start it on a local address ( e.g. http://127.0.0.1:5000 ) and can be opened through your browser of choice.

Dist.rar contains the distribution version and has been tested and ran on windows. If any issues occur for other operating systems the folder "Bioinformatics_vis" can be downloaded in its entirety and
locate yourself within that directory and run pyinstaller command "pyinstaller main.spec" to build your own distribution version with the specifications inside of the .spec file. You may need to change it
to your os requirements. Visit https://pyinstaller.org/en/stable/usage.html# 

The other way to use this tool is through your own IDE or powershell and run the main.py to start the server locally by running the command "python main.py". It will start a server on your local adress which can be seen in the terminal where the command was run. You can use this tool by accessing that adress on your web browser.
