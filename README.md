# HTTP-TRANSLATER

С помощью данного переводчика вы можете перевести слово или предложение путем отправки запроса на сервер и получить ответ. Также можно получить список поддерживаемых языков, установить язык для перевода по умолчанию или  указать его самостоятельно. Ниже приведены запросы и их описание более детально.


## 1)Запрос на получение доступных языков

Request:

	Method: Get
		Path: /api/v1/available_languages

	Response:
		HTTP Code 200
		Headers: Content-type: json
		Body{“error”:False, “languages”:[“ru”,”en”]

	Errors:
		HTTP  Code 500 -внутренние ошибки сервера
		Headers: Content-type: json
		Body{“error”:True,”description”:”Error-description”}

## 2) Запрос для перевода текста на выбранный язык.

Запрос для перевода текста на выбранный язык. Исходный язык текста должен определяться автоматически. Выбранный язык может отсутствовать, если до этого был выбран язык по умолчанию (см "3)"), но если указан – перевести на него.

Request:

	Method: Post
		Path: /api/v1/translate
		Headers: Content-type: json
		Body: {“text”:”Hello world”, “to_lang”:”ru”}	

	Response:
		Headers: Content-type: json
	HTTP Code 200
		Body: {“error”:False, “result”:”Привет  мир”}

Errors:

	HTTP  Code 400 – ошибка в пользовательских данных
		Headers: Content-type: json
		Body: {“error”:True, “description”:”Error description”
		
	HTTP Code 500 -внутренние  ошибки  сервера
		Headers: Content-type: json
		Body: {“error”:True,”description”:”Error-description”}
## 3) Запрос для установки языка по умолчанию для перевода текста
Язык по умолчанию не должен быть установлен при старте программы. Если поле “Unset” указано в True, то необходимо перестать использовать язык по умолчанию.
Request:

	Method: Post
		Path: /api/v1/default_language
		Headers: Content-type: json
		Body: { “Unset”:False,“lang”:”ru”}
	Response:
		Headers: Content-type: json
	HTTP Code 200
		Body: { “error”:False}
Errors:

	HTTP Code 400 – ошибка  в  пользовательских  данных
		Headers: Content-type: json
		Body:{“error”:True, “description”:”Error description”
		
	HTTP Code 500 -внутренние  ошибки  сервера
		Headers: Content-type: json
		Body:{“error”:True,”description”:”Error-description”}

## 4) Запрос для получения языка по умолчанию

Request:

	Method: GET
		Path: /api/v1/default_language
	Response:
		Headers: Content-type: json
		
	HTTP Code 200
		Body:{ “error”:False,”lang”:”ru”}

Errors:

	HTTP  Code 400 – ошибка в пользовательских данных
		Headers: Content-type: json
		Body:{“error”:True, “description”:”Error description”
			
	HTTP Code 500 -внутренние  ошибки  сервера
		Headers: Content-type: json
		Body;{“error”:True,”description”:”Error-description”}
