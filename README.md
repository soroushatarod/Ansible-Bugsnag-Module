# Ansible-Bugsnag-Module

1. How to import the module?

a) Create a folder "library".
b) Save bugsnag.py in it.


Sample playbook.yml

```yaml
- hosts: localhost
  tasks:
    - name: create BugsNag API
      bugsnag:
        api_key: '333fc26d'
        builder_name: 'Jenkins'
        release_stage: 'production'
        app_version: '132135467'

