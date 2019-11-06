# Street Team

Tools to simplify work related to event marketing.

## Instructions

See `Makefile` for now.

## Updating Dependencies

- use [pip-tools](https://github.com/jazzband/pip-tools/) to manage dependencies

## Todo

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

- [ ] security
  - [x] [Security docs](https://www.twilio.com/docs/usage/security)
    - [x] Validate request is from Twilio
  - [x] [anti-fraud developer's guide](https://www.twilio.com/docs/usage/anti-fraud-developer-guide)
  - [x] [Django docs](https://docs.djangoproject.com/en/2.2/topics/security/)
  - [ ] [Django deployment checklist](https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/)
  - [ ] `https` via traefik
    - [ ] [other django configuration](https://docs.djangoproject.com/en/2.2/topics/security/#ssl-https)
    - [ ] `CSRF_COOKIE_SECURE` and `SESSION_COOKIE_SECURE`
- [x] https://www.django-rest-framework.org/topics/ajax-csrf-cors/
- [ ] serving static files in production
  - [ ] `STATIC_ROOT` and `STATIC_URL`
  - [ ] `MEDIA_ROOT`, `MEDIA_URL`, and `FILE_UPLOAD_PERMISSIONS`
  - [ ] https://docs.djangoproject.com/en/2.2/howto/static-files/deployment/
  - [x] https://docs.djangoproject.com/en/2.2/howto/static-files/#serving-static-files-during-development
  - [ ] Maybe use S3?
    - https://coderbook.com/@marcus/how-to-store-django-static-and-media-files-on-s3-in-production/
    - https://testdriven.io/blog/storing-django-static-and-media-files-on-amazon-s3/
    - https://medium.com/@manibatra23/setting-up-amazon-s3-bucket-for-serving-django-static-and-media-files-3e781ab325d5
    - https://www.codingforentrepreneurs.com/blog/s3-static-media-files-for-django/
- [ ] logging
  - [ ] JSON logging
  - [ ] [Filtering error reports](https://docs.djangoproject.com/en/2.2/howto/error-reporting/#filtering-error-reports)
- [ ] sentry
- [ ] `python manage.py check --deploy`

## Roadmap

- [ ] `factory-boy` for testing
- [ ] permissions
- [ ] build out CI, check out azure pipelines
  - [ ] needs to be public first
  - [ ] build out CD pipeline -- release + watchtower
- [ ] api versioning
- [ ] restrict content-type
- [ ] [HTTP Digest Authentication](https://www.twilio.com/docs/usage/security)
