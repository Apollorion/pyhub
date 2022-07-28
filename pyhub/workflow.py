from __future__ import annotations
import inspect
import yaml
from .t import Concurrency, On, ActionCheckout, Action
from typing import List, Optional, Dict


def generate_needs(needs: list[str]) -> str:
    returnable = ""
    for need in needs:
        split = need.split(".")
        job = split[0]
        output = split[1]
        returnable = returnable + "\"${{ needs." + job + ".outputs." + output + " }}\", "

    if returnable == "":
        return ""
    return returnable[:-2]


def generate_action_checkout_dict(action_checkout: ActionCheckout) -> Action:
    action_checkout_step = None
    if action_checkout:
        action_checkout_step = Action(uses='actions/checkout@v3')
        if action_checkout is not None and not isinstance(action_checkout, bool):
            action_checkout_step['with'] = {}

            keys = ["repository", "ref", "token", "ssh_key", "ssh_known_hosts", "ssh_strict", "persist_credentials",
                    "path", "clean", "fetch_depth", "lfs", "submodules", "set_safe_directory"]
            for key in keys:
                if key in action_checkout and action_checkout[key] is not None:
                    action_checkout_step['with'][key.replace("_", "-")] = action_checkout[key]

    return action_checkout_step


def generate_steps(requirements_file, action_checkout, actions, func, run_string, working_directory):
    install_requirements_step = None
    if requirements_file is not None:
        install_requirements_step = {
            'name': 'Install Requirements',
            'run': f"python -m pip install {requirements_file}"

        }

    action_checkout_step = generate_action_checkout_dict(action_checkout)

    steps = []
    if action_checkout_step is not None:
        steps.append(action_checkout_step)

    if actions is not None:
        for action in actions:
            _with = action['_with'] if "_with" in action else {}
            _with2 = action['with'] if "with" in action else {}

            steps.append({
                'uses': action['uses'],
                'with': {**_with, **_with2}
            })

    if install_requirements_step is not None:
        steps.append(install_requirements_step)

    work = {
        'name': func.__name__,
        'id': 'run',
        'run': run_string
    }

    if working_directory is not None:
        work["working-directory"] = working_directory

    steps.append(work)

    return steps


def set_output(output_name: str, value: str):
    """
    Sets output to github actions
    :param output_name: Name of the output
    :param value:  Value of the output
    :return: None
    """
    print(value)


class Workflow:
    def __init__(self, name: str, on: On,
                 concurrency: Concurrency = None,
                 permissions: Optional[List[str]] = None,
                 env: Optional[Dict[str, str]] = None,
                 requirements_file: Optional[str] = None):
        self.jobs = {}
        self.name = name
        self.on = on
        self.concurrency = concurrency
        self.permissions = permissions
        self.env = env
        self.requirements_file = requirements_file

    def job(self,
            needs: Optional[List[str]] = None,
            runs_on: str = "ubuntu-latest",
            control: Optional[str] = None,
            env: Optional[Dict[str, str]] = None,
            action_checkout: Optional[bool | ActionCheckout] = False,
            actions: Optional[list[Action]] = None,
            outputs: Optional[list[str]] = None,
            working_directory: Optional[str] = None):

        if needs is None:
            needs = []

        def wrapped(func):
            # get the function value and remove the first line
            func_val = ''.join(line for line in inspect.getsource(func).splitlines(True)[1:])
            run_string = f'''python <<EOF
def set_output(output_name: str, value: str):
    print(f"::set-output name={{output_name}}::{{value}}")

{func_val}

{func.__name__}({generate_needs(needs)})
EOF
'''

            top_needs = []
            for need in needs:
                top_needs.append(need.split(".")[0])

            self.jobs[func.__name__] = {
                'runs-on': runs_on,
                'needs': top_needs,
                'outputs': {},
                'steps': generate_steps(self.requirements_file, action_checkout, actions, func, run_string, working_directory)
            }

            if outputs is not None:
                for name in outputs:
                    self.jobs[func.__name__]["outputs"][name] = f"${{{{ steps.run.outputs.{name} }}}}"

            if control is not None:
                self.jobs[func.__name__]["if"] = control

            if env is not None:
                self.jobs[func.__name__]["env"] = env

        return wrapped

    def make(self, outfile: Optional[str] = None, return_as: str = "file"):
        workflow = {
            'name': self.name,
            'on': self.on,
            'jobs': self.jobs
        }

        if self.concurrency is not None:
            workflow['concurrency'] = {}
            if "group" in self.concurrency and self.concurrency['group'] is not None:
                workflow['concurrency']['group'] = self.concurrency['group']
            if "cancel_in_progress" in self.concurrency and self.concurrency['cancel_in_progress'] is not None:
                workflow['concurrency']['cancel-in-progress'] = self.concurrency['cancel_in_progress']

        if self.permissions is not None:
            workflow['permissions'] = self.permissions

        if self.env is not None:
            workflow['env'] = self.env

        if outfile is None:
            outfile = "./workflow.yaml"

        if return_as == "file":
            f = open(outfile, "w")
            f.write(yaml.dump(workflow))
            f.close()

        if return_as == "dict":
            return workflow
