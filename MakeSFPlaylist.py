import httplib2
import os
import sys
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow
import dateutil.parser as dp
import time
clientsec="client_secret.json"
message="Woops"
scope="https://www.googleapis.com/auth/youtube"
name="youtube"
version="v3"
flow=flow_from_clientsecrets(clientsec,message=message,scope=scope)
storage = Storage("%s-oauth2.json" % sys.argv[0])
credentials = storage.get()
if credentials is None or credentials.invalid:
  flags = argparser.parse_args()
  credentials = run_flow(flow, storage, flags)
yt=build(name,version, http=credentials.authorize(httplib2.Http()))
playlistId=["PLP9mHssWIjdcNK8h5ceRHKH1HOlKo8b_A","PLP9mHssWIjdc1grxTjrIrRuVs8VPBo0SH","PLP9mHssWIjdfRls5k7u7Qxwatz9g6g_Xm"]
vids=[]
SFResponse=yt.channels().list(part="contentDetails",id="UC_gE-kg7JvuwCNlbZ1-shlA").execute()
nukeResponse=yt.channels().list(part="contentDetails",id="UCLMLTE5R-LR26VKfnaDQtEA").execute()
PBLResponse=yt.channels().list(part="contentDetails",id="UCAdt0pw24jpW4nK9Ajc1nWg").execute()
SFNerdResponse=yt.channels().list(part="contentDetails",id="UCuCLhzmx0AGnsViXF0Q44tg").execute()
SPFResponse=yt.channels().list(part="contentDetails",id="UCxsbRjOUPXeFGj7NSCOl8Cw").execute()
philResponse=yt.channels().list(part="contentDetails",id="UCcV40gnTH9-T8yw3FHjzWZQ").execute()
uploads=[
    SFResponse["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"],
    nukeResponse["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"],
    PBLResponse["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"],
    SFNerdResponse["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"],
    SPFResponse["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"],
    philResponse["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
]
print("Getting all the videos...")
for pl in uploads:
    channelVidsRequest=yt.playlistItems().list(playlistId=pl,part="snippet",maxResults=50)
    while channelVidsRequest:
        channelVids=channelVidsRequest.execute()
        vids=vids+channelVids["items"]
        channelVidsRequest=yt.playlistItems().list_next(channelVidsRequest,channelVids)
print("Done")
print("Sorting the videos by timestamp...")
vids.sort(key=lambda d: int(time.mktime(dp.parse(d["snippet"]["publishedAt"]).timetuple())))
print("Done")
i=0
for v in vids:
  try:
    yt.playlistItems().insert(part="snippet",
                              body={
                                "snippet":{
                                  "playlistId":playlistId[i],
                                  "resourceId":v["snippet"]["resourceId"]
                                }
                              }
                            ).execute()
  except Exception as e:
    if "Playlist contains maximum number of items." in str(e):
      i+=1
      yt.playlistItems().insert(part="snippet",
                                body={
                                  "snippet":{
                                    "playlistId":playlistId[i],
                                    "resourceId":v["snippet"]["resourceId"]
                                  }
                                }
                              ).execute()
    else:
      print("Something went wrong")
      print(str(e))
      break
  finally:
    print("Added "+str(vids.index(v)+1)+"/"+str(len(vids))+": "+v["snippet"]["title"])
