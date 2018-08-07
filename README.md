# Ansible-Bugsnag-Module

<h2>How to import the module?</h2>

<ol>
<li>Create a folder "library"</li>
<li>Save bugsnag.py in it</li>
</ol>


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

