
#!/usr/bin/env python

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
    intent_name=processIntentName(req)
    city_names=processlocation(req)
    property_type=processPropertyType(req)
    maximum_valu=processMaximum(req)
    price_unit=processPriceUnit(req)
    max_area=processAreaMax(req)
    unit_property=processUnits(req)

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
     variable1=str(row_number[0])
     variable2=str(row_number[1])
     variable3=str(row_number[2])
     variable4=str(row_number[3]) 
     #print('speech Data',speech_data)
     #print('Text Data',text_data)
     if "Unable" in row_title[0]:
        message={
         "text":"Sorry there is no such property available."           
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
          }]
            
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
