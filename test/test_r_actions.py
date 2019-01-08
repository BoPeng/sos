#!/usr/bin/env python
#
# Copyright (c) Bo Peng and the University of Texas MD Anderson Cancer Center
# Distributed under the terms of the 3-clause BSD License.

import os
import shutil
import unittest

from sos.parser import SoS_Script
from sos.targets import file_target
from sos.utils import env
from sos.workflow_executor import Base_Executor


class TestActions(unittest.TestCase):
    def setUp(self):
        env.reset()
        self.temp_files = []

    def tearDown(self):
        for f in self.temp_files:
            if file_target(f).exists():
                file_target(f).unlink()

    @unittest.skipIf(not shutil.which('Rscript') or not shutil.which('pandoc'), 'R or pandoc not installed')
    def testRmarkdown(self):
        '''Test action Rmarkdown'''
        if file_target('myreport.html').exists():
            file_target('myreport.html').unlink()
        script = SoS_Script(r'''
[10]

report:
## Some random figure

Generated by matplotlib


[100]
# generate report
output: 'myreport.html'
Rmarkdown(output=_output[0])
''')
        wf = script.workflow()
        Base_Executor(wf, config={'report_output': 'report.md'}).run()
        self.assertTrue(os.path.isfile('myreport.html'))
        #
        file_target('myreport.html').unlink()

    @unittest.skipIf(not shutil.which('Rscript') or not shutil.which('pandoc'), 'R or pandoc not installed')
    def testRmarkdownWithInput(self):
        # Rmarkdown with specified input.
        script = SoS_Script(r'''
[10]
report: output='a.md'
## Some random figure

Generated by matplotlib


[100]
# generate report
output: 'myreport.html'
Rmarkdown(input='a.md', output=_output[0])
''')
        wf = script.workflow()
        Base_Executor(wf).run()
        self.assertTrue(os.path.isfile('myreport.html'))
        if file_target('myreport.html').exists():
            file_target('myreport.html').unlink()

#     def testRmarkdownWithNoOutput(self):
#         # another case is no output, so output goes to standard output
#         # this cannot be tested in travis because of limit on log file.
#         script = SoS_Script(r'''
# [10]
# report: output='a.md'
# ## Some random figure
#
# Generated by matplotlib
#
#
# [100]
# # generate report
# Rmarkdown(input='a.md')
# ''')
#         wf = script.workflow()
#         Base_Executor(wf).run()

    @unittest.skipIf(not shutil.which('Rscript') or not shutil.which('pandoc'), 'R or pandoc not installed')
    def testRmarkdownWithActionOutput(self):
        script = SoS_Script(r'''
[10]
report: output='default_10.md'
A_10

[20]
report: output='default_20.md'
A_20

[100]
# generate report
Rmarkdown(input=['default_10.md', 'default_20.md'], output='output.html')
''')
        wf = script.workflow()
        Base_Executor(wf, config={'report_output': '${step_name}.md'}).run()
        for f in ['default_10.md', 'default_20.md', 'output.html']:
            self.assertTrue(file_target(f).exists())
            file_target(f).unlink()

    @unittest.skipIf(not shutil.which('Rscript') or not shutil.which('pandoc'), 'R or pandoc not installed')
    def testRmarkdownToStdout(self):
        script = SoS_Script(r'''
# generate report
Rmarkdown:
    # this is title
''')
        wf = script.workflow()
        Base_Executor(wf).run()


if __name__ == '__main__':
    unittest.main()
