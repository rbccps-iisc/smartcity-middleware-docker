# SUBSCRIBE API

To subscribe for data / commands from the middleware, use the API with the following parameters.

* `apikey` is required. This apikey is obtained during the registeration of an entity. (its not user apikey eg. guest)

* `name` refers to the entityID

**URL** : `https://localhost:10443/api/1.0.0/subscribe?name=<entityID>`

**Method** : `GET`

**Auth required** : YES

**Curl example**

```bash
curl -ik -X GET "https://localhost:10443/api/1.0.0/subscribe?name=streetlight" -H 'apikey: 219bf59341e24fe2901f52b0f8fbbff6'
```

## Success Response

**Code** : `200 OK`

**Content example**

```json
Data..
Data..
Data..
...

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
