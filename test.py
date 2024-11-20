from fastapi import FastAPI
from mavsdk import System
import os
import asyncio
import os
# no final, quando for devolver o erro, trocar para: "raise HTTPException(status_code="" , detail="")"

from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware


#--------------------------------------------------------------------------------
app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
#--------------------------------------------------------------------------------


#--------------------------------------------------------------------------------
# Setting up drone library
drone = System()
#--------------------------------------------------------------------------------


#connect_ip = "192.168.144.12"
#await drone.connect(system_address=f"udp://:{connect_ip}:{connect_udp}")
#await drone.connect(system_address=f"udp://19856")
# await drone.connect(system_address=f"udp://192.168.144.12:19856")
@app.get("/drone/{connect_udp}")
async def	connecting_w_udp(connect_udp : int):

	await drone.connect(system_address="udp://:{connect_udp}")

	for state in drone.core.connection_state():
		if state.is_connected:
			return({"message" : "Drone connected"})
		else:
			return({"message" : "Not connected"})


@app.get("/getting_info")
async def	getting_info():
	try:
		if drone.core.connection_state:
			async for position in drone.telemetry.position():
				break
			drone_latitude = position.latitude_deg
			drone_longitude = position.longitude_deg
			drone_absolute_altitude = position.absolute_altitude_m
			return (f"drone is on: {drone_latitude} {drone_longitude} {drone_absolute_altitude}")
	except:
		return ({"ERROR" : "Drone not connected, cannot execute the function"})


@app.get("/arm_test")
async def	arm_test():
	try:
		if drone.core.connection_state:
			await drone.action.arm()
			return ({"SUCCESS" : "Drone is armed"})
	except:
		return ({"ERROR" : "Drone no connected, cannot execute the function"})


@app.get("/take_off/{altitude}")
async def	take_off(altitude : float):
	try:
		if drone.core.connection_state:
			await drone.action.set_takeoff_altitude(altitude)
			await drone.action.arm()
			await drone.action.takeoff()
			return ({"SUCCESS" : "Drone is Taking off"})
	except:
		return ({"ERROR" : "Drone not connected, cannot execute the function"})


@app.get("/fly")
async def	fly():
	try:
		if drone.core.connection_state:
			async for position in drone.telemetry.position():
				break
			drone_latitude = position.latitude_deg
			drone_longitude = position.longitude_deg
			drone_absolute_altitude = position.absolute_altitude_m
			drone_relative_altitude = position.relative_altitude_m
			if drone_relative_altitude > 5:
				await drone.action.goto_location(-35.362633,149.163448,605, 0.0)
				return ({"SUCCESS" : "Drone is going to_location B"})
			return ({"ERROR" : "Drone not in air, cannot fly"})
	except:
		return ({"ERROR" : "Drone no connected, cannot execute the function"})


@app.get("/returnHome")
async def	returnHome():
	try:
		if drone.core.connection_state():
			await drone.action.return_to_launch()
			return ({"SUCCESS" : "Drone is going back to launch position"})
	except:
		return ({"ERROR" : "Drone no connected, cannot execute the function"})

@app.get("/land")
async def	drone_land():
	try:
		if drone.core.connection_state:
			async for position in drone.telemetry.position():
				break
			if	position.relative_altitude_m > 1:
				await drone.action.land()
		return ({"SUCCESS" : "Drone is landing"})
	except:
		return ({"ERROR" : "Drone not connected, cannot execute the function"})

@app.get("/")
def	print_hello():
	return ('{"message": "Hello Visuinnovation"}')

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)


