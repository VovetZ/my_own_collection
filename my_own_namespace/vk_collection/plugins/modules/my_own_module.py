#!/usr/bin/python

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: my_own_module
short_description: Custom module my_own_module
version_added: "1.0.0"
description: Custom module my_own_module
options:
    path:
        description: Path to file
        required: true
        type: str
    content:
        description: Content of the file
        required: false
        type: str
extends_documentation_fragment:
    - my_own_namespace.vk-netology.my_doc_fragment_name
author:
    - Vladimir Kuzevanov
'''

EXAMPLES = r'''
# Save content to file
- name: Create file
  my_own_namespace.vk-netology.my_own_module:
    path: "{{ path }}"
    content: "{{ content }}"
'''

RETURN = r'''
changed:
    description: If file changed
    type: bool
    returned: always
    sample: True
'''

from ansible.module_utils.basic import AnsibleModule
import os

def run_module():
    module_args = dict(
        path=dict(type='str', required=True),
        content=dict(type='str', required=False, default="Default content message")
    )
    result = dict(
        changed=False
    )
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    if module.check_mode:
        module.exit_json(**result)

    Path = module.params['path']
    newContent = module.params['content']

    if os.path.isfile(Path):
        fileContent = open(Path, "r").read()
        if fileContent == newContent:
            result['changed'] = False
            result['message'] = "File is already up to date"
            module.exit_json(**result)
    
    errorMessage = ""
    try:
        file = open(Path, "w")
        file.writelines(newContent)
    except Exception as e:
        errorMessage = str(e)
        result['changed'] = False
        result['message'] = "Error writing new content to" + Path
    else:
        result['changed'] = True
        result['message'] = "File " + Path + "created/overwrited with new content"
    
    if len(errorMessage) > 0:
        module.fail_json(msg=errorMessage, **result)
    else:
        file.close
        module.exit_json(**result)


def main():
    run_module()

if __name__ == '__main__':
    main()

