import os.path
import requests

from EventorServer import settings
home_storage_prefix="https://storage.backtory.com/eventsphotos"

def getAccessToken(**kwargs):
    url= settings.BACKTORY_API_SERVICE_PREFIX+"/auth/login"
    headers={
        'X-Backtory-Authentication-Id':settings.X_BACKTORY_AUTHENTICATION_ID,
        'X-Backtory-Authentication-Key':settings.X_BACKTORY_AUTHENTICATION_KEY,
        'X-Backtory-Authentication-Refresh':'1',
    }
    data={
        'refresh_token':settings.BACKTORY_REFRESH_TOKEN
    }
    kwargs['headers']=headers
    kwargs['data']=data
    response=requests.api.request(method='post',url=url,headers=headers,data=data)
    dic=eval(response.text)
    access_token=dic['access_token']
    return access_token


def upload_file(file,**kwargs):
    access_token=getAccessToken()
    url=settings.BACKTORY_STORAGE_SERVICE_PREFIX+'/files'
    headers = {
        'X-Backtory-Storage-Id': settings.BACKTORY_STORAGE_ID,
        'X-Backtory-Authentication-Key':settings.X_BACKTORY_AUTHENTICATION_KEY,
        'Authorization' : 'bearer '+access_token
    }
    data={
        'fileItems[0].path':'/',
        'fileItems[0].replacing':'true'
    }
    files={
        'fileItems[0].fileToUpload': file,
    }
    kwargs['headers'] = headers
    kwargs['data'] = data
    kwargs['files']=files
    response = requests.api.request(method='post', url=url, headers=headers, data=data,files=files)
    dic=eval(response.text)
    saved_file_url=dic['savedFilesUrls'][0]

    return (home_storage_prefix+saved_file_url)
