import os
import json
import time
import aiohttp
import asyncio
import logging
import azure.functions as func

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

# Obtém a URL do HTTP Trigger da variável de ambiente
HTTP_TRIGGER_URL = os.getenv("HTTP_TRIGGER_URL")

if not HTTP_TRIGGER_URL:
    raise ValueError("A variável de ambiente 'HTTP_TRIGGER_URL' não foi configurada.")


@app.timer_trigger(
    schedule="0 * * * * *",
    arg_name="myTimer",
    run_on_startup=False,
    use_monitor=False,
    disabled=False,
)
def timer_trigger(myTimer: func.TimerRequest) -> None:
    logging.info("Executando Function Timer")

    # Executa a lógica assíncrona para processar as requisições
    asyncio.run(execute_parallel_requests())

    logging.info("Todas as requisições foram concluídas.")


async def execute_parallel_requests():
    # Diferentes payloads para as 5 requisições
    payloads = [
        {"unidades_consumidoras": [1, 2, 3], "secounds": 0},
        {"unidades_consumidoras": [4, 5, 6], "secounds": 0},
        {"unidades_consumidoras": [7, 8, 9], "secounds": 0},
        {"unidades_consumidoras": [10, 11, 12], "secounds": 0},
        {"unidades_consumidoras": [13, 14, 15], "secounds": 0},
    ]

    # Lista para armazenar as tarefas
    tasks = []

    # Cria uma sessão HTTP assíncrona
    async with aiohttp.ClientSession(
        timeout=aiohttp.ClientTimeout(total=120)
    ) as session:
        for payload in payloads:
            logging.info(f"Inicializando o payload: {payload}")

            # Cria uma tarefa para cada requisição
            tasks.append(make_request(session, HTTP_TRIGGER_URL, payload))

        # Aguarda a conclusão de todas as tarefas
        responses = await asyncio.gather(*tasks)

    # Processa as respostas recebidas
    for idx, response in enumerate(responses):
        logging.info(f"Resposta da requisição {idx + 1}: {response}")


async def make_request(session, url, payload):
    try:
        logging.info(f"realizando request | payload: {payload}")

        async with session.post(url, json=payload) as response:
            if response.status == 200:
                # Retorna o JSON da resposta
                return await response.json()
            else:
                # Retorna o status de erro
                return {"error": f"Status {response.status}"}
    except Exception as e:
        # Trata erros durante a requisição
        return {"error": str(e)}


@app.route(route="http_trigger", auth_level=func.AuthLevel.FUNCTION)
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Python HTTP trigger function processed a request.")

    time.sleep(req.get_json().get("secounds", 0))

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
