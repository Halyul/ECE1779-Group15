# Frontend

## Requests

URL                   | Method  | Content Type        | Body             | Response                                   |
----------------------|---------|---------------------|------------------|------------------------------------------- |
/api/photos           | GET     | `application/json`  | `{admin: false}` | `@see: routes/libs/api.js/retrieveKeys`    |
/api/key/{key}        | GET     | `application/json`  | `N/A`            | `@see: routes/libs/api.js/retrieveImage`   |
/api/key/{key}        | DELETE  | `application/json`  | `{admin: false}` | `@see: routes/libs/api.js/deleteImage`     |
/api/upload           | POST    |`multipart/form-data`| `file`, `key`    | `@see: routes/libs/api.js/upload`          |
/api/share            | POST    | `application/json`  | `key`            | `@see: routes/libs/api.js/createShare`     |
/api/share            | DELETE  | `application/json`  | `key`, `{admin: false}`|`@see: routes/libs/api.js/deleteShare`|
/api/photos           | GET     | `application/json`  | `{admin: true}`  | `@see: routes/libs/api.js/retrieveKeys`    |
/api/key/{key}        | DELETE  | `application/json`  | `{admin: true}`  | `@see: routes/libs/api.js/deleteImage`     |
/api/share            | DELETE  | `application/json`  | `key`, `{admin: true}`|`@see: routes/libs/api.js/deleteShare`|
/api/stats            | GET     | `application/json`  | `N/A`            | `@see: routes/libs/api.js/getStats`        |
/api/public/{key}     | GET     | `application/json`  | `N/A`            | `@see: routes/libs/api.js/retrieveImage`   |

## TODO
- [x] Login/Signup
    - [x] Design
    - [x] Functionalities
- [x] Photos page
    - [x] Re-design
    - [x] Functionalities
    - [x] Tag
    - [x] is shared
- [x] Image page
    - [x] Show Tag
    - [x] Show is shared
    - [x] Create Share
- [x] Merge share and tags page into photos and use data-table
- [x] Permission (User/Manager)
    - [x] Functionalities
- [x] Admin
    - [x] Design
    - [x] Functionalities
    - [x] Stats
    - [x] All images
        - [x] Delete image
        - [x] Delete share
        - [x] Functionalities
- [x] Public page to access shared photo
    - [x] Design
    - [x] Functionalities
- [ ] Cognito README
- [ ] Integration