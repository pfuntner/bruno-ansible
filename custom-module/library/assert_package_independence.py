#!/usr/bin/python

import re
import subprocess
from ansible.module_utils.basic import AnsibleModule

DOCUMENTATION = '''
---
module: assert_package_independence

description:
    - "Assert that a package does not depend on other packages"

options:
    package:
        description:
            - Name of package to check its dependencies
        required: true
    other_packages:
        description:
            - List of packages to check if the package depends on them
        required: true

usage notes:
  - Only being used and has tested on Ubuntu 20 so far.  Changes are likely needed to run on non-Debian distributions.
  - Designed to fail if `package` depends on one or more of the `other packages`.
'''

EXAMPLES = '''
- name: Assert iptables does not depend on ufw or nftables
  is_package_independent:
    package: iptables
    other_packages:
      - ufw
      - nftables
  become: yes
  become_user: root
  become_method: sudo
'''

RETURN = '''
A dictionary containing the following items.

    messages=[],  # messages via processing
    stdout="",    # raw stdout from `dpkg -s` command
    stderr="",    # raw stderr from `dpkg -s` command
    rc=None,      # raw exit status from `dpkg -s` command
    changed=False
'''


def main():
    """Checks `package` to see if any of the `other_packages` depend on it.

    Returns:
        Calls AnsibleModule.exit_json in order to return to Ansible with a result dictionary
    """

    # Define the available arguments/parameters that a user can pass to the module
    module_args = dict(
        package=dict(type='str', required=True),
        other_packages=dict(type='list', required=True),
    )

    # The result dictionary that gets returned to Ansible
    result = dict(
        changed=False,
        messages=[],
        stdout=[],
        stderr=[],
        rc=None,
    )

    # The AnsibleModule object will be our abstraction working with Ansible
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    try:
      p = subprocess.Popen(['dpkg', '-s', module.params['package']], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
      (result['stdout'], result['stderr']) = tuple([s.decode('utf-8') for s in p.communicate()])
      result['rc'] = p.wait()
    except Exception as e:
      result['messages'].append('Caught {!s}'.format(e))

    if result['rc'] == 0:
      regexp = re.compile(r'^Depends:\s+(.*)$')
      depends = []
      for line in result['stdout'].splitlines():
        match = regexp.search(line)
        if match:
          tokens = re.split(r',\s+', match.group(1))
          result['messages'].append(('Extracting dependencies from {!r}'.format(tokens)))
          for token in tokens:
            other_package = token.split()[0]
            if other_package in module.params['other_packages']:
              depends.append(other_package)
          break
  
      if depends:
        module.fail_json(msg='{package} depends on {other_packages}'.format(package=module.params['package'], other_packages=', '.join(depends)), **result)
    else:
      module.fail_json(msg='`dpkg -s` failed', **result)

    # Return to Ansible with the results
    module.exit_json(**result)

if __name__ == '__main__':
    main()
