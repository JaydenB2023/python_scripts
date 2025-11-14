# converts Google Sheet to csv automatically
import os
import requests
import sys

def getGoogleSheet(spreadsheet_id, outDir, outFile):
  
  url = f'[your_Google_Sheet_URL]'
  response = requests.get(url)
  if response.status_code == 200:
    filepath = os.path.join(outDir, outFile)
    with open(filepath, 'wb') as f:
      f.write(response.content)
      print('CSV file saved to: {}'.format(filepath))    
  else:
    print(f'Error downloading Google Sheet: {response.status_code}')
    sys.exit(1)


##############################################

outDir = '[your_ouput_directory]'

os.makedirs(outDir, exist_ok = True)
filepath = getGoogleSheet('[google sheet code found in url]', outDir, "[name of csv].csv")


sys.exit(0); ## success

