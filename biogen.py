#!/usr/bin/env python
import os
import sys
import re
from pgi.repository import Gtk, GObject

class EntryWindow(Gtk.Window):

    def __init__(self, ask_title="Title", ask_body="Body", message="Message"):
        Gtk.Window.__init__(self, title=ask_title)
        self.set_size_request(200, 100)

        self.timeout_id = None

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)

        label = Gtk.Label(message)
        vbox.pack_start(label, True, True, 0)

        self.entry = Gtk.Entry()
        self.entry.set_text(ask_body)
        vbox.pack_start(self.entry, True, True, 0)

        hbox = Gtk.Box(spacing=6)
        vbox.pack_start(hbox, True, True, 0)

        button = Gtk.Button(label="OK")
        button.connect("clicked",self.on_ok_button_clicked)
        vbox.pack_start(button, True, True, 0)

    def on_ok_button_clicked(self,button):
        Gtk.main_quit()

    def run(self):
        self.show_all()
        Gtk.main()
        result = self.entry.get_text()
        self.destroy()
        return result


def slugify(string):
    """
    Convert non-alphanums to underscores.
    """
    return re.sub('[^0-9a-zA-Z]+', '_', string).lower()

def ask(parent=None, message='', default_value='', title=''):
    """
    Generaically presents a message to a user and returns a reponse
    via return value.
    """
    win = EntryWindow(title, default_value, message)
    return win.run()

def which(program):
    """
    Function to check if a command exists
    """
    import os
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None


def write_file(newpath, name, content):
    """
    Generic file writing function.
    """
    full_file_path = os.path.join(newpath, name.lower())
    full_file = open(full_file_path, 'w')
    full_file.write(content.encode('utf8'))
    full_file.close()

def create_readme(newpath, title, readme):
    """
    Create project readme file.
    """
    readme = """# %s
    %s""" % (title, readme)
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

def create_virtualenv(newpath):
    """
    If possible create a virtualenv
    """
    ve_exe = which('virtualenv')
    if not ve_exe:
        print('Please install virtualenv if you wish to create per project virtualenvs')
        return False

    py_exe = which('pypy')
    if not py_exe:
        python = which('python')

    if not py_exe:
        return False

    venv_path = os.path.join(newpath, 'venv/')
    import subprocess
    # TODO Add no site packages to enforce proper requirements
    proc = subprocess.Popen([ve_exe, "-p", py_exe, venv_path,'--no-site-packages'])
    proc.wait()
    create_requirements(newpath)

def create_requirements(newpath):
    """
    Create file containing the projects requirements
    """
    """pgi
pyperclip
pypy
    """
    write_file(newpath, 'requirements.txt', 'pgi')

def create_activate_deactivate(newpath):
    """
    This will create scripts to run within the project to prepare virtualenvs.
    """
    # Use write_file for this!
    pass

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

def create_skeleton_code(newpath, id, title, sample_content = ''):
    """
    Create main source.
    """
    id = slugify(id)
    main_text = """#!/usr/bin/env python
#%s
import sys

class EntryWindow(Gtk.Window):

    def __init__(self, ask_title="Title", ask_body="Body", message="Message"):
        Gtk.Window.__init__(self, title=ask_title)
        self.set_size_request(200, 100)

        self.timeout_id = None

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)

        label = Gtk.Label(message)
        vbox.pack_start(label, True, True, 0)

        self.entry = Gtk.Entry()
        self.entry.set_text(ask_body)
        vbox.pack_start(self.entry, True, True, 0)

        hbox = Gtk.Box(spacing=6)
        vbox.pack_start(hbox, True, True, 0)

        button = Gtk.Button(label="OK")
        button.connect("clicked",self.on_ok_button_clicked)
        vbox.pack_start(button, True, True, 0)

    def on_ok_button_clicked(self,button):
        Gtk.main_quit()

    def run(self):
        self.show_all()
        Gtk.main()
        result = self.entry.get_text()
        self.destroy()
        return result

def bio_%s(input):
    # Generally a good idea to strip trailing newlines
    input = input.rstrip('\\n')
    # Usually you need to split up compared sequences ie:
    # (part_a, part_b) = input.split('\\n')

    # Insert code here
    %s

    # Result must be returned as a string due to limitations in unit-tests generator
    result = ''
    return str(result)
    # Perhaps you have a list and need to convert to string
    # return str(' '.join([str(i) for i in result]))

def main():
    # Take input from user, tidy and run code
    if len(sys.argv) > 1:
        if sys.argv[1] == 'livetest':
            try:
                from pgi.repository import Gtk, GObject
            except ImportError:
                import sys
                sys.exit('Please run pip -r requirements.txt from virtualenv')
            win = EntryWindow(title, message, default_value)
            input = win.run()
            result = bio_%s(input)
            try:
                import pyperclip
                copy_to_clipboard = True
            except ImportError:
                copy_to_clipboard = False
            # print result to command line
            print(result)
            if copy_to_clipboard:
                print('Result also copied to clipboard')
                pyperclip.copy(result)
        # Assume command line argument is input to code.
        else:
            print(bio_%s(input))
    else:
        print('Please supply a valid argument')

if __name__ == '__main__':
    main()""" % (title, id, sample_content, id, id)
    write_file(newpath, 'bio'+id+'.py', main_text)




def create_project(root_folder):
    """
    Take in project info from user and generate project files.
    """
    # Ask for text id/short description create folder/initial files
    id = ask(message = 'What is the id of the question?', default_value='Ex:BA1A')

    # Ask for text id/short description create folder/initial files
    title = ask(message = 'What is the title of the question?', default_value='Ex:Find All Approximate Occurrences of a Pattern in a String')
    if not title:
        title = id

    # Generate folder and virtualenv
    newpath = create_project_folder(root_folder, id)
    create_skeleton_code(newpath, id, title)
    create_virtualenv(newpath)

    # Ask for text description and create a readme.md
    readme = ask(message = 'What is the description for this problem?')
    create_readme(newpath, title, readme)

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

    # TODO generate activate.sh
    # TODO generate deactivate.sh(use pip freeze)


def main(location):
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
