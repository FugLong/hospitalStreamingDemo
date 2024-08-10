# hospitalStreamingDemo
A project designed to emulate, analyze, and combine multiple realistic data sources from an imaginary hospital.

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
If you ran in the foreground you should see the output and multiple various types of faked data being generated and modified from various realistic sources after the inital bootup and delay.

If you ran in the background you'll have to use docker desktop or terminal to connect to the hospitalSteamingDemo-data_faker-1 container
