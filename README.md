# Parrable EID Decryption Service

Parrable's EID Decryption service provides a REST API for decrypting Parrable EIDs.  It supports both Basic Auth and Certificate Based Authentication.  Credentials can be obtained by contacting info@parrable.com.

Basic auth or Certificate based authentication can be used manually with curl (or similar client), with the decryption script (such as the sample in this repo), or embedded directly into an application.

## Structure of an EID

EIDs are AES-256 encrypted.  Encryption keys are valid for 364 days.  EIDs older than 364 days cannot be decrypted and will return an error.

Example EID: `01.1642621683.970e2018ed2ede6bbc533638bed2911935bd0c9b8286015884c71ac6222d3c24d5f375f1dda53d753628cf591bdb360291258d83a04bc879bca7bef448e6765291ae97234050c46c542b`

An eid has 3 dot separated parts.

The first is the version of the EID (`01`)

The second is the timestamp (less ms) when the EID was created.  This is used to by Parrable to determine the Encryption key. (`1642621683`).

The third is the encrypted url safe base64 payload.

## Request and Response Formats

The path of the decryption request specifies the expected response format.  We recommend using the v2 response format as new features will not be added to the legacy and v1 formats. 

In the below examples `EID` is Parrable's Encrypted Identifier.

### Legacy Response

Example request: `GET https://d.parrable.com?id=EID`

```
{
   "browserid": "83af91be-0592-4bd3-a1d2-fafa8d46466f",
   "deviceid": "0d82c21e-3a9a-4b4b-adc2-342e503a12c6",
}
```

### v1 Response (v1 EID)

Example Request `GET https://d.parrable.com/decrypt/v1?eid=EID`

Where `EID` is Parrable's encrypted ID string.

Response:
```
{
   "browserId": "83af91be-0592-4bd3-a1d2-fafa8d46466f",
   "browserIdDate": 1598046744750,
   "deviceId": "0d82c21e-3a9a-4b4b-adc2-342e503a12c6",
   "deviceIdDate": 1598046744750
}
```

### v2 Response (v1 EID, v2 EID support coming soon)

Example Request `GET https://d.parrable.com/decrypt/v2?eid=EID`

Response:
```
{
    "primaryId":{
        "deviceId":"83af91be-0592-4bd3-a1d2-fafa8d46466f",
        "deviceIdDate":1598046744750,
        "browserId":"0d82c21e-3a9a-4b4b-adc2-342e503a12c6",
        "browserIdDate":1598046744750
    }
}
```

## Manual decryption using curl

```bash
curl --user username:password 'https://d.parrable.com/decrypt/v1?eid=PARRABLE_EID'
```

```bash
curl --key cert/KEYNAME.key --cert cert/CERTNAME.cert 'https://d.parrable.com/decrypt/v1?eid=PARRABLE_EID'
```

## Using a python3 script to decrypt a log file

A sample python3 script is available in this repository to demonstrate certificate based authentication.

1. Download a copy of the decryption script as `decrypt.py`
2. Replace YOUR_CERT_NAME with CERTNAME - matching the file in the `cert/` directory.
3. Replace YOUR_KEY_NAME with KEYNAME - matching the file in the `cert/` directory.

The script requires python3 and the `requests` package as a dependency.

Sending your web access logs through the decryption script will result in decryption of any EID found in the log.

The decrypted EID will result in a DID (device ID) and a BID (browser ID) appended to the line that the EID was found on.

 `demo.log` contains an example log file.  Note that the EID in the demo.log may be older than 364 days and cannot be decrypted.  A new EID can be obtained from the opt-out page of the Parrable Website at [https://www.parrable.com/opt-out/](https://www.parrable.com/opt-out/)

The following command will produce an appended demo.log file:

```bash
cat demo.log | ./decrypt.py | tee demo-decrypted.log
```




