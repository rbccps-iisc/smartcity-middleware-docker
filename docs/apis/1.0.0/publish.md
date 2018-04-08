# PUBLISH API

To publish data to the middleware, devices can use the API with the following parameters in the body.

* `apikey` is required. This apikey is obtained during the registration of an entity. (its not user apikey eg. guest)

**URL** : `https://localhost:10443/api/1.0.0/publish`

**Method** : `POST`

**Auth required** : YES

**Curl example**

```bash
curl --insecure -i -X POST https://localhost:10443/api/1.0.0/publish \
-H 'apikey: 219bf59341e24fe2901f52b0f8fbbff6' \
-d '{"body": "turn ON streetlight"}'
```

## Success Response

**Code** : `200 OK`

**Content example**

```json
Publish message OK
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
