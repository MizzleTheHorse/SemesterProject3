# Template

1. Introduction

This project is a part of a larger audio streaming application, intended to scale to millions of users within the first two years. This team is responsible for downloading and storing audio files from YouTube and artists' own original work. 

As this service is part of a bigger application an API is supplied for interaction with the system. The API will make it possible to add and delete content from the system and make it possible for other microservices to acquire audio files and metadata from the system. This team supplies user interfaces for adding content

A typical implementation for acquiring audio would be to download the audio file and save it locally, and then store it in the preferred way. For example a YouTube downloader/converter, which there are several web-site examples of. An example of an implementation for adding local audio is the way you add original work in iTunes. In this project, a persistence layer will be added which makes it possible to store audio files and make them accessible for the rest of the streaming application.


