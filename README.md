# Street Team

Tools to simplify work related to event marketing.

## Instructions

See `Makefile` for now.

## Roadmap

- [ ] draw out user flow diagram for app interaction
  - [x] implement
- [x] get happy path working with tests
- What are other media thigns we can send?
  - [`content-types` Twilio accepts](https://www.twilio.com/docs/sms/accepted-mime-types)
  - [ ] send a pdf
  - [ ] send a voice memo
  - [ ] send a contact
  - [ ] send a ???

## Production Todo

- [ ] `factory-boy` for testing
- [ ] security
  - [x] [Security docs](https://www.twilio.com/docs/usage/security)
    - [x] Validate request is from Twilio
    - [ ] HTTP Digest Auth (figure out how to do this)
  - [x] [anti-fraud developer's guide](https://www.twilio.com/docs/usage/anti-fraud-developer-guide)
  - [ ] [Django docs](https://docs.djangoproject.com/en/2.2/topics/security/)
  - `https` via traefik
- [ ] permissions
- [ ] versioning
- [ ] restrict content-type
- [ ] https://www.django-rest-framework.org/topics/ajax-csrf-cors/
- [ ] serving static files in production
  - [ ] https://docs.djangoproject.com/en/2.2/howto/static-files/deployment/
  - [ ] https://docs.djangoproject.com/en/2.2/howto/static-files/#serving-static-files-during-development
  - [ ] Maybe use S3?
- [ ] build out CI, check out azure pipelines

## Updating Dependencies

- use [pip-tools](https://github.com/jazzband/pip-tools/) to manage dependencies
