import requests
import unittest
import json

from requests.api import head, request

API_URL = "http://t09-django-service:8000" #Change 't09-django-service' with localhost if tested local


class test_get_empty(unittest.TestCase):

    #test to see if get all tracks is empty
    def test_get_all_tracks(self):
        endpoint = "/get_all_tracks/"
        url = API_URL + endpoint

        r = requests.get(url)
        self.assertEqual(200, r.status_code)
        self.assertIn('{}', r.content.decode("utf-8"))
    
    #test response for getting a yt url not in database
    def test_get_invalid_yt_url(self):
        endpoint = "/get_track/"
        id = "dksfgjka113"
        url = API_URL + endpoint + id

        r = requests.get(url)
        self.assertEqual(404, r.status_code)
        self.assertIn('There was an error retrieving the track URL', r.content.decode("utf-8"))

    #test response for calling an invalid API url
    def test_get_invalid_api_url(self):
        endpoint = "/invalid_endpoint/"
        url = API_URL + endpoint

        r = requests.get(url)
        self.assertEqual(404, r.status_code)

class test_post_empty(unittest.TestCase):

    #test for uploading custom without an mp3 file
    def test_post_invalid_custom_song_mp3file_missing(self):

        endpoint = "/add_custom/"
        url = API_URL + endpoint

        mp3file = "nothing"
        
        artfile = open('test_api/the_gray_chapter_album.jpeg', 'rb').read()
        
        #create the data to be uploaded
        metadataJson = '{"name":"invalid_test","artist":"Invalid_artist","release_year":"2014","part of collection":"true","collection_name":".5 The Gray chapter","track_nr":"2","total_track_count":"12"}'
        metadataJson = dict(metadata=metadataJson)
        data = dict(artwork=artfile, mp3file=mp3file)

        r = requests.post(url, files=data,data=metadataJson) #data or json

        self.assertEqual(200, r.status_code, "Invalid Custom Song Test")
        self.assertNotIn('Successfully uploaded mp3file!', r.content.decode("utf-8"))

    #test for uploading custom song without artwork
    def test_post_invalid_custom_song_art_missing(self):
        endpoint = "/add_custom/"
        url = API_URL + endpoint

        mp3file = open('test_api/Sarcastrophe.mp3', 'rb').read() # rb = read + binary mode
        
        artfile = "nothing"
        
        #create the data to be uploaded
        metadataJson = '{"name":"invalid_test","artist":"Invalid_artist","release_year":"2014","part of collection":"true","collection_name":".5 The Gray chapter","track_nr":"2","total_track_count":"12"}'
        metadataJson = dict(metadata=metadataJson)
        data = dict(artwork=artfile, mp3file=mp3file)

        r = requests.post(url, files=data,data=metadataJson) #data or json

        song_id = r.content.decode("utf-8")[-35:]

        self.assertEqual(200, r.status_code, "Invalid Custom Song Test")
        self.assertIn('Successfully uploaded mp3file!', r.content.decode("utf-8"))
        #delete the uploaded track
        r = requests.get(API_URL + "/delete_track/" + song_id)        

    #test for uploading custom song, without metadata
    def test_post_invalid_custom_song_metadata_missing(self):
        endpoint = "/add_custom/"
        url = API_URL + endpoint
        mp3file = open('test_api/Sarcastrophe.mp3', 'rb').read() # rb = read + binary mode
        
        artfile = open('test_api/the_gray_chapter_album.jpeg', 'rb').read()
        
        #create the data to be uploaded
        metadataJson = 'nothing'
        metadataJson = dict(metadata=metadataJson)
        data = dict(artwork=artfile, mp3file=mp3file)

        r = requests.post(url, files=data,data=metadataJson) #data or json

        

        self.assertEqual(200, r.status_code, "Invalid Custom Song Test")
        self.assertNotIn('Successfully uploaded mp3file!', r.content.decode("utf-8"))

    #test for only uploading an mp3
    def test_post_invalid_custom_song_only_mp3(self):
        endpoint = "/add_custom/"
        url = API_URL + endpoint
        mp3file = open('test_api/Sarcastrophe.mp3', 'rb').read() # rb = read + binary mode
        
        artfile = "nothing"
        
        #create the data to be uploaded
        metadataJson = 'nothing'
        metadataJson = dict(metadata=metadataJson)
        data = dict(artwork=artfile, mp3file=mp3file)

        r = requests.post(url, files=data,data=metadataJson) #data or json

        self.assertEqual(200, r.status_code, "Invalid Custom Song Test")
        self.assertNotIn('Successfully uploaded mp3file!', r.content.decode("utf-8"))


class test_post(unittest.TestCase):


    #tests to see if the CA tracks are empty before start
    def test_21get_empty(self):
        endpoint = "/get_all_tracks/"
        url = API_URL + endpoint

        r = requests.get(url)
        self.assertEqual(200, r.status_code)
        self.assertNotIn('CA_', r.content.decode("utf-8"))

    # Uploads custom song, and checks it has gotten a success message.
    def test_22upload_custom(self):
        import global_var_module

        endpoint = "/add_custom/"
        url = API_URL + endpoint
        mp3file = open('test_api/Sarcastrophe.mp3', 'rb').read() # rb = read + binary mode
        
        artfile = open('test_api/the_gray_chapter_album.jpeg', 'rb').read()
        
        #create the data to be uploaded
        metadataJson = '{"name":"Sarcastrophe","artist":"Slipknot","release_year":"2014","part of collection":"true","collection_name":".5 The Gray chapter","track_nr":"2","total_track_count":"12"}'
        metadataJson = dict(metadata=metadataJson)
        data = dict(artwork=artfile, mp3file=mp3file)

        r = requests.post(url, files=data,data=metadataJson) #data or json

        global_var_module.song_id = r.content.decode("utf-8")[-35:]

        self.assertEqual(200, r.status_code)
        self.assertIn('Successfully uploaded mp3file!', r.content.decode("utf-8") )

    #tests to get all tracks, and see that a new one is present
    def test_23get_all_tracks(self):
        endpoint = "/get_all_tracks/"
        url = API_URL + endpoint

        r = requests.get(url)
        self.assertEqual(200, r.status_code)
        self.assertIn('{\"track 0\":', r.content.decode("utf-8"))


    
    #Tests if one custom uploaded track can be taken from the FTB
    def test_24get_uploaded_track(self):
        import global_var_module
        #first gets all tracks from the SQL db, then takes the ID of the first track

        endpoint = "/get_track/"+global_var_module.song_id
        url = API_URL + endpoint

        r = requests.get(url)

        self.assertEqual(200, r.status_code)
        self.assertIn(global_var_module.song_id + ".mp3", r.content.decode("utf-8"))
    
    #tests to delete the custom uploaded song
    def test_25delete_custom(self):
        import global_var_module

        endpoint = "/delete_track/"
        url = API_URL + endpoint + global_var_module.song_id
        r = requests.get(url)
        self.assertEqual(200,r.status_code)
        self.assertIn("File has been deleted", r.content.decode("utf-8"))
        #tests to see if all tracks now is empty
        test_get_empty().test_get_all_tracks()

    #Tests if the custom uploaded track is actually gone
    def test_26get_uploaded_track_is_deleted(self):
        import global_var_module
    
        endpoint = "/get_track/"+global_var_module.song_id
        url = API_URL + endpoint

        r = requests.get(url)

        self.assertEqual(404, r.status_code)
        self.assertNotIn(global_var_module.song_id, r.content.decode("utf-8"))

    #makes sure the track gets deleted
    @classmethod
    def tearDownClass(self):
        import global_var_module

        requests.get(API_URL + "/delete_track/" + global_var_module.song_id)


class test_youtube(unittest.TestCase):

    #the ID used for all youtube test cases
    youtube_ID = "yjNcXPtNQdE"

    @classmethod
    def setUpClass(self):
        #makes sure the used yt track is deleted before beginning
        requests.get(API_URL + "/delete_track/" + "YT_" + self.youtube_ID)

    def test_11no_youtube(self):
        endpoint = "/get_all_tracks/"
        url = API_URL + endpoint

        r = requests.get(url)
        
        self.assertEqual(200, r.status_code)
        self.assertNotIn("YT_", r.content.decode("utf-8"))

    #add a song from youtube, through api
    def test_12add_youtube(self):
        endpoint = "/add_youtube/"
        url = API_URL + endpoint + self.youtube_ID

        r = requests.get(url)
 
        self.assertEqual(200, r.status_code)
        self.assertIn("New song added to System", r.content.decode("utf-8"))

    #check is correct error is displayed, and there are not 2 tracks present for same id
    def test_13add_duplicate_youtube(self):
        endpoint = "/add_youtube/"
        url = API_URL + endpoint + self.youtube_ID

        r = requests.get(url)
 
        self.assertEqual(404, r.status_code)
        self.assertIn("Song already in database", r.content.decode("utf-8"))
        
        #checks to see if duplicate tracks are found in get all tracks
        endpoint = "/get_all_tracks/"
        url = API_URL + endpoint

        r = requests.get(url)
        #Makes sure that only one track is present
        self.assertEqual(200, r.status_code)
        self.assertIn('{"track 0": "YT_yjNcXPtNQdE"}',r.content.decode("utf-8"))
        self.assertNotIn('{"track 1": "YT_yjNcXPtNQdE"}', r.content.decode("utf-8"))

    #test response from giving an invalid url
    def test_14wrong_yt_url(self):
        endpoint = "/add_youtube/"
        ## youtube id is random, to get an invalid yt id
        youtube_ID = "hs39jsvms"
        url = API_URL + endpoint + youtube_ID

        r = requests.get(url)
        self.assertEqual(404, r.status_code)
        self.assertIn("URL not valid", r.content.decode("utf-8"))


    #get the URL to the uploaded track
    def test_15get_youtube(self):
        endpoint = "/get_track/"
       
        url = API_URL + endpoint + "YT_" + self.youtube_ID

        r = requests.get(url)
        self.assertEqual(200, r.status_code)
        self.assertIn("YT_" + self.youtube_ID + ".mp3", r.content.decode("utf-8"))

    #delete the uploaded youtube track
    def test_16delete_youtube(self):
        endpoint = "/delete_track/"

        url = API_URL + endpoint + "YT_" +self.youtube_ID

        r = requests.get(url)
        self.assertEqual(200, r.status_code)
        self.assertIn("File has been deleted", r.content.decode("utf-8"))

        test_get_empty().test_get_all_tracks()

    #Tests if the yt uploaded track is removed
    def get_17uploaded_track_is_deleted(self):
    
        endpoint = "/get_track/" + "YT_" +self.youtube_ID
        url = API_URL + endpoint

        r = requests.get(url)

        self.assertEqual(404, r.status_code)
        self.assertNotIn("YT_" + self.youtube_ID, r.content.decode("utf-8"))

    @classmethod
    def tearDownClass(self):

        requests.get(API_URL + "/delete_track/" + "YT_yjNcXPtNQdE")


unittest.main()