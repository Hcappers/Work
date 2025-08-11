# Search VirusTotal from a file
# Original  powershell script by Chris Shearer <23-June-2022>
# Original Python script by Haskell Cappers <25-October-2023>
# Submit a file hash to VirusTotal using a .csv file for input
# Input file format <filename>,<filehash>,<host>
# python get-VTFR.py <filename>

import requests, sys, os, csv

# Make sure that the user has entered a file in the command line
if len(sys.argv) < 2:
    print('Usage: get-VTFP-file.py <filename>')
    sys.exit()

# Check to see if .csv file exists and return the file name and path.
def fileCheck():
    vtFile = sys.argv[1]
    if not os.path.exists(vtFile):
        print(f"File {vtFile} does not exist.")
        sys.exit()
    else:
        print(f"File {vtFile} does exist and submitting to VT.")

    return vtFile

# function on finding out what API key to use for VT and setting the API key
def apiKey():
    vt_API_key = input("Choose which API key to use (1 or 2)")
    if vt_API_key == "1":
        vt_API_key = ''
    elif vt_API_key == "2":
        vt_API_key = ''
    else: 
        print("Invalid input. Please choose 1 or 2.")

        return vt_API_key

# Set Network protocol to TLS 1.2
#requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'DEFAULT:!DH'
#requests.packages.urllib3.util.ssl_.DEFAULT_SSL_CIPHER_LIST = 'TLS_AES_128_GCM_SHA256:TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384'

# Submit file to VT
def submit_VT_Hash(vtHash, vt_API_key):
    headers = {'apikey': vt_API_key, 'resource': vtHash}
    VT_Body = headers
    VT_Url = 'https://www.virustotal.com/api/v3/files/SHA-256'
    VT_Results = VT_Response = requests.post(VT_Url, data = VT_Body)
    return VT_Results

# Get content from .csv file and make a new file with VT results
def csvContent(vtFileName, vt_API_key, vtResult):
    try:
        with open(vtFileName, 'r', newline='') as vtFile:
            csvRead = csv.DictReader(vtFile, fieldnames=['Filename', 'Hash', 'Host'])

            with open('VT-Results.txt', 'a') as resultFile:
                for row in csvRead:
                    filename = row['Filename'].strip()
                    hashValue = row['Hash'].strip()
                    resultFile.write(f'Filename: {filename}, Hash: {hashValue}\n')

                    if not filename:
                        continue

                    resource = vtResult.get('resource', '')
                    scanDate = vtResult.get('scan_date', '')
                    positives = vtResult.get('positives', '')
                    total = vtResult.get('total', '')
                    permalink = vtResult.get('permalink', '')

                    resultFile.write("============================\n")
                    resultFile.write(f"File Name   :{filename}\n")
                    resultFile.write(f"Resource    :{resource}\n")
                    resultFile.write(f"Hosts       :{row['Host']}\n")
                    resultFile.write(f"Scan Date   :{scanDate}\n")
                    resultFile.write(f"Positives   :{positives}\n")
                    resultFile.write(f"Total Scans :{total}\n")
                    resultFile.write(f"Permalink   :{permalink}\n")
                    
    except FileNotFoundError as e:
        print(f"File {vtFileName} not found. Please check the file name and path.")
        raise SystemExit
    except PermissionError as e:
        print(f"File {vtFileName} cannot be opened. Please check the file name and path.")
        raise SystemExit
    except Exception as e:
        print(f"Error: {e}")
        raise SystemExit
    

if __name__ == '__main__':
    vtFileName = fileCheck()
    vt_API_key = apiKey()
    vtResult = submit_VT_Hash(vtFileName,vt_API_key)
    if vtResult is not None:
        csvContent(vtFileName, vt_API_key, vtResult)



        """
            NOTES:
            - Error handling for seeing if there are two command line arguments -> works
            - Error handling for seeing if the file exists -> works
            - Submitting the API key to VT -> does not work, response error code 403
                - is the api key correct? -> yes
                - is the api key being submitted correctly? -> ?, I think the api key needs to be submitted via the header in the request
                - is the api key being submitted to the correct url? -> yes 
            - Submitting the file to VT -> untested
            - Getting results from VT and writing them to a file -> untested

            From the VirusTotal API documentation:
                import requests
                url = "https://www.virustotal.com/api/v3/files/SHA-256"
                headers = {
                            "accept": "application/json", -> indicates that the client expects JSON as the response format.
                            "x-apikey": "5b715b064eba13d46f244491f27f1538dd654c9c228e3407eecc99c402174b3b"
                        }
                response = requests.get(url, headers=headers)
                print(response.text)

            - Changes 11/20/2023
                - Add the headers to the request on line 43, hope to fix the error code 403. 
                - 
        """
