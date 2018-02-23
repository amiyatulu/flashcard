# flashcard
Generate flash cards

**Requirements**  
python3  
reportlab  

Fill the fields (*title* and *content*) of **questions.csv** using **LibreOffice Calc** or **MS Excel** 

You can use **&lt;br\\&gt;** for line breaks

Use **question_to_json.py** to generate **card.json** from **questions.csv**

**Command:**

python3 question_to_json.py -f "path/to/file/questions.csv"


Then generate flashcard pdf using **flash.py**

**Command:**

python3 flash.py


