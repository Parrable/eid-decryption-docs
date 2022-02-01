#!/usr/bin/env python3
import requests
import sys, os
import re
from string import Template

PARRABLE_DECRYPTION_ENDPOINT = 'https://d.parrable.com/decrypt/v1'

script_base = os.path.dirname(os.path.abspath(__file__))

client_cert_path = os.path.join(script_base, 'cert', 'CERTNAME.cert')
client_key_path = os.path.join(script_base, 'cert', 'KEYNAME.key')

def decrypt(eid):
  response = requests.get(
    PARRABLE_DECRYPTION_ENDPOINT,
    params={ 'eid': eid },
    cert=(client_cert_path, client_key_path)
  )
  response.raise_for_status()

  # Returns object
  # {
  #   'deviceId': 'UUID',
  #   'deviceIdDate': 13-digit epoch,
  #   'browserId': 'UUID',
  #   'browserIdDate': 13-digit epoch,
  # }
  return response.json()

if __name__ == "__main__":
  eidRegex = re.compile(r'(?P<eid>\d{2}\.\d{10}\.\w{148})')
  
  while True:
    logLine = sys.stdin.readline().strip()
    if not logLine: break
  
    eidMatch = eidRegex.search(logLine)
  
    if eidMatch:
      decrypted = decrypt(eidMatch.group('eid'))
      decryptedIds = Template('did:$deviceId:$deviceIdDate|bid:$browserId:$browserIdDate').substitute(decrypted)
      sys.stdout.write(("{}|{}\n".format(logLine, decryptedIds)))
    else:
      sys.stdout.write("{}\n".format(logLine))