#!/bin/sh
mvn clean install exec:java -Dexec.mainClass="testSim.$1.Main"
