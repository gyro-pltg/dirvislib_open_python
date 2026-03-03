import struct

import matplotlib.pyplot as plt

import cartopy.crs as ccrs

from cartopy.io import shapereader
import cartopy.io.img_tiles as cimgt

import os

dataslist=dict()


def open_degree(latdegree,londegree):
	#print(__name__)
	if (f"N{latdegree}E{londegree}" in dataslist.keys()):
		###if (__name__=="__main__"): print("file was previously opened and converted already")
		pass
	else:
		if(f"N{latdegree}E{londegree}.hgt" in os.listdir("./SRTM_unpackedfull/")):
			with open(f"./SRTM_unpackedfull/N{latdegree}E{londegree}.hgt", 'rb') as elevatnfile:
				fileconts=elevatnfile.read()
			###if (__name__=="__main__"): print(len(fileconts))
			filecontstrue = struct.unpack(f">{('h' * ((len(fileconts)) // 2))}", fileconts)
			dataslist[f"N{latdegree}E{londegree}"]=filecontstrue
		else:
			dataslist[f"N{latdegree}E{londegree}"]=[0]*1201*1201


												#must reorder or even restructurize the coordinate arguments
def elevationfromcoordinate(displaymap, coordmode, basisN, basisE, *coo, **kwrgarr):
	open_degree(basisN,basisE)
	
	
	if(coordmode=="minsecond"):
		#can even make deeper functions
		latoffbase=1200-int(round((coo[0]*60+coo[1])/3,0)) #also patch
		lonoffbase=int(round((coo[2]*60+coo[3])/3,0))

	elif(coordmode=="decimal"):
		latoffbase=1200-int(round(3600*(coo[0]%1)/3,1))
		lonoffbase=int(round(3600*(coo[1]%1)/3,1))



	###if (__name__=="__main__"): print(f"{latoffbase} {lonoffbase}")
	##if (__name__=="__main__"): print(latoffbase*1201 + lonoffbase)
	#retvalue1 = filecontstrue[(int(((60-minAT)*60+(60-secAT))/3))*1201 + (int((minON*60+secON)/3))] - also try to make this option work just for fun
	#retvalue1 = filecontstrue[(1201-(int((minAT*60+secAT)//3)))*1201 + (int((minON*60+secON)//3))]
	retvalue1 = dataslist[f"N{basisN}E{basisE}"][latoffbase*1201 + lonoffbase]
	#why tf did (retvalue1 = filecontstrue[(minAT*60+int(secAT*3))*1201 + minON*60+int(secON*3)]) even work

	###if (__name__=="__main__"): print(f"elevation {retvalue1} m")




	if(displaymap):




		fig = plt.figure(figsize=(16, 9))
		ax1 = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
		ax1.set_global()
		ax1.stock_img()
		ax1.coastlines()

		latoffset=0
		lonoffset=0

		while(latoffset<1201):
			while(lonoffset<1201):
				#try:
				if (True):
					ht=dataslist[f"N{basisN}E{basisE}"][latoffset*1201 + lonoffset]
				#except Exception as e:
				#	print(e)
				#	print(latoffset*1201 + lonoffset)
				#if(ht==retvalue1):
				if(latoffset==latoffbase and lonoffset==lonoffbase):
					ax1.plot(basisE+(lonoffset/1201), (1+basisN)-(latoffset/1201), 'o', color="red",markersize=5, transform=ccrs.PlateCarree())
					pass
		
				lonoffset+=1
			lonoffset=0
			latoffset+=1

		#maybe try to make it work just for fun idk
		#ax1.plot(131+(((minAT*60+int(secAT/3))*1201 + minON*60+int(secON/3))%1201)/1201, 44-(((minAT*60+int(secAT/3))*1201 + minON*60+int(secON/3))//1201)/1201, 'o', color="red",markersize=5, transform=ccrs.PlateCarree())

		if(coordmode=="minsecond"): ax1.plot(basisE+coo[2]/60+coo[3]/3600,basisN+coo[0]/60+coo[1]/3600, 'P', color="pink",markersize=3, transform=ccrs.PlateCarree())
		if (coordmode=="decimal"): ax1.plot(basisE+coo[1],basisN+coo[0], 'P', color="pink",markersize=3, transform=ccrs.PlateCarree())
		plt.show()
	
	return retvalue1



