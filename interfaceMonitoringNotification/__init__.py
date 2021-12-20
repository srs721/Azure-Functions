import logging
import os
import azure.functions as func

def send_data_to_serviceBus(data_body):

    connections_string = os.environ.get('AzureWebJobsServiceBus')
    queues_name = os.environ.get('serviceBusInterfaceQueue')

    CONNECTION_STR = connections_string
    QUEUE_NAME = queues_name
    logging.info(QUEUE_NAME)

    def send_message(sender):
        try:
            message = azure.servicebus.ServiceBusMessage(data_body)
            sender.send_messages(message)
            logging.info(message)
            return "Data sent successfully!"

        except Exception as e:
            logging.error(str(e))
            return str(e)

    servicebus_client = azure.servicebus.ServiceBusClient.from_connection_string(conn_str=CONNECTION_STR, logging_enable=True)

    with servicebus_client:
        sender = servicebus_client.get_queue_sender(queue_name=QUEUE_NAME)
        with sender:
            send_message(sender)   


def main(req: func.HttpRequest) -> func.HttpResponse:

    logging.info('Python HTTP trigger function processed a request.')
    
    data_body = req.get_body()
    if data_body:
        logging.info(data_body)
        get_result = send_data_to_serviceBus(data_body)
        return func.HttpResponse(get_result,status_code=200)
    else:
        logging.info("Missing Data")
        return func.HttpResponse("Missing data")