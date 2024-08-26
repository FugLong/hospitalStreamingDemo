# hospitalStreamingDemo
A project designed to generate multiple emulated data sources from an imaginary hospital. Currently includes a tradtitional EHR db running in postgresql that is updated over time through faked traditional data entry updates and new age FHIR API calls. All faked API calls are logged in a separate postgres db. In addition, there are multiple faked streams of data coming from a kafka container that represent multiple types of data and devices. There are real time streams of data from modern hospital monitoring devices as well as medium speed events like new age patient tracking and status mobile apps. 

## Requirements
Docker

## Usage
Clone the repo, then enter the repo's folder: 
```
cd hospitalStreamingDemo
```
Change postgres password in .env if you want

Then run: 
```
docker-compose up --build 
```
OR, to run in background:
```
docker-compose --build -d 
```
If you ran in the foreground wait for 20 seconds or so and you should see the output of multiple various types of faked data being generated and modified from various realistic sources after the inital bootup and delay.

If you ran in the background you'll have to use docker desktop or terminal to connect to the hospitalSteamingDemo-data_faker-1 container
