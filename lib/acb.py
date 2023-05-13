# Print variables
def print_variable(variable_name, variable_value, colon_position=0):
    key = variable_name
    #val = globals()[variable_name]
    val = variable_value
    print("{}".format(key) + (" " * max(0, colon_position - len(key))), ":", val)

# MQTT subroutines
def mqtt_subscribe_callback(topic, msg):
    print((topic, msg))

def mqtt_connect(client_id, mqtt_srvr, mqtt_port, mqtt_user, mqtt_pass):
    from umqttsimple import MQTTClient
    client = MQTTClient(client_id, mqtt_srvr, int(mqtt_port), mqtt_user, mqtt_pass)
    client.connect()
    #print("Connected to MQTT broker %s" %mqtt_srvr)
    #print("Publishing to MQTT topic %s" %topic_pub)
    return client

def mqtt_connect_and_subscribe(client_id, mqtt_srvr, topic_sub, mqtt_subscribe_callback):
    from umqttsimple import MQTTClient
    client = MQTTClient(client_id, mqtt_srvr)
    client.set_callback(mqtt_subscribe_callback)
    client.connect()
    client.subscribe(topic_sub)
    #print('Connected to %s MQTT broker, subscribed to %s topic' %(mqtt_srvr, topic_sub))
    return client
