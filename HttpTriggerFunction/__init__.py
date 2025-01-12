import azure.functions as func
import logging
import json
import time

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)


@app.route(route="http_trigger")
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Python HTTP trigger function processed a request.")

    logging.info("teste2")

    time.sleep(req.get_json().get("secounds", None))

    unidades_consumidoras = req.get_json().get("unidades_consumidoras")
    if unidades_consumidoras:
        return func.HttpResponse(
            json.dumps(
                {
                    "response": "Lista Processada",
                    "return": unidades_consumidoras,
                }
            ),
            mimetype="application/json",
        )

    return func.HttpResponse(
        "Obrigatório envio da lista de Unidades Consumidoras!",
        status_code=200,
    )
