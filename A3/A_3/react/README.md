# Frontend

## Requests

URL                   | Method  | Content Type        | Body        | Response |
----------------------|---------|---------------------|-------------|----------|
/api/login            | POST    | application/json    |             |          |
/api/register         | POST    | application/json    |             |          |
/api/renew            | PUT     | N/A                 |             |          |
/api/logout           | POST    | N/A                 |             |          |
/api/check_auth       | POST    | N/A                 |             |          |
/api/check_permission | POST    | N/A                 |             |          |
/api/photos           | GET     |                     |             |          |
/api/upload           | POST    |                     |             |          |
/api/shares           | GET     |                     |             |          |
/api/share            | POST    |                     |             |          |
/api/share            | DELETE  |                     |             |          |
/api/tags             | GET     |                     |             |          |
/api/images           | GET     |                     |             |          |
/api/images           | DELETE  |                     |             |          |
/api/stats            | GET     |                     |             |          |
/api/public           | GET     |                     |             |          |

## TODO
- [ ] Login/Signup
    - [x] Design
    - [ ] Functionalities
- [ ] Photos page
    - [x] Re-design
    - [ ] Functionalities
    - [x] Tag
    - [x] is shared
- [ ] Image page
    - [x] Show Tag
    - [x] Show is shared
    - [x] Create Share
- [ ] Tags page
    - [x] Design
    - [ ] Functionalities
- [ ] Tag page
    - [x] Design
    - [ ] Functionalities
- [ ] Share Page
    - [x] Number of access
    - [x] Design
    - [ ] Functionalities
- [ ] Merge share and tags page into photos and use data-table
- [ ] Permission (User/Manager)
    - [x] Functionalities
- [ ] Admin
    - [x] Design
    - [ ] Functionalities
    - [x] Stats
    - [ ] All images
        - [x] Delete image
        - [x] Delete share
        - [ ] Functionalities
- [ ] Public page to access shared photo
    - [x] Design
    - [ ] Functionalities

# AWS Cognito