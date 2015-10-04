# What this does

For anyone working on the [Coursera Bioinformatic Algorithms Specialisation](https://www.coursera.org/specializations/bioinformatics) or solving [Rosalind](http://rosalind.info/) problems using Python. I've written this script to generate a standardised way to structure, write and test your code.

The sample and extra data provided from the Coursera course are converted into valid unit tests, the advantage being to test your code against the datasets involves simply running `python bio_**_test.py`.

The other advantage is this creates a per project virtual environments, using PyPy and a PyPy compatible GTK library, to ensure the fastest possible development, runtime and testing.

# Requirements

Simply create a virtualenv and install whatever's in the requirements.txt using `pip install -r requirements.txt`.

# How to run
1. Run `python biogen.py project_root_folder` via the command line. This root folder is the parent folder for all your bioinformatic algorithms coursework. For example `/home/user/Documents/bioinformatics`

2. Answer the questions that pop-up on the screen.

3. Within the newly created working directory run `source venv/bin/activate` to enable the new projects virtualenvironment.

4. Run `pip install -r requirements.txt` to install the initial project dependencies.

5. You should now also have a `bio_**.py` and a `bio_**_test.py`. If you run `python bio_**_test.py` it will throw up two errors, that your code neither passes the sample nor extra dataset unit tests.

6. Now just write the working code and re-run the unit tests using `python bio_**_test.py` until it finally passes. Now you're good to test with live data.

7. Because the live data tends to have a 5 minute time-limit, I've written a helper function to run when you are testing the code with live data. In the generated code folder, simply run `python bio_**.py livetest` and a text input will pop-up asking for your input. If pyperclip is installed this will also automatically copy the result to clipboard, especially handy for huge result sets.

8. The generated code is meant to be a starting point. For example, if you end up writing more functions, you should be writing unit tests for those functions too.

# TODOs

* Better testing of inputs
* Create an activate and deactivate that automatically store the requirements a developer adds while working on code
* Convert file strings to template files
