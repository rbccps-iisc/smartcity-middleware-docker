# UNSHARE API

Used by entity to remove share access of a follower.
To remove share access of your data for a follower, use the API with the following parameters in the body.


* `apikey` of the entity who will remove access
* `entityID` refers to the name of the entity to whom data was shared
* `permission` can be read, write, read-write. Permission will be revoked to interested entity.

**URL** : `https://localhost:10443/api/1.0.0/share`

**Method** : `DELETE`

**Auth required** : YES

**Curl example**
Entity with `apikey` 4aefb1678fa74ce183edb44c79405dc1 (camera) removes sharing of its data with `app1` with only `read` permission.

```bash
curl -ik -X DELETE https://localhost:10443/api/1.0.0/share \
-H 'apikey:  4aefb1678fa74ce183edb44c79405dc1' \
-d '{"entityID": "app1", "permission":"read"}'
```
## Success Response

**Code** : `200 OK`

**Content example**

```json
Read access given to app1 at camera exchange removed.
```
## Error Response

**Condition** : If `apikey` is wrong.

**Code** : `403 FORBIDDEN`

**Content** :

```json
{
"message": "Invalid authentication credentials"
}
```
