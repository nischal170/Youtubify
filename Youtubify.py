import requests
from credentials import *
import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

class Youtubify:
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



    def show_playlists(self,arg):
        print("Here are your spotify playlists,Press Keys to add desired playlist to create Youtube Playlist\n")
        for i in range (0,len(arg)):
            print("{}".format(i),arg[i])

        self.ask_choice(arg)
        return()

    def ask_choice(self,arg):
        ch=int(input("\n enter playlist Number "))
        self.playlist_name=self.arg[ch]

        print("creating a playlist in youtube  named '{}' ".format(arg[ch]))
        self.get_playlist_tracks(ch,arg)
        return(ch,self.playlist_name)


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
        artists = []
        song_name = []
        print("Getting tracks of the playlist '{}' ".format(arg[choice]))
        for i in range(0, len(play)):
            artists.append(play[i]['track']['album']['artists'][0]['name'])
            song_name.append(play[i]['track']['name'])

            print(artists[i], " ", song_name[i])


        return(song_name,artists)

    def youtube_client(self):
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
            body={
                "snippet": {
                    "title": "{}".format(self.playlist_name),
                    "description": "This is a Playlist created direct from Spotify playlist",
                    "tags": [

                    ],
                    "defaultLanguage": "en"
                },
                "status": {
                    "privacyStatus": "private"
                }

            }
        )
        response = request.execute()

        print(response)








if __name__ == '__main__':

    cp = Youtubify()

    cp.get_spotify_playlist()