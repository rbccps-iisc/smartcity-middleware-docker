# REGISTER API

This API is used by a User to register entities (Devices or Applications).

* Apikey, content-type, entity schema is required.
For details on schema, visit following URL https://github.com/rbccps-iisc/smart_cities_schemas

`Note: a guest User is available in the ideam with apikey as guest.

**URL** : `https://localhost:10443/api/1.0.0/register`

**Method** : `POST`

**Auth required** : YES

**Curl example**

```bash
curl -X POST \
  https://localhost:10443/api/1.0.0/register \
  -H 'apikey: guest' \
  -H 'content-type: application/json' \
  -k -d '{
  "entitySchema": {
    "refCatalogueSchema": "generic_iotdevice_schema.json",
    "resourceType": "streetlight",
    "tags": ["onstreet", "Energy", "still under development!"],
    "refCatalogueSchemaRelease": "0.1.0",
    "latitude": {
      "value": 13.0143335,
      "ontologyRef": "http://www.w3.org/2003/01/geo/wgs84_pos#"
    },
    "longitude": {
      "value": 77.5678424,
      "ontologyRef": "http://www.w3.org/2003/01/geo/wgs84_pos#"
    },
    "owner": {
      "name": "IISC",
      "website": "http://www.iisc.ac.in"
    },
    "provider": {
      "name": "Robert Bosch Centre for Cyber Physical Systems, IISc",
      "website": "http://rbccps.org"
    },
    "geoLocation": {
      "address": "80 ft Road, Bangalore, 560012"
    },
    "data_schema": {
      "type": "object",
      "properties": {
        "dataSamplingInstant": {
          "type": "number",
          "description": "Sampling Time in EPOCH format",
          "units": "seconds",
          "permissions": "read",
          "accessModifier": "public"
        },
        "caseTemperature": {
          "type": "number",
          "description": "Temperature of the device casing",
          "units": "degreeCelsius",
          "permissions": "read",
          "accessModifier": "public"
        },
        "powerConsumption": {
          "type": "number",
          "description": "Power consumption of the device",
          "units": "watts",
          "permissions": "read",
          "accessModifier": "public"
        },
        "luxOutput": {
          "type": "number",
          "description": "lux output of LED measured at LED",
          "units": "lux",
          "permissions": "read",
          "accessModifier": "public"
        },
        "ambientLux": {
          "type": "number",
          "description": "lux value of ambient",
          "units": "lux",
          "permissions": "read",
          "accessModifier": "public"
        },
        "targetPowerState": {
          "type": "string",
          "enum": ["ON", "OFF"],
          "units": "dimensionless",
          "description": "If set to ON, turns ON the device. If OFF turns OFF the device. Writeable parameter. Writeable only allowed for authorized apps",
          "permissions": "read-write",
          "accessModifier": "protected"
        },
        "targetBrightnessLevel": {
          "type": "number",
          "description": "Number between 0 to 100 to indicate the percentage brightness level. Writeable only allowed for authorized apps",
          "units": "percent",
          "permissions": "read-write",
          "accessModifier": "protected"
        },
        "targetControlPolicy": {
          "enum": ["AUTO_TIMER", "AUTO_LUX", "MANUAL"],
          "units": "dimensionless",
          "permissions": "read-write",
          "description": "Indicates which of the behaviours the device should implement. AUTO_TIMER is timer based, AUTO_LUX uses ambient light and MANUAL is controlled by app. Writeable only allowed for authorized apps",
          "accessModifier": "protected"
        },
        "targetAutoTimerParams": {
          "type": "object",
          "permissions": "read-write",
          "properties": {
            "targetOnTime": {
              "type": "number",
              "description": "Indicates time of day in seconds from 12 midnight when device turns ON in AUTO_TIMER. Writeable only allowed for authorized apps",
              "units": "seconds",
              "accessModifier": "protected"
            },
            "targetOffTime": {
              "type": "number",
              "description": "Indicates time of day in seconds from 12 midnight when device turns OFF in AUTO_TIMER. Writeable only allowed for authorized apps",
              "units": "seconds",
              "accessModifier": "protected"
            }
          }
        },
        "targetAutoLuxParams": {
          "type": "object",
          "permissions": "read-write",
          "properties": {
            "targetOnLux": {
              "type": "number",
              "description": "Indicates ambient lux when device turns ON in AUTO_LUX. Writeable only allowed for authorized apps",
              "units": "lux",
              "accessModifier": "protected"
            },
            "targetOffLux": {
              "type": "number",
              "description": "Indicates ambient lux when device turns OFF in AUTO_LUX. Writeable only allowed for authorized apps",
              "units": "lux",
              "accessModifier": "protected"
            }
          }
        }
      },
      "additionalProperties": false
    },
    "serialization_from_device": {
      "format": "protocol-buffers",
      "schema_ref": {
        "type": "proto 2",
        "mainMessageName": "sensor_values",
        "link": "https://raw.githubusercontent.com/rbccps-iisc/applications-streetlight/master/proto_stm/txmsg/sensed.proto"
      }
    },
    "serialization_to_device": {
      "format": "protocol-buffers",
      "schema_ref": {
        "type": "proto 2",
        "mainMessageName": "targetConfigurations",
        "link": "https://raw.githubusercontent.com/rbccps-iisc/applications-streetlight/master/proto_stm/rxmsg/actuated.proto"
      }
    },
    "id": "streetlight"
  }
}'
```

## Success Response

**Code** : `200 OK`

**Content example**

```json
{
  "Registration": "success",
  "entityID": "streetlight",
  "apiKey": "219bf59341e24fe2901f52b0f8fbbff6",
  "subscriptionEndPoint": "https:\/\/smartcity.rbccps.org\/api\/{version}\/follow?id=dashboard",
  "accessEndPoint": "https:\/\/smartcity.rbccps.org\/api\/{version}\/db?id=dashboard",
  "publicationEndPoint": "https:\/\/smartcity.rbccps.org\/api\/{version}\/publish?id=dashboard",
  "resourceAPIInfo": "https:\/\/rbccps-iisc.github.io"
}
```

## Error Response

**Condition** : If 'apikey' is wrong.

**Code** : `403 FORBIDDEN`

**Content** :

```json
{
"message": "Invalid authentication credentials"
}
```
**Condition** : Precondition Failed

**Code** : `412 PRECONDITION FAILED`

**Content** :

```json
{
"Registration": "failure",
"Reason": "ID already used."
}
```
