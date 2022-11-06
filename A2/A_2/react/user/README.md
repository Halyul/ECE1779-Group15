# User Frontend

## Requests

URL            |  Method | Content Type        | Body      
---------------|---------|---------------------|-------------
/api/upload    | POST    | multipart/form-data | `file`, `key` 
/api/list_keys | POST    | application/json    | N/A
/api/key/<key> | POST    | application/json    | N/A                               

## TODO
- [x] Remove functionality to configure memcache settings.
- [x] Remove functionality that displays memcache statistics.