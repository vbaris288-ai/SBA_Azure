import azure.functions as func
import logging
import math
import json

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="CalculateArea")
def CalculateArea(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger CalculateArea processed a request.')

    try:
        req_body = req.get_json()
    except ValueError:
        return func.HttpResponse(
             json.dumps({"error": "Invalid JSON payload."}),
             status_code=400,
             mimetype="application/json"
        )
        
    shape = req_body.get('shape')
    
    if not shape:
        return func.HttpResponse(
             json.dumps({"error": "Please pass a shape in the request body"}),
             status_code=400,
             mimetype="application/json"
        )
        
    area = 0
    try:
        if shape == 'circle':
            radius = req_body.get('radius')
            if radius is None:
                raise ValueError("Please pass a radius for circle")
            area = math.pi * (float(radius) ** 2)
        elif shape == 'rectangle':
            length = req_body.get('length')
            width = req_body.get('width')
            if length is None or width is None:
                raise ValueError("Please pass length and width for rectangle")
            area = float(length) * float(width)
        elif shape == 'triangle':
            base = req_body.get('base')
            height = req_body.get('height')
            if base is None or height is None:
                raise ValueError("Please pass base and height for triangle")
            area = 0.5 * float(base) * float(height)
        else:
            return func.HttpResponse(
                json.dumps({"error": f"Unknown shape: {shape}"}), 
                status_code=400,
                mimetype="application/json"
            )
            
    except ValueError as e:
        return func.HttpResponse(
            json.dumps({"error": str(e)}), 
            status_code=400,
            mimetype="application/json"
        )

    return func.HttpResponse(
        json.dumps({"shape": shape, "area": area}),
        mimetype="application/json"
    )
