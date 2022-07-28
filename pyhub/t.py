from typing import TypedDict, Optional


class Concurrency(TypedDict, total=False):
    group: Optional[str]
    cancel_in_progress: Optional[str | bool]


class TypesList(TypedDict, total=False):
    types: list[str]


class On(TypedDict, total=False):
    branch_protection_rule: Optional[TypesList]
    check_run: Optional[TypesList]
    check_suite: Optional[TypesList]
    create: Optional[bool]  # Need to add conditional for this and all other optional bools
    delete: Optional[bool]
    deployment: Optional[bool]
    deployment_status: Optional[bool]
    discussion: Optional[TypesList]
    discussion_comment: Optional[TypesList]
    fork: Optional[bool]
    gollum: Optional[bool]
    push: Optional[dict]
    # TODO: add the rest


class ActionCheckout(TypedDict, total=False):
    repository: Optional[str]
    ref: Optional[str]
    token: Optional[str]
    ssh_key: Optional[str]
    ssh_known_hosts: Optional[str]
    ssh_strict: Optional[str]
    persist_credentials: Optional[str]
    path: Optional[str]
    clean: Optional[str]
    fetch_depth: Optional[str]
    lfs: Optional[str]
    submodules: Optional[str]
    set_safe_directory: Optional[str]


Action = TypedDict("Action", {'uses': str, 'with': Optional[object], '_with': Optional[object]}, total=False)
