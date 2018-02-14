#!/bin/sh
mvn exec:java -Dexec.mainClass="testSim.$1.Main"
