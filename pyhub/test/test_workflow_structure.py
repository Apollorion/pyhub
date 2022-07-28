import unittest
from pyhub.workflow import Workflow
from pyhub.t import On


def test_function():
    print("test_function_print")


class TestWorkflowStructure(unittest.TestCase):

    def test_env_top_level(self):
        """
        Env Vars defined in the workflow class should be top level in the file
        """
        env_dict = {"var1": "var1Value"}
        workflow = Workflow("test", On(push={}), env=env_dict)
        made = workflow.make(return_as="dict")

        self.assertIn("env", made)
        self.assertDictEqual(made["env"], env_dict)

    def test_workflow_name(self):
        """
        workflows should have names
        """

        workflow = Workflow("test", On(push={}))
        made = workflow.make(return_as="dict")

        self.assertIn("name", made)
        self.assertEqual(made["name"], "test")

    def test_permissions(self):
        """
        permissions exist when used
        """
        workflow = Workflow("test", On(push={}), permissions=["write-all"])
        made = workflow.make(return_as="dict")

        self.assertIn("permissions", made)
        self.assertEqual(made["permissions"], ["write-all"])

    def test_job_exists(self):
        """
        jobs should exist when used
        """

        workflow = Workflow("test", On(push={}))
        wrapped = workflow.job()
        wrapped(test_function)
        made = workflow.make(return_as="dict")

        self.assertIn("jobs", made)
        self.assertIn("test_function", made["jobs"])

    def test_on(self):
        """
        on keyword exists in file
        """
        workflow = Workflow("test", On(push={}))
        made = workflow.make(return_as="dict")

        self.assertIn("on", made)
        self.assertEqual(made["on"], {"push": {}})
