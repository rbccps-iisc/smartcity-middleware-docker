# VIDEO RTMP API

To access video data from the middleware, devices can use this API with the following parameters in the body.

* `apikey` is required. This apikey is obtained during the registration of an entity. (its not user apikey eg. guest)

**URL** : `https://localhost:10443/api/1.0.0/video.rtmp`

**Method** : `GET`

**Auth required** : YES

**Curl example**

```bash
curl --insecure -i -X GET https://localhost:10443/api/1.0.0/video.rtmp?stream=stream_name&id=entityid&apikey=entity_api_key

```

## Success Response

**Code** : `301 Moved Permanently`

**Content example**

```
HTTP/1.1 301 Moved Permanently
Date: Tue, 15 May 2018 12:32:44 GMT
Content-Type: text/plain
Content-Length: 0
Location: rtmp://video1.rbccps.org/live1/stream_name?user=entity_id&pass=entity_api_key
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
