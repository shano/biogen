import unittest
import os,tempfile
import biogen


class BioGenTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        test_dir = tempfile.mkdtemp()
        self.root_tmp = str(test_dir)
        self.id = 'BA1B'
        self.newpath = biogen.create_project_folder(self.root_tmp, self.id)

    def test_slugify(self):
        self.assertEqual('ba1b',biogen.slugify(self.id))

    def test_folder_is_created(self):
        self.assertEqual(self.newpath,os.path.join(self.root_tmp,biogen.slugify(self.id)))
        self.assertTrue(os.path.exists(self.newpath))

    def test_readme(self):
        sample_text = """We say that Pattern is a most frequent k-mer in Text if it maximizes Count(Text, Pattern) among all k-mers. For example, "ACTAT" is a most frequent 5-mer in "ACAACTATGCATCACTATCGGGAACTATCCT", and "ATA" is a most frequent 3-mer of "CGATATATCCATAG".

Frequent Words Problem

Find the most frequent k-mers in a string.

Given: A DNA string Text and an integer k.

Return: All most frequent k-mers in Text (in any order)."""
        biogen.create_readme(self.newpath, sample_text)
        readme_path = os.path.join(self.newpath, 'readme.md')
        self.assertTrue(os.path.isfile(readme_path))
        with open (readme_path, "r") as myfile:
          contents=myfile.read()
        self.assertEqual(contents, sample_text)

    def test_sample_unit_test(self):
        sample_dataset = """ACGTTGCATGTCGCATGATGCATGAGAGCT
4"""
        sample_dataset_answer = """CATG GCAT"""
        sample_ut = biogen.create_unittest_text(self.id, 'sample', sample_dataset, sample_dataset_answer)
        self.assertTrue(sample_dataset in sample_ut)
        self.assertTrue(sample_dataset_answer in sample_ut)
        self.assertTrue('def test_' + biogen.slugify(self.id) + '_sample' in sample_ut)

    def test_extra_unit_test(self):
        extra_dataset = """CGGAAGCGAGATTCGCGTGGCGTGATTCCGGCGGGCGTGGAGAAGCGAGATTCATTCAAGCCGGGAGGCGTGGCGTGGCGTGGCGTGCGGATTCAAGCCGGCGGGCGTGATTCGAGCGGCGGATTCGAGATTCCGGGCGTGCGGGCGTGAAGCGCGTGGAGGAGGCGTGGCGTGCGGGAGGAGAAGCGAGAAGCCGGATTCAAGCAAGCATTCCGGCGGGAGATTCGCGTGGAGGCGTGGAGGCGTGGAGGCGTGCGGCGGGAGATTCAAGCCGGATTCGCGTGGAGAAGCGAGAAGCGCGTGCGGAAGCGAGGAGGAGAAGCATTCGCGTGATTCCGGGAGATTCAAGCATTCGCGTGCGGCGGGAGATTCAAGCGAGGAGGCGTGAAGCAAGCAAGCAAGCGCGTGGCGTGCGGCGGGAGAAGCAAGCGCGTGATTCGAGCGGGCGTGCGGAAGCGAGCGG
12"""
        extra_dataset_answer = """CGGCGGGAGATT CGGGAGATTCAA CGTGCGGCGGGA CGTGGAGGCGTG CGTGGCGTGCGG GCGTGCGGCGGG GCGTGGAGGCGT GCGTGGCGTGCG GGAGAAGCGAGA GGAGATTCAAGC GGCGGGAGATTC GGGAGATTCAAG GTGCGGCGGGAG TGCGGCGGGAGA"""
        extra_ut = biogen.create_unittest_text(self.id, 'extra', extra_dataset, extra_dataset_answer)
        self.assertTrue(extra_dataset in extra_ut)
        self.assertTrue(extra_dataset_answer in extra_ut)
        self.assertTrue('def test_' + biogen.slugify(self.id) + '_extra' in extra_ut)

    def test_unit_test_file(self):
        sample_dataset = """ACGTTGCATGTCGCATGATGCATGAGAGCT
4"""
        sample_dataset_answer = """CATG GCAT"""
        sample_ut = biogen.create_unittest_text(self.id, 'sample', sample_dataset, sample_dataset_answer)
        extra_dataset = """CGGAAGCGAGATTCGCGTGGCGTGATTCCGGCGGGCGTGGAGAAGCGAGATTCATTCAAGCCGGGAGGCGTGGCGTGGCGTGGCGTGCGGATTCAAGCCGGCGGGCGTGATTCGAGCGGCGGATTCGAGATTCCGGGCGTGCGGGCGTGAAGCGCGTGGAGGAGGCGTGGCGTGCGGGAGGAGAAGCGAGAAGCCGGATTCAAGCAAGCATTCCGGCGGGAGATTCGCGTGGAGGCGTGGAGGCGTGGAGGCGTGCGGCGGGAGATTCAAGCCGGATTCGCGTGGAGAAGCGAGAAGCGCGTGCGGAAGCGAGGAGGAGAAGCATTCGCGTGATTCCGGGAGATTCAAGCATTCGCGTGCGGCGGGAGATTCAAGCGAGGAGGCGTGAAGCAAGCAAGCAAGCGCGTGGCGTGCGGCGGGAGAAGCAAGCGCGTGATTCGAGCGGGCGTGCGGAAGCGAGCGG
12"""
        extra_dataset_answer = """CGGCGGGAGATT CGGGAGATTCAA CGTGCGGCGGGA CGTGGAGGCGTG CGTGGCGTGCGG GCGTGCGGCGGG GCGTGGAGGCGT GCGTGGCGTGCG GGAGAAGCGAGA GGAGATTCAAGC GGCGGGAGATTC GGGAGATTCAAG GTGCGGCGGGAG TGCGGCGGGAGA"""
        extra_ut = biogen.create_unittest_text(self.id, 'extra', extra_dataset, extra_dataset_answer)
        biogen.create_unittests(self.newpath, self.id, sample_ut, extra_ut)
        test_file_path = os.path.join(self.newpath, 'bio'+biogen.slugify(self.id).lower()+'_test.py')
        self.assertTrue(os.path.isfile(test_file_path))
        with open (test_file_path, "r") as myfile:
          test_contents=myfile.read()
        # Test if tests contain valid strings
        self.assertTrue('import bio' + biogen.slugify(self.id) in test_contents)
        self.assertTrue('bio' + biogen.slugify(self.id) + '.' + 'bio_' + biogen.slugify(self.id) in test_contents)
        self.assertTrue('class Bio' + biogen.slugify(self.id) + 'TestCase(unittest.TestCase)' in test_contents)

    def test_main(self):
        biogen.create_skeleton_code(self.newpath, self.id, 'return len(input)')
        main_file_path = os.path.join(self.newpath, 'bio'+biogen.slugify(self.id).lower()+'.py')
        print(main_file_path)
        self.assertTrue(os.path.isfile(main_file_path))
        with open (main_file_path, "r") as myfile:
          main_contents=myfile.read()
        self.assertTrue('def bio_' + biogen.slugify(self.id) + '(input):' in main_contents)

    def test_livetest(self):
        pass

    def test_activate(self):
        pass

    def test_deactivate(self):
        pass

    def test_virtualenv(self):
        pass


if __name__ == '__main__':
    unittest.main()
