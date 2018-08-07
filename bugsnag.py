#!/usr/bin/python

# Copyright: (c) 2018, Soroush Atarod <atarod@infinitypp.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import fetch_url

### Documentation
ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: bugsnag
short_description: Reports application builds
description:
    - Creates a new application release on Bugsnag
version_added: "1.0"
author: Soroush Atarod @_atarod
options:
    api_key:
        required: true
        description:
            - API Key of the Bugsnag account
    app_version:
        required: true
        description:
            - The version number of the application.
    release_stage:
        required: true
        description:
            - The release stage 
    builder_name:
        default: 'none'
        description:
            - The name of the entity that triggered the build. Could be a user, system etc
    source_control_repository:
        description:
            - Link to the source control
    source_control_revision:
        description:
            - The source control SHA-1 hash for the code that has been built
notes: check_mode is supported
'''

EXAMPLES = '''
# Adds or modify the backend '212.1.1.1' to a
# without source control
- name: create BugsNag API
  bugsnag:
    api_key: '122'
    builder_name: 'Jenkins'
    release_stage: 'production'
    app_version: '132135467'
    source_control_repository: 'https://github.com/owner/repo'
    source_control_revision: '123qwe213'

'''

RETURN = '''
'''

def main():

    # required_together this means that these two parameters needs to be
    # specified together. If source_control_repository is specified
    # then source_control_revision has to be specified as-well
    required_together = [['source_control_repository', 'source_control_revision']]

    # we declare the parameters of our Module here
    # bugsnag needs api_key, api_version and release_stage always
    # as a result will set the required value to True. We won't be logging the API_KEY
    # for security reason. the rest are optional
    arguments = dict(
            api_key=dict(required=True, no_log=True),
            app_version=dict(required=True),
            release_stage=dict(required=True),
            builder_name=dict(required=False),
            source_control_repository=dict(required=False),
            source_control_revision=dict(required=False)
        )

    # we pass the parameters to AnsibleModule class
    # we declare that this module supports check_mode as-well
    module = AnsibleModule(
        argument_spec=arguments,
        required_together=required_together,
        supports_check_mode=True
    )

    # Bugsnag requires raw-json data
    # this is why we will create a dict called "params"

    params = {
        'apiKey': module.params['api_key'],
        'appVersion': module.params['app_version']
    }

    headers = {'Content-Type': 'application/json'}

    if module.params['builder_name']:
        params['builderName'] = module.params['builder_name']

    if module.params['release_stage']:
        params['releaseStage'] = module.params['release_stage']

    if module.params['source_control_repository'] and module.params['source_control_revision']:
        params['sourceControl'] = {}

    if module.params['source_control_repository']:
        params['sourceControl']['repository'] = module.params['source_control_repository']

    if module.params['source_control_revision']:
        params['sourceControl']['revision'] = module.params['source_control_revision']

    # Bugsnag API URL
    url = 'https://build.bugsnag.com/'

    if module.check_mode:
        module.exit_json(changed=True)

    # We will be using Ansible fetch_url method to call API requests. We don't want to
    # use Python requests as its best to use the utils provided by Ansible.
    response, info = fetch_url(module, url, module.jsonify(params), headers=headers)

    # we receive status code 200 we will return it TRUE
    if info['status'] == 200:
        module.exit_json(changed=True)
    else:
        module.fail_json(msg="unable to call API")


if __name__ == '__main__':
    main()
