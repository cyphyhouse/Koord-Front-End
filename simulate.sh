#!/bin/sh
cd appCode
cp $1 ../
cd ..
cp $1 KoordFE/
cd KoordFE
python parser.py $1
an="$(echo $1 | cut -d '.' -f 1)"

mkdir ../src/main/java/testSim/$an
mv *.java ../src/main/java/testSim/$an
cd ..
mvn compile 
mvn install
HOME_DIR=`echo "$HOME"`
java -cp target/newLib-0.1-BasicFunctionality.jar:"$HOME_DIR"/.m2/repository/log4j/log4j/1.2.17/log4j-1.2.17.jar:lib/* testSim.$an.Main
rm $1
