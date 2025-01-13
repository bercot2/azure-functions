# azure-functions

- Como instalar a CLI do Azure
https://learn.microsoft.com/pt-br/cli/azure/install-azure-cli

- Desenvolver o Azure Functions usando o Visual Studio Code
https://learn.microsoft.com/pt-br/azure/azure-functions/functions-develop-vs-code?tabs=node-v4%2Cpython-v2%2Cisolated-process%2Cquick-create&pivots=programming-language-python

- Desenvolver o Azure Functions localmente usando o Core Tools
https://learn.microsoft.com/pt-br/azure/azure-functions/functions-run-local?tabs=windows%2Cisolated-process%2Cnode-v4%2Cpython-v2%2Chttp-trigger%2Ccontainer-apps&pivots=programming-language-python

# Forma de subir Function para o APP
 - Deverá clicar F1 no VS Code e criar o app do function.
 - Após criar o app do Function, deverá configurar o repositório do git na parte de armazenamento do app.
 - Agora basta clicar F1 e escolher a opção Azure Functions: Deploy to Function App.

# Como criar uma function manualmente
func new

# Como verificar as functions existentes no app
az functionapp function list --name <NOME_DA_FUNCTION_APP> --resource-group <NOME_DO_GRUPO_DE_RECURSOS>

# Configurar Deploy automático via "Push" na Branch principal configurada na Function Azure

- Configurar no action gerado pela Azure conforme abaixo:
```
    # Deploy para o Azure Functions
    - name: Deploy to Azure Functions
      uses: Azure/functions-action@v1
      with:
        app-name: "function-azure-teste-b2"  # Nome do Function App no Azure
        package: "."                        # Diretório do código
        publish-profile: "${{ secrets.AZURE_FUNCTIONAPP_PUBLISH_PROFILE }}"
```

- Criar o Publish Profile no Azure
O publish profile é necessário para autenticar o GitHub com o Azure Functions.

No portal do Azure:

Navegue até o seu Function App.

Vá para Configurações > Deployment > Deployment Center.
Clique em Get Publish Profile para baixar o arquivo de perfil de publicação.

No GitHub:

Vá até o repositório.

Clique em Settings > Secrets and variables > Actions > New repository secret.
Adicione um segredo com o nome AZURE_FUNCTIONAPP_PUBLISH_PROFILE e cole o conteúdo do publish profile.

# Formas de configurar funções separadamente
 - Exemplo de estrutura abaixo:
```
├── HttpTriggerFunction/
│   ├── __init__.py       # Código do HttpTrigger
│   ├── function.json     # Configuração da função HTTP Trigger
├── TimerTriggerFunction/
│   ├── __init__.py       # Código do TimerTrigger
│   ├── function.json     # Configuração da função Timer Trigger
├── requirements.txt       # Dependências do projeto
├── host.json              # Configuração do app
├── local.settings.json    # Configuração local (opcional)
```

> Exemplo do arquivo function.json
```
{
  "scriptFile": "__init__.py",
  "bindings": [
    {
      "authLevel": "function",
      "type": "httpTrigger",
      "direction": "in",
      "name": "req",
      "route": "http_trigger",
      "methods": ["get", "post"]
    },
    {
      "type": "http",
      "direction": "out",
      "name": "res"
    }
  ]
}
```

Nesse formato, cada function deverá ter sua própria pasta

> Possíveis erros
- A variável de Ambiente abaixo pode ocasionar problema, caso ocorra problema, basta remover essa variável de ambiente, caso esteja utilizando o deploy via git actions
{
    "name": "WEBSITE_RUN_FROM_PACKAGE",
    "value": "https://functionoperacaocpb2.blob.core.windows.net/github-actions-deploy/Functionapp_2025112193629437.zip?sv=2023-11-03&st=2025-01-12T19%3A31%3A32Z&se=2026-01-12T19%3A36%3A32Z&sr=b&sp=r&sig=rVRrNSMj61d8zFfwNNHSwd7mu6y06iu2b%2BR4btzW6TE%3D",
    "slotSetting": false
}
