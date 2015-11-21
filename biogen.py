#!/usr/bin/env python
import os
import sys
import re
from pgi.repository import Gtk, GObject


class FileChooserWindow(Gtk.Window):

    def __init__(self, ask_title,ask_button):
        Gtk.Window.__init__(self, title=ask_title)

        box = Gtk.Box(spacing=6)
        self.add(box)

        button1 = Gtk.Button(ask_button)
        button1.connect("clicked", self.on_file_clicked)
        box.add(button1)

        self.dialog = Gtk.FileChooserDialog("Please choose a file", self,
                                            Gtk.FileChooserAction.OPEN,
                                            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                             Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

    def on_file_clicked(self, widget):
        self.add_filters(self.dialog)
        self.dialog.run()
        Gtk.main_quit()

    @staticmethod
    def add_filters(dialog):
        filter_text = Gtk.FileFilter()
        filter_text.set_name("Text files")
        filter_text.add_mime_type("text/plain")
        dialog.add_filter(filter_text)

        filter_any = Gtk.FileFilter()
        filter_any.set_name("Any files")
        filter_any.add_pattern("*")
        dialog.add_filter(filter_any)

    def run(self):
        self.show_all()
        Gtk.main()
        result = self.dialog.get_filename()
        self.dialog.destroy()
        self.destroy()
        return result


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
        self.entry.set_max_length(0)
        self.entry.truncate_multiline = False
        vbox.pack_start(self.entry, True, True, 0)

        hbox = Gtk.Box(spacing=6)
        vbox.pack_start(hbox, True, True, 0)

        button = Gtk.Button(label="OK")
        button.connect("clicked",self.on_ok_button_clicked)
        vbox.pack_start(button, True, True, 0)

    @staticmethod
    def on_ok_button_clicked(button):
        Gtk.main_quit()

    def run(self):
        self.show_all()
        Gtk.main()
        result = self.entry.get_text()
        self.destroy()
        return result


def slugify(string):
    """ Convert non-alphanums to underscores """
    return re.sub('[^0-9a-zA-Z]+', '_', string).lower()


def ask_file(title='', button=''):
    """
    Generically presents a file dialog to a user and returns a response
    via return value.
    """
    win = FileChooserWindow(title, button)
    filename = win.run()
    with open(filename, 'r') as content_file:
        content = content_file.read()
    return content


def ask(message='', default_value='', title=''):
    """
    Generically presents a message to a user and returns a response
    via return value.
    """
    win = EntryWindow(title, default_value, message)
    return win.run()


def which(program):
    """
    Function to check if a command exists
    """
    import os

    def is_exe(executable_file_path):
        return os.path.isfile(executable_file_path) and os.access(executable_file_path, os.X_OK)

    file_path, file_name = os.path.split(program)
    if file_path:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None


def write_file(new_path, name, content):
    """
    Generic file writing function.
    """
    full_file_path = os.path.join(new_path, name.lower())
    full_file = open(full_file_path, 'w')
    try:
        text = content.encode('utf8', 'replace')
    except UnicodeDecodeError:
        text = content
    full_file.write(text)
    full_file.close()


def read_file_contents(path, filename=None):
    if filename:
        path = os.path.join(path, filename)
    file_handle = open(path)
    return file_handle.read()


class Biogen():

    def __init__(self, root_folder):
        self.template_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'templates/')
        self.root_folder = root_folder

    def create_readme(self, new_path, title, body):
        """ Create project readme file."""
        src = read_file_contents(self.template_folder, 'readme.txt')
        rewrites = {'title': title, 'body': body}
        write_file(new_path, 'readme.md', src.format(**rewrites))

    def create_unittest_text(self, problem_name, test_type, data_set, data_set_answer):
        problem_name = slugify(problem_name)
        src = read_file_contents(self.template_folder, 'unit_tests.py.txt')
        rewrites = {'test_type': test_type, 'problem_name': problem_name,
                    'data_set': data_set, 'data_set_answer': data_set_answer,
                    'space': '        '}
        return src.format(**rewrites)

    def create_unittests(self, new_path, problem_name, sample_ut, extra_ut):
        """Create the unit test file"""
        problem_name = slugify(problem_name)
        src = read_file_contents(self.template_folder, 'skeleton_unit_tests.py.txt')
        rewrites = {'problem_name': problem_name, 'sample_unit_test': sample_ut, 'extra_unit_test': extra_ut}
        write_file(new_path, 'bio'+problem_name+'_test.py', src.format(**rewrites))

    def create_skeleton_code(self, new_path, problem_name, title, sample_content=''):
        """ Create main source. """
        src = read_file_contents(self.template_folder, 'skeleton.py.txt')
        problem_name = slugify(problem_name)
        rewrites = {'title': title, 'id': problem_name, 'snippet': sample_content}
        write_file(new_path, 'bio'+problem_name+'.py', src.format(**rewrites))

    def create_requirements(self):
        """ Create file containing the projects requirements """
        src = read_file_contents(self.template_folder, 'requirements.txt')
        write_file(self.root_folder, 'requirements.txt', src)

    def create_virtualenv(self):
        """
        If possible create a virtualenv
        """
        virtual_path = os.path.join(self.root_folder, 'venv/')
        if os.path.exists(virtual_path):
            print('Virtual Environment already exists, skipping....')
            return False

        ve_exe = which('virtualenv')
        if not ve_exe:
            print('Please install virtualenv if you wish to create per project virtualenvs')
            return False

        py_exe = which('pypy')
        if not py_exe:
            py_exe = which('python')

        if not py_exe:
            return False

        import subprocess
        # TODO Add no site packages to enforce proper requirements
        process = subprocess.Popen([ve_exe, "-p", py_exe, virtual_path, '--no-site-packages'])
        process.wait()
        self.create_requirements()

    def create_project_folder(self, problem_name):
        """
        Create folder for project based on root.
        """
        problem_name = slugify(problem_name)
        new_path = os.path.join(self.root_folder, problem_name)
        if not os.path.exists(new_path):
            os.makedirs(new_path)
        else:
            sys.exit('Cannot run as project folder already exists!')
        return new_path

    def create_project(self):
        """ Take in project info from user and generate project files. """
        # Ask for text id/short description create folder/initial files
        problem_name = ask(message='What is the id of the question?', default_value='Ex:BA1A')
        new_path = self.create_project_folder(problem_name)

        # Ask for text id/short description create folder/initial files
        title = ask(message='What is the title of the question?',
                    default_value='Ex:Find All Approximate Occurrences of a Pattern in a String')
        if not title:
            title = problem_name

        # Ask for text description and create a readme.md
        readme = ask(message='What is the description for this problem?')

        # Ask for sample data set and response
        sample_data_set = ask(message='What is the sample data set?')
        sample_data_set_answer = ask(message='What is the sample data sets expected output?')

        # Ask for extra data set and response
        extra_data_set_raw = ask_file(title='Extra data set file', button='Please select extra data set')
        if 'Input:' in extra_data_set_raw and 'Output:' in extra_data_set_raw:
            (extra_data_set, extra_data_set_answer) = extra_data_set_raw.split("Output:")
        elif 'Input' in extra_data_set_raw and 'Output' in extra_data_set_raw:
            (extra_data_set, extra_data_set_answer) = extra_data_set_raw.split("Output")
        else:
            sys.exit('Please select a valid extra data set file')

        # Generate code and virtualenv
        self.create_skeleton_code(new_path, problem_name, title)
        self.create_virtualenv()

        self.create_readme(new_path, title, readme)

        extra_data_set = '\n'.join(extra_data_set.split('\n')[1:]).strip()
        extra_data_set_answer = extra_data_set_answer.strip()

        # Generate unit tests
        sample_ut = self.create_unittest_text(problem_name, 'sample', sample_data_set, sample_data_set_answer)
        extra_ut = self.create_unittest_text(problem_name, 'extra', extra_data_set, extra_data_set_answer)
        self.create_unittests(new_path, problem_name, sample_ut, extra_ut)

        # TODO generate activate.sh
        # TODO generate deactivate.sh(use pip freeze)


def main(project_location):
    biogen = Biogen(project_location)
    biogen.create_project()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        location = sys.argv[1]
        if os.path.exists(location):
            main(location)
        else:
            print('Invalid path specified')
    else:
        print('Please specify folder path')
