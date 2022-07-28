from pyhub.workflow import Workflow
from pyhub.types import Concurrency, On, ActionCheckout, Action

workflow = Workflow("My Amazing Test Workflow",
                    On(push={}),
                    concurrency=Concurrency(group="main"),
                    permissions=["write-all"],
                    env={
                        'TEST': 'test',
                        'A': 'false'
                    },
                    requirements_file="requirements.txt")


@workflow.job(needs=["test2"], env={'this': 'isgood'}, action_checkout=ActionCheckout(ref='main'), actions=[Action(uses="actions/install-python", _with={"test": "yes"})])
def test1(output_from_test_2):
    print(output_from_test_2)


@workflow.job(control="github.ref_name == 'main'", runs_on="custom-runner")
def test2():
    return "test2 returned"


workflow.make()
