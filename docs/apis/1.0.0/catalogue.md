# CATALOGUE API

Used by applications to find the entities registered in ideam.

**URL Without Search** : `https://localhost:10443/api/1.0.0/cat`

**URL With Search** : `https://localhost:10443/api/1.0.0/cat?<key>=<value>`

**Method** : `GET`

**Auth required** : NO

**Curl example**
Without Search
```bash
curl -X GET -k https://localhost:10443/api/1.0.0/cat
```
With Search
```bash
curl -X GET -k https://localhost:10443/api/1.0.0/cat?resourceType=streetlight
```
## Success Response

**Code** : `200 OK`

**Content example**

```json
{
 Schema document of the entity
}

```
