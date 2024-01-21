import sslclient

def update_world_model(model):
    ssl_vision_ip_addr = "244.5.23.2"
    client = sslclient.client(ssl_vision_ip_addr, port=10006)
    client.connect()

    data = client.receive()

    if data.HasField('geometry'):
        model.update_geometry(data.geometry)

    if data.HasField('detection'):
        model.update_detection(data.detection)