# Street Team

Tools to simplify work related to event marketing.

## Instructions

See `Makefile` for now.

## Roadmap

- [ ] draw out user flow diagram for app interaction
  - [ ] save everything that comes in
  - [ ] just sms
    - [ ] copy > 5 message
  - [ ] 1 - 5 pictures
    - [ ] we receive your picture(s). Thank you!
  - [ ] > 5 pictures
    - [ ] Somethign went wrong. You may have forgotten to attach a picture. Remember you can attach up to 5 pictures per message!
  - [ ] how to handle users that have not registered with website (not in MVP)
- [ ] get happy path working with tests
- What are other media thigns we can send?
  - [`content-types` Twilio accepts](https://www.twilio.com/docs/sms/accepted-mime-types)
  - [ ] send a pdf
  - [ ] send a voice memo
  - [ ] send a contact
  - [ ] send a ???

## Production Todo

- [ ] security
  - [ ] [lock down endpoint](https://www.twilio.com/docs/usage/tutorials/how-to-secure-your-django-project-by-validating-incoming-twilio-requests)
  - [ ] [Security docs](https://www.twilio.com/docs/usage/security)
  - [ ] [anti-fraud developer's guide](https://www.twilio.com/docs/usage/anti-fraud-developer-guide)
  - [ ] [Django docs](https://docs.djangoproject.com/en/2.2/topics/security/)
- [ ] permissions
- [ ] versioning
- [ ] restrict content-type
- [ ] https://www.django-rest-framework.org/topics/ajax-csrf-cors/
