# FOLLOW API

Used by entities (subscribers) to follow (express interest) about data produced by another entity
* `apikey` of the entity requesting data access
* `entityID` refers to the name of the entity whose data is required
* `permission` can be read, write, read-write. Permission will be mentioned to interested entity.
**URL** : `https://localhost:10443/api/1.0.0/follow`

**Method** : `POST`

**Auth required** : YES

**Curl example**
Entity with `apikey` 9810db90bb6f4c3eae98359d080ac1fe is requesting entity `camera` for `read` permission. The approval
will happen when camera owner does a sharing of the device with read access only.

```bash
curl -ik -X POST https://localhost:10443/api/1.0.0/follow \
-H 'apikey: 9810db90bb6f4c3eae98359d080ac1fe' \
-d '{"entityID": "camera", "permission":"read"}'
```
## Success Response

**Code** : `200 OK`

**Content example**

```json
A follow request has been made to entity camera with read access at 2018-04-08 10:08:01 GMT.
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
