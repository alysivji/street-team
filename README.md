# Street Team

[![Build Status](https://travis-ci.com/alysivji/street-team.svg?branch=master)](https://travis-ci.com/alysivji/street-team)
[![codecov](https://codecov.io/gh/alysivji/street-team/branch/master/graph/badge.svg)](https://codecov.io/gh/alysivji/street-team)
[![License: MIT](https://img.shields.io/badge/License-MIT-red.svg)](https://opensource.org/licenses/MIT)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

Tools to simplify work related to event marketing.

## Project Information

Organizing events is a thankless job.
There are many moving pieces that go into planning an event
and then running it the day of.

It is unreasonable to ask event organizers
to take pictures and operate social media
on top of the laundry list of things they are responsibile for.

[Chicago Python](https://www.chipy.org) has grown in 2019:
from 2-3 events/month to 5-8 events/month.
Having a dedicated individual attend all events
to manage social media is a tall ask.
Multiple resources would ease the workload,
but requires coordination ahead of time.

### Introducing the Chicago Python Street Team

Have you ever wondered how you can help Chicago Python
in the limited time you have?
You're in luck!
We've built a platform to enable our community to
help us manage our social media channels.

Take a picture while at a Chicago Python event
and text it to the group inbox!
The social media manager will review all pictures
and  use the appropriate ones for social media posts.

Outsourcing to the community FTW!!

### Current Features

- Send a text message with 1-5 images to a phone number
  - this image could be featured in a Chicago Python social media post!

### Upcoming Roadmap

- Login to add caption to pictures and add to the Twitter queue
  - Social Media Manager will approve tweets to be published

### Etymology

A [**street team**](https://en.wikipedia.org/wiki/Street_team)
is a group of volunteers who "hit the streets"
to promote an event or a product.

## Contributing

### Set up Development Environment

1. Fork and clone repo
1. Create and activate virtual environment
1. `pip install pre-commit==1.20.0`
1. `pre-commit install`
1. `pip install -r requirements.txt`
1. Point IDE's PYTHONPATH to the virtualenv's Python binary

`make up` to start server

### Updating Dependencies

- use [pip-tools](https://github.com/jazzband/pip-tools/) to manage dependencies
- add new dependency to `requirements.in` and run `make requirements`

## Notes

### Django Admin Details

l / p = admin@dev.com / password

### Dump Production Database

```console
pg_dump -h ${POSTGRES_HOST} -U ${STREET_TEAM_USER} -p ${POSTGRES_PORT} ${STREET_TEAM_DB} > dbdump.sql
rsync -vr -e ssh ${user}@${vps_ip}:${path_to_file} [path_to_save_to]
pg_restore -d 'postgres://streetteam_user:streetteam_password@0.0.0.0:9432/streetteam' --jobs 4 dbdump.sql
```

### Sample Data Migration

```python
from datetime import datetime
from django.db import migrations


def add_default_datetimes_to_newly_created_column(apps, schema_editor):

    MediaResource = apps.get_model("mediahub", "MediaResource")
    all_records = MediaResource.objects.all()
    for record in all_records.iterator():
        record.created_at = datetime.utc()
        record.updated_at = datetime.utc()
        record.save()


class Migration(migrations.Migration):

    dependencies = [
        ('mediahub', '0002_add_datetime_fields_to_model'),
    ]

    operations = [
        migrations.RunPython(add_default_datetimes_to_newly_created_column, reverse_code=migrations.RunPython.noop)
    ]
```

### Django-Watchman

We are using [Django-Watchman](https://github.com/mwarkentin/django-watchman) to monitor services.

Dashboard: http://0.0.0.0:8100/watchman/dashboard/

### LocalStack

We are using [LocalStack](https://github.com/localstack/localstack) to replicate an S3-like object store for development.

```bash
export AWS_ACCESS_KEY_ID=foo
export AWS_SECRET_ACCESS_KEY=foo

# make bucket
aws --endpoint-url=http://localhost:4566 --region us-east-1 s3api create-bucket --bucket streetteam --acl public-read

# upload file
aws --endpoint-url=http://localhost:4566 --region=us-east-1 s3 cp requirements.txt s3://streetteam

# list bucket
aws --endpoint-url=http://localhost:4566 --region=us-east-1 s3 ls s3://streetteam

# view file
http://localhost:4566/streetteam/requirements.txt
```
