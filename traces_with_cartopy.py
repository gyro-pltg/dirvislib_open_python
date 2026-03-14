import struct

import matplotlib.pyplot as plt




printingexcess = bool(0)

import os

import math
import time


dataslist=dict()

	




from get_elevation import dataslist, elevationfromcoordinate



#use an actual formula for angular distance instead
def cartesianfromgeo(declat, declon):
	phi = math.radians(declat)
	sig = math.radians(declon)
	return (math.cos(phi)*math.cos(sig), math.cos(phi)*math.sin(sig),math.sin(phi))




def midpointlinear(n,declat1,declon1,declat2,declon2):
	middlelat = declat1+n*(declat2-declat1)
	middlelon = declon1+n*(declon2-declon1)

	return (middlelat, middlelon)


def midpointcircle(f,in_azimuth,declat1,declon1,declat2,declon2):

	phi_1 = math.radians(declat1)
	sig_1 = math.radians(declon1)

	phi_2 = math.radians(declat2)
	sig_2 = math.radians(declon2)

	azi_r=math.radians(in_azimuth)


	a = math.sin((1-f)*azi_r)/ math.sin(azi_r)
	b = math.sin(f*azi_r) / math.sin(azi_r)
	x = a * math.cos( phi_1) * math.cos( sig_1) + b * math.cos( phi_2) * math.cos( sig_2)
	y = a * math.cos( phi_1) * math.sin( sig_1) + b * math.cos( phi_2) * math.sin( sig_2)
	z = a * math.sin(phi_1) + b * math.sin(phi_2)
	
	middlelat = math.degrees(math.atan2(z, math.sqrt(math.pow(x,2)+math.pow(y,2))))
	middlelon = math.degrees(math.atan2(y, x))



	return (middlelat, middlelon)







def sec_isosceles(n,k, alpha):
	beta = (180-alpha)/2
	return k*math.sin(math.radians(beta))/math.sin(math.radians(180-beta-n*alpha))


def sec_diffsides(n,alpha, k, j, g, cosbeta):

	if (g==0):
		g=gcalc(k,j, alpha)

	if(printingexcess): print(f"beta {math.degrees(math.acos(cosbeta))}")

	if(printingexcess): print(f"na {alpha*(n)}")

	m=k*math.sin(math.acos(cosbeta))/math.sin(math.radians(180)-math.radians(n*alpha)-math.acos(cosbeta))


	return m




def gcalc(k,j, alpha):
	return math.sqrt(math.pow(j,2)+math.pow(k,2)-2*j*k*math.cos(math.radians(alpha)))	




def calcazimuth(plotpoint, declat1, declon1, declat2, declon2):







	cart1 = cartesianfromgeo(declat1, declon1)
	cart2 = cartesianfromgeo(declat2, declon2)

	c = math.sqrt(math.pow(cart2[0]-cart1[0],2)+math.pow(cart2[1]-cart1[1],2)+math.pow(cart2[2]-cart1[2],2))
	


	out_degs = math.degrees(math.acos(1-math.pow(c,2)/2))
	#print(tracesteps)

	#rearrange!!
	if(plotpoint == True):
		#print(tracebetweentwo(out_degs, declat1, declon1, 2, declat2, declon2, 191))
		pass
		

	return out_degs



def tracebetweentwo(coords1, coords2, **kwargsdata):
	is_visible = True

	earth_r = 6367460


	if(not ("maxdist" in kwargsdata.keys())):
		kwargsdata["maxdist"] = 0

	defaultablevalues = {"trace_checks_per_one_degree":500,"maxdist":0}


	for dfkey in defaultablevalues.keys():
		if (not dfkey in kwargsdata.keys()):
			kwargsdata[dfkey] = defaultablevalues[dfkey] 


	azi = calcazimuth(True,coords1[0], coords1[1], coords2[0], coords2[1])

	tracestepcount = abs(math.ceil(azi*kwargsdata["trace_checks_per_one_degree"]))
	if(tracestepcount==0): tracestepcount = 1
	tracestepsingle = 1/tracestepcount

	lineheightinglist = []
	lineheightinglistradial = []

	centerdistancelist = []


	start_ele = elevationfromcoordinate(False,"decimal",int(coords1[0]//1),int(coords1[1]//1), coords1[0], coords1[1])
	final_ele = elevationfromcoordinate(False,"decimal",int(coords2[0]//1),int(coords2[1]//1), coords2[0], coords2[1])


	k_pre = earth_r+start_ele+coords1[2]
	j_pre = earth_r+final_ele+coords2[2]


	spacedist=gcalc(k_pre,j_pre,azi)
	
	if(printingexcess):print(math.sqrt(math.pow(j_pre,2)+math.pow(k_pre,2)-2*j_pre*k_pre*math.cos(math.radians(azi))))

	cosbeta_pre = (math.pow(spacedist,2)+math.pow(k_pre,2)-math.pow(j_pre,2))/(2*k_pre*spacedist)


	#comment to be deleted in some commits

	i = 0
	while (i<=1):
		#needed?
		if (kwargsdata["maxdist"]==0 or spacedist<=kwargsdata["maxdist"]):
			#print(spacedist)
				#printingexcess=False

			if(printingexcess): print(i)
			#middlelat = declat1+i*(declat2-declat1)
			#middlelon = declon1+i*(declon2-declon1)
			#middlelat, middlelon =midpoint(i, declat1,declon1,declat2,declon2)

			#middlelat, middlelon =midpointlinear(i,declat1,declon1,declat2,declon2)
			middlelat, middlelon = midpointcircle(i,azi,coords1[0],coords1[1],coords2[0],coords2[1])


			pointelev = elevationfromcoordinate(False,"decimal",int(middlelat//1),int(middlelon//1), middlelat, middlelon)
			if(printingexcess): print(pointelev)
			#ax2_slicing.plot(i,pointelev,'o', color="red",markersize=5)
			if (pointelev<=15000):
				lineheightinglist.append(pointelev)
				#lineheightinglistradial.append([i*out_degs,pointelev])
			else:
				#lineheightinglist.append(lineheightinglist[len(lineheightinglist)-1])
				pass

			if(printingexcess): print()
			#print(pointelev)
			#print(earth_r+pointelev)
			#print(sec_isosceles(i,earth_r,out_degs))
			
			#m_res = sec_diffsides(i,abs(out_degs), earth_r+5,earth_r+557,spacedist)
			m_res = sec_diffsides(i,abs(azi), k_pre, j_pre,spacedist,cosbeta_pre)
			
			if(printingexcess): print(m_res)
			#print(earth_r+pointelev)
			#print((sec_diffsides(i,abs(out_degs),earth_r+2, earth_r+557,spacedist))-(earth_r+pointelev))
			#print(earth_r-sec_isosceles(i,earth_r,out_degs))
			#if(sec_isosceles(i,12734920+pointelev,out_degs)>(earth_r+pointelev)):
			#	print("is an obstacle")
			if(m_res<(earth_r+pointelev)):
				if(printingexcess): print("is an obstacle")
				#ax1.plot(middlelon, middlelat, 'o', color="yellow",markersize=7, transform=ccrs.PlateCarree())
				is_visible = False
			centerdistancelist.append(m_res-earth_r)
			if(printingexcess):print("_-_-_")
		else:
			is_visible = False
		i+=tracestepsingle

	lineheightinglist.append(elevationfromcoordinate(False,"decimal",int(coords2[0]//1),int(coords2[1]//1), coords2[0], coords2[1])+coords2[2])#253 nahodka mast
	


	return is_visible





reqkeys_calculateareainfos = []
def calculateareainfos(display_map, mast_dec_coord,start_coord,lenghts, **kwargsdata):


	requiredvalues = ["transmr_heightrel"]		
	defaultablevalues = {"write_process_logs":True,"gatherprecisionstep":0.05, "trace_checks_per_one_degree":500, "maxtransmissiondist":0, "logpercentageprecision":5, "receiver_heightrel":2}


	for dfkey in defaultablevalues.keys():
		if (not dfkey in kwargsdata.keys()):
			kwargsdata[dfkey] = defaultablevalues[dfkey] 



	for rqkey in requiredvalues:
		assert (rqkey in kwargsdata.keys()),f'Missing key {rqkey}'



	if(kwargsdata["write_process_logs"]):
		logpercentageprecision = 5
		reachedpercentages=[]

	

	if(display_map==True):

		
		from cartopy.io import shapereader
		import cartopy.io.img_tiles as cimgt
		import cartopy.crs as ccrs

		fig = plt.figure(figsize=(16, 9))
		ax1 = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())

		ax1.coastlines()
		ax1.stock_img()

		ax1.set_extent([min(start_coord[1],mast_dec_coord[1])-0.2,max(start_coord[1]+lenghts[1],mast_dec_coord[1])+0.2, min(start_coord[0],mast_dec_coord[0])-0.2,max(start_coord[0]+lenghts[0],mast_dec_coord[0])+0.2], crs=ccrs.PlateCarree())

		





	covered_tiles_total=0
	noncovered_tiles_total=0

	covered_tiles_land=0
	noncovered_tiles_land=0


	covered_tiles_marine=0
	noncovered_tiles_marine=0

	gathers_projected= (int(lenghts[0]/kwargsdata["gatherprecisionstep"])+1)*(int(lenghts[1]/kwargsdata["gatherprecisionstep"])+1)
	gathers=0

	if(kwargsdata["write_process_logs"]):
		starttime = time.time()

	lai = start_coord[0]
	while(round(lai,3)<=start_coord[0]+lenghts[0]):

		loi = start_coord[1]
		while (round(loi,3)<=start_coord[1]+lenghts[1]):
			res_trace = tracebetweentwo(coords1 = [lai, loi, kwargsdata["receiver_heightrel"]],coords2 =  [mast_dec_coord[0], mast_dec_coord[1], kwargsdata["transmr_heightrel"]], trace_precision = kwargsdata["trace_checks_per_one_degree"], maxdist = kwargsdata["maxtransmissiondist"])
			if(res_trace==False):
				noncovered_tiles_total+=1
				if(display_map==True): ax1.plot(loi,lai, 'o', color="red",markersize=2, transform=ccrs.PlateCarree())
			else:
				covered_tiles_total+=1
				if(display_map==True): ax1.plot(loi,lai, 'o', color="cyan",markersize=2, transform=ccrs.PlateCarree())
			if(elevationfromcoordinate(False,"decimal",int(lai//1),int(loi//1), lai, loi) == 0):
				if(display_map==True): ax1.plot(loi,lai, 'o', color="blue",markersize=1, transform=ccrs.PlateCarree())
			#if(true):
			else:
				if(res_trace==False):
					noncovered_tiles_land+=1
				else:
					covered_tiles_land+=1

			loi+=kwargsdata["gatherprecisionstep"]

			gathers+=1

			if(kwargsdata["write_process_logs"]):
				currpercentage = round(gathers/gathers_projected*100,0)
				if(currpercentage%logpercentageprecision == 0):
					if (not currpercentage in reachedpercentages):

						print(f'{int(currpercentage)} percent complete')
						reachedpercentages.append(currpercentage)



		
		lai+=kwargsdata["gatherprecisionstep"]

	




	if(kwargsdata["write_process_logs"]):
		endtime = time.time();
		print (f"time elapsed:{endtime-starttime}")


	if(display_map==True): 
		ax1.plot(mast_dec_coord[1],mast_dec_coord[0], 'o', color="green",markersize=2, transform=ccrs.PlateCarree())
		plt.show()

	if(noncovered_tiles_total+covered_tiles_total!=0):
		coveragetotal = covered_tiles_total/(noncovered_tiles_total+covered_tiles_total)
	else:
		coveragetotal=0
	if(noncovered_tiles_land+covered_tiles_land!=0):
		coverageland =covered_tiles_land/(noncovered_tiles_land+covered_tiles_land)
	else:
		coverageland=0


	covered_tiles_marine = covered_tiles_total-covered_tiles_land
	noncovered_tiles_marine = noncovered_tiles_total-noncovered_tiles_land

	if(noncovered_tiles_marine+covered_tiles_marine!=0):
		coveragemarine = covered_tiles_marine/(noncovered_tiles_marine+covered_tiles_marine)
	else:
		coveragemarine=0

	

	return dict(gathered_points=gathers, total_covered_tiles = covered_tiles_total, total_noncovered_tiles=noncovered_tiles_total, total_coverage=coveragetotal, land_covered_tiles = covered_tiles_land, land_noncovered_tiles=noncovered_tiles_land, land_coverage=coverageland, nautical_covered_tiles = covered_tiles_marine, nautical_noncovered_tiles=noncovered_tiles_marine, nautical_coverage=coveragemarine)









if __name__=="__main__":
	#print(calculateareainfos(True, [43.1225,131.899444],[42,131],[1.5,2], maxdist = 30000,  transmr_heightrel=187, receiver_heightrel=52, gatherprecisionstep = 0.03, trace_checks_per_one_degree = 250, write_process_logs = True))
	#print(dataslist.keys())
	pass
