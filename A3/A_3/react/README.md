# Frontend

## Requests

URL         | Method | Content Type        | Body                     | Response                                    |
------------|--------|---------------------|--------------------------|---------------------------------------------|
/api/photos | POST   |`application/json`   |`user`, `role`, `admin`   | `@see: routes/libs/api.js/retrieveKeys`     |
/api/key    | POST   |`application/json`   |`key`, `user`, `role`     | `@see: routes/libs/api.js/retrieveImage`    |
/api/key    | DELETE |`application/json`   |`key`, `user`, `role`     | `@see: routes/libs/api.js/deleteImage`      |
/api/upload | POST   |`multipart/form-data`|`file`,`key`,`user`,`role`| `@see: routes/libs/api.js/upload`           |
/api/share  | POST   |`application/json`   |`key`,`user`,`role`       | `@see: routes/libs/api.js/createShare`      |
/api/share  | DELETE |`application/json`   |`key`,`user`,`role`       | `@see: routes/libs/api.js/deleteShare`      |
/api/stats  | POST   |`application/json`   |`user`,`role`             | `@see: routes/libs/api.js/getStats`         |

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
- [x] Cognito README
- [ ] Integration