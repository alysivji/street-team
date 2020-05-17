# Street Team Applications

## Directory

|Application|Description
|---|---|
|debug|Tools to help development and debug|
|events|Event management tools|
|mediahub|Collect media sent to site in a central location; display it to the world|
|twilio_integration|Integrate with twilio webhook to process messages received|
|users|Custom Django User class|
|website|Contains all logic related to the website view|

## Workflow

- New users create an account
- Users can create a new team or join an existing team (later)
  - New user is admin, can select other admins
- Team admin can create events and add members to team
  - Organizers
  - Leads (not yet, but later)
  - Members
- Events are planned activities / social engagements teams can take pictures for
  - All members and organizers of an event can upload pictures; caption their own pictures
  - Organizers can crop and approve for posting
