
INSTALLATION:

--High level language

Java Development Kit (required JDK 7 or higher)

You can download the required JDK at http://www.oracle.com/technetwork/java/javase/downloads/index.html

In Linux systems, to make sure that everything works you should be able to call java -version and javac -version from a Terminal. For Windows and Mac users, find the Java Control Panel. Under the General tab in the Java Control Panel, the version can be checked from the About section.

###Python 2.7.x Python 2 is required for the parser. Visit https://www.python.org/downloads/ to download and install python.

Python Lex Yacc (ply)

python-ply is a requirement, you can download it at http://www.dabeaz.com/ply/ and install it through distutils using the provided setup.py file by running the command python setup.py install.

It might be required to provide the full installation path of python, in case the path variable is not set properly. Linux users can install it using sudo apt-get install python-ply.

Ensure that you have the execute permissions the scripts 

Installing StarL (newlib) 
We are migrating to the adopt-handler mechanism of starL now. for user convenience we use maven to compile projects. install maven from linux repositories if you have linux. This assumes you have installed java on your system.


Running apps:
Your file should be stored in the appCode directory, and should have an extension ".krd"
To run application, run  ./simulate.sh <appname.krd> 


