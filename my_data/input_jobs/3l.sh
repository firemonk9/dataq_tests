#!/bin/bash
export JAVA_HOME=$1
$2bin/spark-submit --master local --class org.diff.DataDiffTool /Users/dhiraj/Documents/dataq/datadiff/target/scala-2.11/dataq-v2.jar INPUT_FILE=$6 OUTPUT_FILE=$7 ACTION=DIFF SUBMITTED_TIME=123123123 LICENSED=true local=true PROJECT_ID=$3 EXECUTION_ID=$4 JOB_ID=$5 