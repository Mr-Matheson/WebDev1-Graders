# Overview
This autograder is a useful tool for grading the assignments in the CCSDUT Shared Canvas Web Development sandbox. It currently supports the ***My First Webpage***, ***My Second Webpage***, and ***Dungeon Map*** assignments, although support is planned for ***My First Website***, ***HTML Test Part 2***, and the ***Final Project***.

## Basic Usage
When you run the autograder program, you'll be presented with a console window and a GUI. You can ignore the console, it's just for debugging purposes. The GUI looks like this:

![Autograder GUI](/images/gui.png)

It has a field that asks for the file path to a zip file containing all your students submissions for an assignment. Download that zip file from the Canvas assignment page, and enter its file path in the appropriate field:

![Download Submissions button on Canvas Assignment](/images/download_submissions_as_zip.png)

Then you'll need to find or create a folder where you want the autograder's results and feedback to be saved on your computer. Next, select which assignment to grade from the drop down (remembering that for the moment, only ***My First Webpage***, ***My Second Webpage***, and ***Dungeon Map*** are supported). Finally, hit the ***Run Local Auto-Grader*** button. Voila! Your results will display in the window and be saved to a CSV spreadsheet file in your ***Results*** directory.

## Automatic Canvas Grade Uploads
After you've reviewed the results in the preview window or in the spreadsheet, you can paste in the URL from the SpeedGrader page on Canvas:

![Speedgrader URL Location](/images/speedgrader_url.png)

Click the **Submit to Canvas** button, and the autograder will open a new browser window for the SpeedGrader. Follow the prompts to sign in and watch as the program inputs scores and leaves feedback for each students!

### WARNING
It's critical that you match the submissions with the correct Assignment Autograder and SpeedGrader URL, otherwise the autograder may grade each assignment based off the wrong rubric, or even worse, it may upload grades and feedback for the wrong assignment. Some students might get a score for an assignment they didn't turn in or not get a score when they should have, or they may get a score and feedback intended for another assignment. In any case, it'll be a mess you have to figure out.

## Compilation
To package the autograder into a GUI-based standalone executable (named **Assignmentgrader.exe**), use the following command:
>pyinstaller -F -n AssignmentGrader --hidden-import=bs4 --hidden-import=selenium --hidden-import=pandas --hidden-import=pygetwindow --add-data "my_first_website_grader.py;." --add-data "utilities.py;." --add-data "auto_canvas.py;." --add-data "dungeon_grader.py;." --add-data "test_part_2_grader.py;." --add-data "my_first_webpage_grader.py;."
 --add-data "my_second_webpage_grader.py;." --add-binary "chromedriver.exe;." grader_gui.py

Unless you're already running in a virtual environment or you already have these dependencies installed, you can first install them all:
>pip install requests beautifulsoup4 selenium pandas pygetwindow pyinstaller urllib3