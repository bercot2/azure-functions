import azure.functions as func
import aiohttp
import asyncio
import logging

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)


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
    # URL do endpoint da Azure Function HTTP Trigger
    http_trigger_url = "https://function-teste-b2.azurewebsites.net/api/http_trigger?code=x5N-CmeYZRLB90Sbd4tfdT8iZ7KAqEWUL8zj5e11NP1fAzFukGEuSA%3D%3D"

    # Diferentes payloads para as 5 requisições
    payloads = [
        {"unidades_consumidoras": [1, 2, 3], "secounds": 5},
        {"unidades_consumidoras": [4, 5, 6], "secounds": 5},
        {"unidades_consumidoras": [7, 8, 9], "secounds": 5},
        {"unidades_consumidoras": [10, 11, 12], "secounds": 5},
        {"unidades_consumidoras": [13, 14, 15], "secounds": 5},
    ]

    # Lista para armazenar as tarefas
    tasks = []

    # Cria uma sessão HTTP assíncrona
    async with aiohttp.ClientSession() as session:
        for payload in payloads:
            logging.info(f"Inicializando o payload: {payload}")

            # Cria uma tarefa para cada requisição
            tasks.append(make_request(session, http_trigger_url, payload))

        # Aguarda a conclusão de todas as tarefas
        responses = await asyncio.gather(*tasks)

    # Processa as respostas recebidas
    for idx, response in enumerate(responses):
        logging.info(f"Resposta da requisição {idx + 1}: {response}")


async def make_request(session, url, payload):
    try:
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
