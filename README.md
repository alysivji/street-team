# Street Team

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

### Django Admin Details

l / p = admin@dev.com / password
