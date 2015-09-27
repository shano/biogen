import wx
import os
import sys
import re

def slugify(string):
    """
    Convert non-alphanums to underscores.
    """
    return re.sub('[^0-9a-zA-Z]+', '_', string).lower()

def ask(parent=None, message='', default_value=''):
    """
    Generaically presents a message to a user and returns a reponse
    via return value.
    """
    dlg = wx.TextEntryDialog(parent, message, defaultValue=default_value)
    dlg.ShowModal()
    result = dlg.GetValue()
    dlg.Destroy()
    return result

def write_file(newpath, name, content):
    """
    Generic file writing function.
    """
    full_file_path = os.path.join(newpath, name.lower())
    full_file = open(full_file_path, 'w')
    full_file.write(content.encode('utf8'))
    full_file.close()

def create_readme(newpath, readme):
    """
    Create project readme file.
    """
    write_file(newpath, 'readme.md', readme)

def create_unittest_text(id, test_type, dataset, dataset_answer):
    id = slugify(id)
    return """
    def test_%s_%s(self):
        self.assertEqual(bio%s.bio_%s(\"\"\"%s\"\"\"), \"\"\"%s\"\"\")""" % (id, test_type, id, id, dataset, dataset_answer)

def create_unittests(newpath, id, sample_ut, extra_ut):
    id = slugify(id)
    unittest_text = """
import unittest
import bio%s

class Bio%sTestCase(unittest.TestCase):
    %s
    %s

if __name__ == '__main__':
    unittest.main()""" % (id, id, sample_ut, extra_ut)

    write_file(newpath, 'bio'+id+'_test.py', unittest_text)


def create_project_folder(root_folder, id):
    """
    Create folder for project based on root.
    """
    id = slugify(id)
    newpath = os.path.join(root_folder, id)
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    else:
        sys.exit('Cannot run as project folder already exists!')
    return newpath

def create_skeleton_code(newpath, id, sample_content = ''):
    """
    Create main source.
    """
    id = slugify(id)
    main_text = """#!/usr/bin/env python

def bio_%s(input):
    # Usually you need to split up compared sequences ie:
    # (part_a, part_b) = input.split('\\n')
    
    # Insert code here
    %s

    # Result must be returned as a string due to limitations in unit-tests generator
    result = ''
    return str(result)

def main():
    # Take input from user, tidy and run code
    if len(sys.argv) > 1:
        if sys.argv[1] == 'livetest':
            import wx
            app = wx.App()
            app.MainLoop()
            dlg = wx.TextEntryDialog(None, 'Paste in live input')
            dlg.ShowModal()
            input = dlg.GetValue()
            dlg.Destroy()
            result = bio_%s(input)
            # print result to command line
            print(result)
        # Assume command line argument is input to code.
        else:
            print(bio_%s(input))
    else:
        print('Please supply a valid argument')

if __name__ == '__main__':
    main()""" % (id, sample_content, id, id)
    write_file(newpath, 'bio'+id+'.py', main_text)




def create_project(root_folder):
    """
    Take in project info from user and generate project files.
    """
    # Ask for text id/short description create folder/initial files
    id = ask(message = 'What is the id of the question?', default_value='Ex:BA1A')
    id = id

    # Generate folder
    newpath = create_project_folder(root_folder, id)
    create_skeleton_code(newpath, id)

    # Ask for text description and create a readme.md
    readme = ask(message = 'What is the description for this problem?')
    create_readme(newpath, readme)

    # Ask for sample dataset and response 
    sample_dataset = ask(message = 'What is the sample dataset?')
    sample_dataset_answer = ask(message = 'What is the sample datasets expected output?')


    # Ask for extra dataset and response
    extra_dataset = ask(message = 'What is the extra dataset?')
    extra_dataset_answer = ask(message = 'What is the extra datasets expected output?')

    # Generate unit tests
    sample_ut = create_unittest_text(id, 'sample', sample_dataset, sample_dataset_answer)
    extra_ut = create_unittest_text(id, 'extra', extra_dataset, extra_dataset_answer)
    create_unittests(newpath, id, sample_ut, extra_ut)

    # TODO generate virtualenv
    # TODO generate activate.sh
    # TODO generate deactivate.sh(use pip freeze)


def main(location):
    # Initialize wx App
    app = wx.App()
    app.MainLoop()
    create_project(location)
    

if __name__ == "__main__":
    if len(sys.argv) > 1:
      location = sys.argv[1]
      if os.path.exists(location):
        main(location)
      else:
        print('Invalid path specified')
    else:
      print('Please specify folder path')
