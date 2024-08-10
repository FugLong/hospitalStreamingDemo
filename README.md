# hospitalStreamingDemo
A project designed to emulate, analyze, and combine multiple realistic data sources from an imaginary hospital.

## Requirements
Docker

## Usage
Clone the repo, enter the repo's folder: 
```
cd hospitalStreamingDemo
```
Then run: 
```
docker-compose up --build 
```
OR, to run in background:
```
docker-compose --build -d 
```
If you ran in the foreground you should see the output and multiple various types of faked data being generated and modified from various realistic sources after the inital bootup and delay.

If you ran in the background you'll have to use docker desktop or connect to the hospitalSteamingDemo-hospitalStreamingDemo-1 container
