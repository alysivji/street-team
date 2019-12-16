# Street Team Ansible Playbooks

This folder contains Ansible configuration settings to deploy Street Team on a VPS.

## `~/.bash_profile`

```bash
export STREETTEAM_DB_URI={}
export DJANGO_SECRET_KEY={}

export STREETTEAM_GITHUB_CLIENT_ID={}
export STREETTEAM_GITHUB_CLIENT_SECRET={}

export STREETTEAM_TWILIO_ACCOUNT_SID={}
export STREETTEAM_TWILIO_AUTH_TOKEN={}
export STREETTEAM_TWILIO_SERVICE_SID={}
```

### Where to Find Keys

#### GitHub

https://github.com/settings/applications/

#### Twilio

Account SID / Auth Token: https://www.twilio.com/console/project/settings
Service SID: https://www.twilio.com/console/verify/services

## Deployment Workflow

1. `pip install ansible` installed the machine you will be deploying from
1. Check to see what the ansible playbook would do, we can run `ansible-playbook -i ./hosts site.yml --ask-become-pass -C`
1. Remove `-C` option to run playbook to deploy app
