for i in *.ui
do
    pyside6-uic $i -o "${i%.ui}.py"
done
