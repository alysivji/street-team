# Street Team Ansible Playbooks

This folder contains Ansible configuration settings to deploy Street Team on a VPS.

## `~/.bash_profile`

```bash
export STREETTEAM_DB_URI={}
export TWILIO_AUTH_TOKEN={}
export DJANGO_SECRET_KEY={}
```

## Deployment Workflow

1. `pip install ansible` installed the machine you will be deploying from
1. Check to see what the ansible playbook would do, we can run `ansible-playbook -i ./hosts site.yml --ask-become-pass -C`
1. Remove `-C` option to run playbook to deploy app
