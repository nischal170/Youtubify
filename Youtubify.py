import requests
from credentials import *#Importing everything from crediantials file
import os
import json

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

class Youtubify:
    def __init__(self):
        pass


    #first get the playlist of the user from spotify

    def get_spotify_playlist(self):
       url='https://api.spotify.com/v1/users/{}/playlists'.format(user_id)
       response=requests.get(url,

                headers={

                "Content-Type": "application/json",

                "Authorization": "Bearer {}".format(spotify_token)

            })
       playlist=response.json()
       play = playlist['items']
       lis = []#creating empty list for storing names of playlist
       self.ids=[]#creating empty list for storind playlist id
       for i in range(0, len(play)):
           lis.append(play[i]['name'])
           self.ids.append(play[i]['id'])

       self.show_playlists(lis)



       return(lis,self.ids)

#showing the playlists of the user


    def show_playlists(self,arg):
        print("Here are your spotify playlists,Press Keys to add desired playlist to create Youtube Playlist\n")
        for i in range (0,len(arg)):
            print("{}".format(i),arg[i])

        self.ask_choice(arg)
        return()

#select the playlist from the list

    def ask_choice(self,arg):
        ch=int(input("\n enter playlist Number "))
        self.playlist_name=arg[ch]

        print("creating a playlist in youtube  named '{}' ".format(arg[ch]))
        self.get_playlist_tracks(ch,arg)
        return(ch,self.playlist_name)

#getting all the tracks from the selected playlist

    def get_playlist_tracks(self,choice,arg):

        playlist_id=self.ids[choice]

        url = "https://api.spotify.com/v1/playlists/{}/tracks?market=ES&fields=items(track(name%2Calbum(artists.name)))".format(
            playlist_id)
        response = requests.get(url,

                                headers={

                                    "Content-Type": "application/json",

                                    "Authorization": "Bearer {}".format(spotify_token)

                                })
        playlist = response.json()
        play = playlist['items']
        self.no_of_tracks=len(play)
        artists = []
        song_name = []
        trackname=[]
        print("Getting tracks of the playlist '{}' ".format(arg[choice]))
        for i in range(0, len(play)):
            artists.append(play[i]['track']['album']['artists'][0]['name'])
            song_name.append(play[i]['track']['name'])

            print(artists[i], " ", song_name[i])
        self.trackname=[' '.join(x) for x in zip(artists,song_name)]#merging artists and song_name lists  into a single list
        self.youtube_client()





        return(self.trackname,self.no_of_tracks)

    #setting up youtube client and creating empty  playlist in youtube

    def youtube_client(self):
        scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]
        # Disable OAuthlib's HTTPS verification when running locally.
        # *DO NOT* leave this option enabled in production.
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        api_service_name = "youtube"
        api_version = "v3"
        client_secrets_file = "CLIENT_SECRET_FILE.json"

        # Get credentials and create an API client
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            client_secrets_file, scopes)
        credentials = flow.run_console()
        youtube = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials)

        request = youtube.playlists().insert(
            part="snippet",
            body={
                "snippet": {
                    "title": "{}".format(self.playlist_name),
                    "description": "automatically created by python"
                }
            }
        )
        response=request.execute()
        self.get_tracks_id(youtube)

        return()

    #searching the obtained tracks in youtube and keepind the tracks id in list
    def get_tracks_id(self,youtube):
        list_id=[]
        for i in range(0,self.no_of_tracks):
            request = youtube.search().list(
                part="snippet",
                maxResults=1,
                q="{}".format(self.trackname[i])
                )
            response = request.execute()
            play=response['items']
            list_id.append(play[0]['id']['videoId'])
            self.listid=list_id

        self.get_playlist_id(youtube)


        return(self.listid)

    #getting the id of playlist which we have created  earlier

    def get_playlist_id(self,youtube):
        request = youtube.playlists().list(
            part="id,snippet",
            mine=True
        )
        response = request.execute()
        play=response['items']
        titlelist = []
        ids = []
        it=len(play)
        for i in range(0, it):
            titlelist.append(play[i]['snippet']['title'])
            ids.append(play[i]['id'])


        for i in range(0, it):
            if self.playlist_name == play[i]['snippet']['title']:
                d = i
                break
        print(d)
        ytplaylist_id=ids[d]
        self.add_tracks_to_yt_playlist(ytplaylist_id)

        return(ytplaylist_id,youtube)

    #adding the tracks to the playlist with their track id

    def add_tracks_to_yt_playlist(self,ytplaylist_id,youtube):
        for i in range(0,self.no_of_tracks):
            request = youtube.playlistItems().insert(
                part="snippet",
                body={
                    "snippet": {
                        "playlistId": "{}".format(ytplaylist_id),
                        "position": i,
                        "resourceId": {
                            "kind": "youtube#video",
                            "videoId": "{}".format(self.listid)
                        }
                    }
                }
            )
        response = request.execute()
        return(response)




if __name__ == '__main__':

    cp = Youtubify()

    cp.get_spotify_playlist()