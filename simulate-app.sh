#!/bin/sh
mvn clean install
mvn exec:java -Dexec.mainClass="testSim.$1.Main"
