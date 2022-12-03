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
/api/users            | GET     |                     |             |          |
/api/users            | POST    |                     |             |          |
/api/users            | DELETE  |                     |             |          |
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
- [ ] Tag page
    - [ ] Design
    - [ ] Functionalities
- [ ] Share Page
    - [x] Number of access
    - [x] Design
    - [ ] Functionalities
- [ ] Permission (User/Manager)
    - [ ] Design
    - [ ] Functionalities
- [ ] Admin
    - [ ] Design
    - [ ] Functionalities
    - [ ] Stats
    - [ ] All images
        - [ ] Delete image
        - [ ] Delete share
    - [ ] All users
        - [ ] Assign roles
        - [ ] Create/Delete
    - [ ] To modify user info? PUT /api/users
- [ ] Public page to access shared photo
    - [x] Design
    - [ ] Functionalities