#!/usr/bin/env python
import math
import urllib
from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError
import json
import os
from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)
intent_name="string"
@app.route('/webhook', methods=['POST'])
def webhook():
	req = request.get_json(silent=True, force=True)
	print("Request:")
	print(json.dumps(req, indent=4))
	res = processRequest(req)
	res = json.dumps(res, indent=4)
	print("after json.dumps",res)
	r = make_response(res)
	r.headers['Content-Type'] = 'application/json'
	return r

def processRequest(req):
	if req.get("result").get("action") != "final_budget":
		return {}
	global city_names
	global QR
	global intent_name
	global s_id
	global str
	global r_slug
	global im_url
	intent_name=processIntentName(req)
	city_names=processlocation(req)
	property_type=processPropertyType(req)
	maximum_valu=processMaximum(req)
	price_unit=processPriceUnit(req)
	max_area=processAreaMax(req)
	unit_property=processUnits(req)
	s_id=processsession(req)
	maximum_value=convertMaximum(maximum_valu, price_unit)
	print(maximum_value)

	#baseurl = "https://aarz.pk/bot/index.php?city_name="+city_names+"&sector_name="+sector_names+"&minPrice="+maximum_value+"&type="+property_type+"&LatestProperties="+latest+"&UnitArea="+area_property+"&Unit="+unit_property+"&school="+school+"&airport="+airport+"&transport="+transport+"&security="+security+"&shopping_mall="+malls+"&fuel="+fuel
	#baseurl="https://www.aarz.pk/search/bot?postedBy=searchPage&view=&city_s="+city_names+"&price_min="+maximum_value+"&price_max=0estate_agent=&purpose=Sell&property_type="+property_type
	if maximum_value == 0:
		baseurl="https://www.aarz.pk/search/bot?postedBy=searchPage&view=&city_s="+city_names+"&type="+property_type+"&land_area="+unit_property+"&min_r=0&max_r="+max_area
	else:  
		baseurl="https://www.aarz.pk/search/bot?postedBy=searchPage&view=&city_s="+city_names+"&type="+property_type+"&price_max="+maximum_value+"&land_area="+unit_property+"&min_r=0&max_r="+max_area
	#print("city:",city_names)
	print("url is:",baseurl)
	result = urllib.request.urlopen(baseurl).read()
	#print('result of url:', result)
	data = json.loads(result)
	#print('data:', data)
	#res2=json_to_text(data)
	res2 = makeWebhookResult(data)
	print('res2:',res2)
	return res2

def processIntentName(req):
	result = req.get("result")
	parameters = result.get("metadata")
	intent = parameters.get("intentName")
	return intent
def processsession(req):
	session_id = req.get("sessionId")
	#print(session_Id)
	return session_id
def recommendationalgo():
	rating=10
	buy1={}
	buy2={}
	smallbuy={}

	avgmid={}
	avg=0
	avrg={}
	hcount=0
	actualvector={}

	mod1=0
	mod2=0
	modict1={}
	modict2={}

	vecmul=0
	reslt=0

	simdict={}
	suggestiondic={}
	simusrs={}
	

	hfh="no one"
	housecount=0
	hcountf=0

	#s_id='1C11'
	#row_title=['1500 Square Feet C Type Apartment for Sale in i-11','C type apartment for sale in i-11 isb','C, D & E Type apartments for sale in G-11/3','E Type Apartment for Sale','15 Marla Plot for Sale in Islamabad F-10']

	cominglist={}
	comingdata={}

	for val in row_title:
		cominglist.update({val:rating})
		rating=rating-2
	comingdata.update({s_id:cominglist})

	buy1={'1C1':{'1450 Square Feet Apartment for Sale in Islamabad F-10':10,'666 Square Yard Plot for Sale in Islamabad F-10/2':8},
	'1C2':{'1 Kanal Residential Land for Sale in Peshawar DHA Defence':10,'15 Marla House for Sale in Peshawar Abshar Colony':8},
	'1C3':{'10.6 Marla House for Sale in Quetta Double Road':10,'5 Marla House for Sale in Quetta Chilten Housing Scheme':8},
	'1C4':{'1 Kanal House for Sale in Rawalpindi Bahria Town':10,'10 Marla House for Sale in Rawalpindi Bahria Town Phase-2':8},
	'1C5':{'1 Kanal Bungalow Available For Sale in AFOHS New Malir':10,'1 Kanal Plot For Sale In DHA Phase-8':8},
	'1C6':{'1 Kanal House For Sale In Askari-5, Lahore':10,'1 Kanal House for Rent in Lahore DHA Phase-5 Block K':8}}

	url={'1C1':{'1450 Square Feet Apartment for Sale in Islamabad F-10':{'1450-square-feet-apartment-for-sale-in-f-10-islamabad-for-rs-80-lac-99671','uploads\/properties\/2017\/8\/1450-square-feet-apartment-for-sale-in-f-10-islamabad-for-rs-80-lac-99671-image-1.jpg'},'666 Square Yard Plot for Sale in Islamabad F-10/2':{'666-square-yard-plot-for-sale-in-f-102-islamabad-for-rs-75-crore-100682','uploads\/properties\/2017\/8\/666-square-yard-plot-for-sale-in-f-102-islamabad-for-rs-75-crore-100682-1502094279-image-0.jpg'}}
	,'1C2':{'1 Kanal Residential Land for Sale in Peshawar DHA Defence':{'40-kanal-land-available-for-sale-near-hayat-abad-and-al-haram-peshawar-37428','uploads\/properties\/2017\/4\/40-kanaal-land-available-near-hayat-abad-and-al-haram-37428-image-1.jpg'},'15 Marla House for Sale in Peshawar Abshar Colony':{'13-marla-house-is-available-for-sale-askari-5-peshawar-38524','uploads\/properties\/2017\/4\/13-marla-house-is-available-for-sale-askari-5-peshawar-38524-image-1.jpg'}},
	'1C3':{'10.6 Marla House for Sale in Quetta Double Road':{'106-marla-house-for-sale-in-double-road-quetta-for-rs-18-crore-89134','uploads\/properties\/2017\/7\/house-for-sale-at-double-road-quetta-89134-image-1.jpg'},'5 Marla House for Sale in Quetta Chilten Housing Scheme':{'8-marla-house-for-sale-in-arbab-town-quetta-77326','uploads\/properties\/2017\/6\/8-marla-house-for-sale-in-arbab-town-quetta-77326-image-1.jpg'}},
	'1C4':{'1 Kanal House for Sale in Rawalpindi Bahria Town':{'1-kanal-house-for-sale-in-bahria-town-rawalpindi-for-rs-32-crore-101225','uploads\/properties\/2017\/8\/1-kanal-house-for-sale-in-bahria-town-rawalpindi-for-rs-32-crore-101225-image-1.jpg'},'10 Marla House for Sale in Rawalpindi Bahria Town Phase-2':{'10-marla-house-for-sale-in-bahria-town-phase-2-rawalpindi-for-rs-225-crore-101234','uploads\/properties\/2017\/8\/10-marla-house-for-sale-in-bahria-town-phase-2-rawalpindi-for-rs-225-crore-101234-image-1.jpg'}},
	'1C5':{'1 Kanal Bungalow Available For Sale in AFOHS New Malir':{'1-kanal-bungalow-available-for-sale-in-afohs-new-malir-54978','uploads\/properties\/2017\/5\/1-kanal-available-for-sale-in-afohs-new-malir-54978-image-1.jpg'},'1 Kanal Plot For Sale In DHA Phase-8':{'1-kanal-plot-for-sale-in-dha-phase-8-57932','uploads\/properties\/2017\/5\/1-kanal-plot-for-sale-57932-image-1.jpg'}},
	'1C6':{'1 Kanal House For Sale In Askari-5, Lahore':{'1-kanal-house-for-sale-in-askari-5-lahore-52144','uploads\/properties\/2017\/5\/1-kanal-house-for-sale-in-askari-5-lahore-52144-image-1.jpg'},'1 Kanal House for Rent in Lahore DHA Phase-5 Block K':{'1-kanal-house-for-rent-in-dha-phase-5-block-k-lahore-for-rs-15-lac-101337','uploads\/properties\/2017\/8\/1-kanal-house-for-rent-in-dha-phase-5-block-g-lahore-for-rs-13-lac-101337-image-1.jpg'}}}
	
	buy1.update(comingdata)

	print (buy1)

	#taking average

	for outerkey in buy1:
		avgmid.update(buy1[outerkey])
		for key in avgmid:
			avg=avg+avgmid[key]
			hcount=hcount+1
		avrg.update({outerkey:avg/hcount})
		avg=0
		avgmid.clear()
		hcount=0


#centered cosine

	for outerkey in buy1:
		buy2.update({outerkey:buy1[outerkey]})
		for okey in buy2:
			smallbuy.update(buy2[okey])
			for key in smallbuy:
				smallbuy[key]=smallbuy[key]-avrg[outerkey]
			actualvector.update({outerkey:smallbuy})
			smallbuy={}
		buy2.clear()	
	#print (actualvector)


#cosine similarity

	for outerkey in actualvector:
		modict1.update(actualvector[outerkey])
		for value in modict1:
			mod1=mod1+(modict1[value]*modict1[value])
		mod1=math.sqrt(mod1)
		for outerkey2 in actualvector:
			modict2.update(actualvector[outerkey2])
			for value in modict2:
				mod2=mod2+(modict2[value]*modict2[value])
			mod2=math.sqrt(mod2)
			for value in modict1:
				if value in modict2:
					vecmul=vecmul+(modict1[value]*modict2[value])
			if(vecmul/(mod1*mod2)>=reslt and outerkey2!=outerkey and modict1!=modict2):
				reslt=(vecmul/(mod1*mod2))
				simusr=outerkey2
			vecmul=0
			modict2={}
		simdict.update({outerkey:simusr})
		modict1={}
		reslt=0

#print (simdict)


#suggesting

	for key in simdict:
		for key2 in buy1[simdict[key]]:
			if key2 not in buy1[key]:
			#print("Suggestion for", key,":", key2)
				if key not in suggestiondic:
					suggestiondic[key]=key2		


#users who have no similar users

	for user in buy1:
		for house in buy1[user]:
			for user2 in buy1:
				if house in  buy1[user2]:
					housecount=housecount+1
			if(housecount>hcountf):
				hcountf=housecount
				hfh=house
			housecount=0

	for user in simdict:
		if user not in suggestiondic:
			suggestiondic[user]=hfh
		#print("Suggestion for", user,":", hfh)

#print (suggestiondic)

	for val in suggestiondic:
		if val==s_id:
			str=suggestiondic[val]

#storing row_slug and image url
	global suggesting_user
	global r_slug
	global im_url
	suggesting_user=simdict[s_id]
	flag_i=0	    
	for value in url[suggesting_user][str]:
		if flag_i==0:
			r_slug=value
			flag_i=flag_i+1
		else:
			im_url=value
			flag_i=0
	#sts='ashar'
	return (str,r_slug,im_url)
def processlocation(req):
	global city
	result = req.get("result")
	parameters = result.get("parameters")
	cityNames = parameters.get("location")
	city = cityNames.get("city")
	#print("city data:", city)
	#print("city:", city)

	return city

#Price and Unit
def processMaximum(req):
	result = req.get("result")
	parameters = result.get("parameters")
	act_pri = parameters.get("actual_price")
	if act_pri == '0':
		return act_pri
	else:
		maximum = act_pri.get("number")
	return maximum

def processPriceUnit(req):
	result = req.get("result")
	parameters = result.get("parameters")
	price_unit = parameters.get("price_unit")
	return price_unit

def processMinimum(req):
	result = req.get("result")
	parameters = result.get("parameters")
	min_price = parameters.get("min_price")
	return min_price

def processPropertyType(req):
	result = req.get("result")
	parameters = result.get("parameters")
	propertyType = parameters.get("PropertyType")
	return propertyType

def processAreaMax(req):
	result = req.get("result")
	parameters = result.get("parameters")
	max_area = parameters.get("max_area")
	return max_area

def processUnits(req):
	result = req.get("result")
	parameters = result.get("parameters")
	units = parameters.get("Unit")
	print(units)
	return units

def processProjectName(req):
	result = req.get("result")
	parameters = result.get("parameters")
	project_name = parameters.get("ProjectName")
	return project_name 

#Price
def convertMaximum(pric, unit):
	print(pric)
	price = int(pric)
	print(price)
	if unit[0] == 'z':
		price = int(pric)
	elif unit[0] == 'l' or unit[0] == 'L':
		price = price * (10 ** 5)
	elif unit[0] == 'm' or unit[0] == 'M':
		price = price * (10 ** 6)
	elif unit[0] == 'c' or unit[0] == 'C':
		price = price * (10 ** 7)
	print(price)
	return str(price)

def makeWebhookResult(data):
	i=0
	global row_title
	length=len(data)
	speech_data = "Here are some properties with your choice. We have total of "+str(length)+" records of your interest in city  "+city+"."
	text_data = "Here are some properties with your choice. We have total of "+str(length)+" records of your interest in city  "+city+"."
	row_id=['test','test1','test2','test3','test4','test5','test6','test7','test8','test9','test10']
	row_title=['test','test1','test2','test3','test4','test5','test6','test7','test8','test9','test10']
	row_location=['test','test1','test2','test3','test4','test5','test6','test7','test8','test9','test10']
	row_price=['test','test1','test2','test3','test4','test5','test6','test7','test8','test9','test10']
	row_slug=['test','test1','test2','test3','test4','test5','test6','test7','test8','test9','test10']
	row_number=['test','test1','test2','test3','test4','test5','test6','test7','test8','test9','test10']
	row_image=['test','test1','test2','test3','test4','test5','test6','test7','test8','test9','test10']
	row_city=['test','test1','test2','test3','test4','test5','test6','test7','test8','test9','test10']
	while (i <length):
		row_id[i]=data[i]['property_id']
		row_title[i]=data[i]['title']
		row_location[i]=data[i]['address']
		if row_location[i] == "" or row_location[i] == " ":
		   row_location[i] = "not specified"
		row_price[i]=data[i]['price']
		row_slug[i]=data[i]['slug']
		row_number[i]=data[i]['number']
		row_image[i]=data[i]['image']
		row_city[i]=data[i]['city_name']
		speech_data_parts="Here is record " + str(i+1) +":"+ row_title[i]+" in city "+row_city[i] + " price is "+ str(row_price[i]) + "."
		speech_data = speech_data + speech_data_parts
		text_data_parts ="Here is record " + str(i+1) +":"+ row_title[i]+" in city "+row_city[i] + " price is "+ str(row_price[i])+ ". For Info about this contact at number "+str(row_number[i]) + "."
		text_data = text_data + text_data_parts	
		i+=1
	print(row_title[0])
	(algostr,r_slug,im_url)=recommendationalgo()
	algos = "suggestion: " + algostr
	text_data = text_data + algos + r_slug + im_url
	variable1=str(row_number[0])
	variable2=str(row_number[1])
	variable3=str(row_number[2])
	variable4=str(row_number[3]) 
	#print('speech Data',speech_data)
	#print('Text Data',text_data)
	if "Unable" in row_title[0]:
        message={
	  "attachment":{
	   "type":"template",
	      "payload":{
	"template_type":"generic",
	"elements":[
             {
             "title":algos,
              #"subtitle":row_location[0],
              #"subtitle":"Price: Rs."+str(row_price[0]),
                "item_url": "https://www.aarz.pk/property-detail/"+r_slug,               
               "image_url":"https://www.aarz.pk/"+im_url ,
             "buttons":[
                 {
                "type":"element_share"
                  }
            ]
          }
    ]
          }
      }
}
	elif length==1:
		message={
	  "attachment":{
	   "type":"template",
	      "payload":{
	"template_type":"generic",
	"elements":[
          {
             "title":row_title[0],
              "subtitle":row_location[0],
              "subtitle":"Price: Rs."+str(row_price[0]),
                "item_url": "https://www.aarz.pk/property-detail/"+row_slug[0],               
               "image_url":"https://www.aarz.pk/"+row_image[0] ,
             "buttons":[
              {
              "type":"phone_number",
              "title":"Call Agent",
              "payload":"+92"+variable1[1:]
              },
                 {
                "type":"element_share"
                  }
            ]
          }
          {
             "title":algos,
              #"subtitle":row_location[0],
              #"subtitle":"Price: Rs."+str(row_price[0]),
                "item_url": "https://www.aarz.pk/property-detail/"+r_slug,               
               "image_url":"https://www.aarz.pk/"+im_url ,
             "buttons":[
                 {
                "type":"element_share"
                  }
            ]
          }
        ]
      }
    }
  }
	elif length==2:
		message= {
         "attachment": {
           "type": "template",
            "payload": {
               "template_type": "generic",
               "elements": [{
               "title": row_title[0],
                "subtitle":row_location[0],
              "subtitle":"Price: Rs."+str(row_price[0]),
                "item_url": "https://www.aarz.pk/property-detail/"+row_slug[0],               
               "image_url":"https://www.aarz.pk/"+row_image[0]  ,
                "buttons": [{
                "type":"phone_number",
              "title":"Call Agent",
             "payload":"+92"+variable1[1:]
                },
                    {
                "type":"element_share"
                    
                    }, 
                   ],
          }, 
                   {
                "title": row_title[1],
                 "subtitle":row_location[1],
              "subtitle":"Price: Rs."+str(row_price[1]),
                 "item_url": "https://www.aarz.pk/property-detail/"+row_slug[1],               
               "image_url":"https://www.aarz.pk/"+row_image[1]  ,
                "buttons": [{
                "type":"phone_number",
              "title":"Call Agent",
             "payload":"+92"+variable2[1:]
            },
                     {
                "type":"element_share"
                    
                    }, 
                   ]
          },
                   {
             "title":algos,
              #"subtitle":row_location[0],
              #"subtitle":"Price: Rs."+str(row_price[0]),
                "item_url": "https://www.aarz.pk/property-detail/"+r_slug,               
               "image_url":"https://www.aarz.pk/"+im_url ,
             "buttons":[
                 {
                "type":"element_share"
                  }
            ]
          }
               ]
            
        }
      }
    }
	else:
		message= {
         "attachment": {
           "type": "template",
            "payload": {
               "template_type": "generic",
               "elements": [
                   {
               "title": row_title[0],
                "subtitle":row_location[0],
              "subtitle":"Price: Rs."+str(row_price[0]),
                "item_url": "https://www.aarz.pk/property-detail/"+row_slug[0],               
               "image_url":"https://www.aarz.pk/"+row_image[0]  ,
                "buttons": [{
                "type":"phone_number",
              "title":"Call Agent",
              "payload":"+92"+variable1[1:]
                },
                    {
                "type":"element_share"
                  
            }, 
                   ],
          }, 
                   {
               "title": row_title[1],
               "subtitle":row_location[1],
              "subtitle":"Price: Rs."+str(row_price[1]),
                "item_url": "https://www.aarz.pk/property-detail/"+row_slug[1],               
               "image_url":"https://www.aarz.pk/"+row_image[1]  ,
                "buttons": [{
                "type":"phone_number",
              "title":"Call Agent",
              "payload":"+92"+variable2[1:]
            }, 
                     {
                "type":"element_share"
                    
                    }, 
                   ],
          }, 
                   {
               "title": row_title[2],
                "subtitle":row_location[2],
              "subtitle":"Price: Rs."+str(row_price[2]),
                "item_url": "https://www.aarz.pk/property-detail/"+row_slug[2],               
               "image_url":"https://www.aarz.pk/"+row_image[2]  ,
                "buttons": [{
               "type":"phone_number",
              "title":"Call Agent",
              "payload":"+92"+variable3[1:]
            }, 
                     {
                "type":"element_share"
                    
                    }, 
                   ],
          },
                    {
             "title":algos,
              #"subtitle":row_location[0],
              #"subtitle":"Price: Rs."+str(row_price[0]),
                "item_url": "https://www.aarz.pk/property-detail/"+r_slug,               
               "image_url":"https://www.aarz.pk/"+im_url ,
             "buttons":[
                 {
                "type":"element_share"
                  }
            ]
          }
               ]
            }
         }
}
	return {
        "speech": text_data,
        "displayText": text_data,
        "data": {"facebook": message},
        "contextOut": [],
        "source": "apiai-onlinestore-shipping"
    }
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

app.run(debug=True, port=port, host='0.0.0.0')
