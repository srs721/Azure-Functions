# Azure-Functions
This repo is about azure functions.
There are two functions included whith different logic.

I am using a portal which displays information about various networking devices. The functions are used to fetch the information using Rest API.


AZURE SERVICE BUS - Messaging bus on cloud, that is used to tranfer data and connect cloud to other applications and services. We can create and service bus on azure. 
To use the service bus in function, simply under the configurations add a new environment variable and its value as service bus name. use the environment variable in the script.
The connection string - azurewebservicebus conatins cred stored in key vault - Example - @Microsoft.KeyVault(SecretUri=https://{function_url}/secrets/ServiceBusConnectionString/{id})

1. Availability Issue Report --- 
   Using three different URLS I am fetching the required data and sending it to our public function url.
  First url is used to get the dashboard id, once the dasboard id is fetched we fetch the widget information using the next url. The final url is used to fetch the device's availability score.
  
2. Interface Monitoring Function ---
   Part 1 - Includes two parts, In the servicenow portal user will create a service request with an attached excel sheet. The excel sheet will contain data about the devices and whether
  they should be monitored or not. Based on the monitoring column I will pick only those devices and create a SERVICENOW workflow which will have script to convert the excel data into
  required json format and also fetch the details of devices like the manufactuer name and company name from its sys_id.
  
  Part 2 - Once the json is ready, it is then sent to the azure function using POST request. The json data received in azure function, is then converted into required format needed and
  sent to SERVICEBUS, one by one.
