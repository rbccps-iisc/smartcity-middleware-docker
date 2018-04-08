# UNREGISTER API

To De-Register entities from the middleware, the Users can call this API with the following parameters.

* `apikey` of the owner who registered the entity


**URL** : `https://localhost:10443/api/1.0.0/register`

**Method** : `DELETE`

**Auth required** : YES

**Curl example**
Entity named app will be removed.

```bash
curl -ik -X DELETE https://localhost:10443/api/1.0.0/register \
-H 'apikey:  guest' \
-d '{"entityID": "app"}'
```
## Success Response

**Code** : `200 OK`

**Content example**

```json
{"response": "app6 entity removed. ", "status": "success"}
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
