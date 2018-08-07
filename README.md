# Ansible-Bugsnag-Module

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

