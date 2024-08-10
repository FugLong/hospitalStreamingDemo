# hospitalStreamingDemo
A project designed to process, analyze, and visualize multiple realistic, emulated data sources from an imaginary hospital. 

(Currently just has fake data sources)

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
