# What this does

For anyone working on the [Coursera Bioinformatic Algorithms Specialisation](https://www.coursera.org/specializations/bioinformatics) or solving [Rosalind](http://rosalind.info/) problems using Python. I've written this script to generate a standardised way to structure, write and test your code.

The sample and extra data provided from the Coursera course are converted into valid unit tests, the advantage being to test your code against the datasets involves simply running `python bio_**_test.py`.

# Requirements

This requires wxPython. There's a installer guide [here](http://wiki.wxpython.org/How%20to%20install%20wxPython).

# How to run
1. Run `python biogen.py project_root_folder` via the command line. This root folder is the parent folder for all your bioinformatic algorithms coursework. For example /home/user/Documents/bioinformatics

2. Answer the questions that pop-up on the screen.

3. Now you should have a `bio_**.py` and a `bio_**_test.py`. If you run `python bio_**_test.py` it should throw up two errors, that your code neither passes the sample nor extra dataset unit tests.

4. Now just write the working code and re-run the unit tests using `python bio_**_test.py` until it finally passes. Now you're good to test with live data.

5. Because the live data tends to have a 5 minute time-limit. I wrote a helper function to run when you are testing the code with live data. In the generated code folder, simply run `python bio_**.py` livetest and a text input will pop-up asking for your input.

6. The generated code is meant to be a starting point. For example, if you end up writing more functions, you should be writing unit tests for those functions too.

# TODOs

* Better testing of inputs
* Create virtual environments
* Create an activate and deactivate that automatically store the requirements a developer adds while working on code
* Convert file strings to template files
