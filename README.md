# Application Tracker

This is a backend only implementation of a job application tracker with the capabilities of:
- viewing applications
- creating new applications
- adding comments on individual applications
- approving/rejecting applications
- removing applications
  
---

## API
This API is managed through two endpoints:
- /applications/
- /comments/

  

### `GET /applications/`

Returns a list of all applications\
Requires group: "AppViewer"

### `GET /applications/{app-id}/`\
Returns an individual application, will all associated comments\
Requires group: "AppViewer"

### `POST /applications/`\
Creates a new application\
Requires group: "AppCreator"\
JSON Payload:\
```
{
  "applicant_name": str,
  "status"(optional): str(choices of "SUBMITTED", "APPROVED", "REJECTED"),
}
```

### `PATCH/PUT /applications/{app-id}/`\
Edit an application\
Requires group: "AppApprover"\
JSON Payload:\
```
{
  "status": str(choices of "SUBMITTED", "APPROVED", "REJECTED")
}
```

### `DELETE /applications/{app-id}/`\
Delete an application\
Requires group: "AppEditor"\

### `POST /comments/`\
Create a comment\
Requires group: "AppEditor:\
JSON Payload:\
```
{
  "application": int(app-id),
  "text": str(limit 200 characters)
}
```

---
## Usage

Spin up containers:
- `docker-compose up -d`

Perform migrations:
- `docker-compose exec web python manage.py migrate`

Run tests:
- `docker-compose exec web pytest`

I added a data migration to pre-populate the users and user groups:
- admin:password - superuser with all permissions
- app_viewer:password
- app_creator:password
- app_editor:password
- app_approver:password


You can utilize curl to make request:
```
curl -vv \
-X GET \
-u 'admin:password' \
http://localhost:8654/applications/
```

---
## Design Decisions

There was a lot of initial setup work, but I found it very useful because almost the entirety of my django development work has
been on existing systems with already well defined structures.

Since this is a very simple CRUD API, I tried to leverage Django Rest Framework's Viewset as much as possible, essentially not
needing to write individual codefor each different CRUD interaction. This proved pretty useful and no customer @actions were needed

Working with permissions to the specifications, I had to provide a different level of permission use for each type of operation
(list, create, update, retrieve, destroy). This allows for each operation to have a different list of groups that can perform
each action. I went with groups more because I had familiarity with it, but I believe individual permissions could also be used
since the prompt listed permission levels for each interaction.

While everything is pretty bare bones now, there is some flexibility with the serializers to display/allow edits of only certain
fields. For example, the owner of an application could be able to view his/her information, but not see any comments being made.

This was my first time working with pytest, most of my previous experience was with django's and DRF's test framework. The model
bakery and parameterized tools work just the same, so everything was pretty seamless.

I have a lot of familiarity with black and flake8; set up pre-commit hooks for all 3 tools to use while developing.
