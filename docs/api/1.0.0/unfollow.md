# UNFOLLOW API

To un-follow (remove interest) about a subscribed data, use the API with the following parameters in the body

* `apikey` of the entity requesting data access
* `entityID` refers to the name of the entity whose data is required
* `permission` can be read, write, read-write. Permission will be mentioned to interested entity.
**URL** : `https://localhost:10443/api/1.0.0/follow`

**Method** : `DELETE`

**Auth required** : YES

**Curl example**
Entity with `apikey` 4d04c10f5bf24d4f8aa93529e34wer is requesting entity `camera` to remove `read` permission. The permission will be removed immediately.

```bash
curl --insecure -i -X DELETE https://localhost:10443/api/1.0.0/follow \
-H 'apikey: 4d04c10f5bf24d4f8aa93529e34wer' \
-d '{"entityID": "camera", "permission":"read"}'
```
## Success Response

**Code** : `200 OK`

**Content example**

```json
unfollow success
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
