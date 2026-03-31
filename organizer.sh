#!/bin/bash
echo "--------------------------------------"
echo " GRADE ARCHIVER FILE "
echo "--------------------------------------"

if [ ! -f "grades.csv" ]; then 
    echo "Error: grades.csv is not found in the current directory!"
    exit 1
fi

if [ ! -d "archive" ]; then
    mkdir archive
    echo " created the archive directory"
fi

TIMESTAMP=$(date +"%Y%m%d-%H%M%S")

NEW_FILENAME="grades_${TIMESTAMP}.csv"

mv grades.csv "archive/$NEW_FILENAME"
echo " moved grades.csv to archive/$NEW_FILENAME"

touch grades.csv
echo "created new empty grades.csv"

echo "$(date '+%Y-%m-%d %H:%M:%S') | Original: grades.csv | Archived: $NEW_FILENAME" >> organizer.log
echo ""
echo "the archive completed "
echo "----------------------------------------------"
