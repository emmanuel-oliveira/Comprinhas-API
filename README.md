# API de Automatização de Links de Afiliados


## Objetivos

Automatizar a gestão de promoções de links de afiliados, garantindo rapidez e precisão no envio de ofertas de qualidade para os administradores e, posteriormente, para o público-alvo.

## Descrição

Esta API, desenvolvida em Flask (Python), automatiza o processo de criação e publicação de links de afiliados. O fluxo é o seguinte:

1. **Busca de Promoções**: A API consulta a **API da Shopee** para encontrar promoções, aplicando filtros baseados na confiabilidade do vendedor e no nível de desconto.
2. **Geração de Texto**: Utiliza a **Gemini API (LLM)** para criar um texto personalizado sobre o produto em promoção.
3. **Aprovação dos Administradores**: Envia a promoção e o texto gerado para aprovação dos administradores via **Telegram**, utilizando bots. Os administradores têm três opções:
   - **Negar**: Não publicar a oferta.
   - **Aprovar**: Publicar a oferta no canal de promoções.
   - **Refazer Texto**: Solicitar à LLM que gere um novo texto para a promoção.
4. **Publicação**: Após a aprovação, a promoção é publicada automaticamente em um canal de promoções no Telegram.

## Tecnologias Utilizadas

![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white) ![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white) ![MongoDB](https://img.shields.io/badge/MongoDB-%234ea94b.svg?style=for-the-badge&logo=mongodb&logoColor=white)
- **Python**: Linguagem de programação principal.
- **Flask**: Framework web utilizado para desenvolver a API.
- **Pydantic**: Utilizado para validação e definição de modelos de dados da API.
- **Gemini API**: LLM usada para gerar textos sobre as promoções.
- **MongoDB**: Banco de dados para armazenar informações dos administradores e promoções.
- **Shopee API**: Utilizada para buscar promoções com base em critérios definidos.
- **Telegram Bot API**: Integração para comunicação com os administradores e para publicação das promoções no canal.

## Fluxo do Processo

### 1. Listar Promoções
- **Requisição:** `GET /sales`
- A rota busca promoções utilizando a API da Shopee e aplica validações (confiabilidade e descontos). Os produtos encontrados são inseridos no banco de dados para evitar duplicidade. O produto só é reprocessado se houver uma nova promoção após um período.

![Imagem do fluxo de Listar Promoções](https://github.com/emmanuel-oliveira/Comprinhas-API/blob/main/.github/images/salesFlow.png)

### 2. Gerar Texto para Promoções
- **Requisição:** `POST /sales/generate/text`
- Promoções sem texto são listadas e enviadas para a Gemini API. A API gera uma descrição baseada em um prompt predefinido, e o texto gerado é armazenado no banco de dados.

![Imagem do fluxo de Geração de Texto](https://github.com/emmanuel-oliveira/Comprinhas-API/blob/main/.github/images/generateTextFlow.png)

### 3. Enviar Promoções para Aprovação
- **Requisição:** `POST /sales/send/admins`
- Promoções que ainda não foram enviadas para aprovação são listadas e enviadas para os administradores via Telegram. Cada administrador recebe uma mensagem com opções para aprovar, negar ou refazer o texto.

![Imagem do fluxo de Envio para Aprovação](https://github.com/emmanuel-oliveira/Comprinhas-API/blob/main/.github/images/sendApproveFlow.png)

### 4. Aprovação e Publicação de Promoções
- Os administradores interagem com a mensagem enviada via Telegram:
  - **Negar**: A promoção é registrada como reprovada no banco de dados.
  - **Refazer Texto**: O Gemini API gera um novo texto e o processo de aprovação é reiniciado.
  - **Aprovar**: A promoção é publicada no canal de promoções.

![Imagem do fluxo de Aprovação e Publicação](https://github.com/emmanuel-oliveira/Comprinhas-API/blob/main/.github/images/approveFlow.png)

## Vídeo Demonstrativo

[Vídeo demonstrativo](https://github.com/emmanuel-oliveira/Comprinhas-API/blob/main/.github/videos/videoDemo.mp4)


