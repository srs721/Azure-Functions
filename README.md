# Azure-Functions
This repo is about azure functions.
There are two functions included whith different logic.

I am using a portal which displays information about various networking devices. The functions are used to fetch the information using Rest API.

1. Availability Issue Report --- 
   Using three different URLS I am fetching the required data and sending it to our public function url.
  First url is used to get the dashboard id, once the dasboard id is fetched we fetch the widget information using the next url. The final url is used to fetch the device's availability score.
  
2. Interface Monitoring Function ---
   Part 1 - Includes two parts, In the servicenow portal user will create a service request with an attached excel sheet. The excel sheet will contain data about the devices and whether
  they should be monitored or not. Based on the monitoring column I will pick only those devices and create a SERVICENOW workflow which will have script to convert the excel data into
  required json format and also fetch the details of devices like the manufactuer name and company name from its sys_id.
  
  Part 2 - Once the json is ready, it is then sent to the azure function using POST request. The json data received in azure function, is then converted into required format needed and
  sent to SERVICEBUS, one by one.
