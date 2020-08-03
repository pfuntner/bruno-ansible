#!/usr/bin/python

import subprocess
from ansible.module_utils.basic import AnsibleModule

DOCUMENTATION = '''
---
module: my_module

description:
    - "Trying out a custom module"

options:
    command:
        description:
            - Command to run on instance
        required: true
'''

EXAMPLES = '''
- name: Run custom module
  my_module:
    command: hostname
  become: yes
  become_user: root
  become_method: sudo
'''

RETURN = '''
A dictionary containing the following items.

    stdout=[],
    stderr=[],
    rc=None,
    changed=False
'''


def main():
    """Executes the module

    Returns:
        Calls AnsibleModule.exit_json in order to return to Ansible with a result dictionary
    """

    # Define the available arguments/parameters that a user can pass to the module
    module_args = dict(
        command=dict(type='str', required=True)
    )

    # The result dictionary that gets returned to Ansible
    result = dict(
        changed=False,
        stdout=[],
        stderr=[],
        rc=None
    )

    # The AnsibleModule object will be our abstraction working with Ansible
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    p = subprocess.Popen(module.params['command'].splitlines(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (result['stdout'], result['stderr']) = tuple([s.decode('utf-8') for s in p.communicate()])
    result['rc'] = p.wait()
    
    # Return to Ansible with the results
    module.exit_json(**result)


if __name__ == '__main__':
    main()
