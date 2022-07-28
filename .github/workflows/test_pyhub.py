from pyhub.workflow import Workflow
from pyhub.t import On

workflow = Workflow("Test Pyhub", On(push={"branches": ["run-tests"]}))

install_python_3_10 = """
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3.10
"""

@workflow.job(action_checkout=True, working_directory="pyhub/test", interpreter="python3.10", raw_bash=install_python_3_10)
def test_pyhub():
    import glob
    import unittest
    import pip

    pip.main(["install", "../../"])

    test_files = glob.glob('test_*.py')
    module_strings = [test_file[0:len(test_file) - 3] for test_file in test_files]
    suites = [unittest.defaultTestLoader.loadTestsFromName(test_file) for test_file in module_strings]
    test_suite = unittest.TestSuite(suites)
    test_runner = unittest.TextTestRunner().run(test_suite)
    print(test_runner)


workflow.make(outfile="./test_pyhub.yaml")
