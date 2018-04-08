# DATABASE API

Used by Application to get archived data of an entity from the database.

**URL** : `https://localhost:10443/api/1.0.0/db`

**Method** : `GET`

**Auth required** : NO

**Curl example**

```bash
curl --insecure -i -X GET https://localhost:10443/api/1.0.0/db \
-H 'apikey: 5667f573271f47fd847a1bfe922daf30' \
-d '{ "query": { "match": { "key": "streetlight" } } }'
```
## Success Response

**Code** : `200 OK`

**Content example**

```json
{
  "took" : 4,
  "timed_out" : false,
  "_shards" : {
    "total" : 5,
    "successful" : 5,
    "failed" : 0
  },
  "hits" : {
    "total" : 13864,
    "max_score" : null,
    "hits" : [
        {
        "_index" : "sensor_data",
        "_type" : "logs",
        "_id" : "AV6eg3yAh735b9FofAMo",
        "_score" : null,
        "_source" : {
          "ambientLux" : 550,
          "dataSamplingInstant" : 8698322,
          "powerConsumption" : 0,
          "@timestamp" : "2017-09-20T08:59:30.808Z",
          "caseTemperature" : 24,
          "slaveAlive" : true,
          "@version" : "1",
          "luxOutput" : 790,
          "routing-key" : "70b3d58ff0031de5",
          "batteryLevel" : 3265
        },
        "sort" : [
          1505897970808
        ]
      }
    ]
  }
}
```
