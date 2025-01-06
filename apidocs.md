## Survey backend api

 ---
 ### JWT errors
headers:
```Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxNCwiaWF0IjoxNzM2MTQ4ODE2LCJleHAiOjE3MzY0MDgwMTZ9.vkGdIi99Tgmn-R-vaFGjy-_Lvs_eptVl0urXD_eYj64```


---
### User
POST /surveys/api/login/ вход
```
{
    "username": text,
    "password": text,
}
```
response: **200_OK**
```
{
    "id": 15,
    "username": "000000",
    "email": null,
    "admin": false,
    "answered_surveys": [],
    "created_surveys": [],
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxNSwiaWF0IjoxNzM2MTUzNjU5LCJleHAiOjE3MzY0MTI4NTl9.LsiPKbCKdbzFocsJkFD1EkNNrMpmstopGGuBfNCs2_8"
}
```
error: **400_BAD_REQUEST**
```
{
   "error": "Invalid password"
}
```
error: **404_NOT_FOUND**
```
{
   "error": "Invalid username"
}
```
POST /surveys/api/users/  создание пользователя
```
{
    "email": text,
    "username": text,
    "password": text,
}
```
response: **201_CREATED**
```
{
    "id": 15,
    "username": "000000",
    "email": null,
    "admin": false,
    "answered_surveys": [],
    "created_surveys": [],
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxNSwiaWF0IjoxNzM2MTUzNjU5LCJleHAiOjE3MzY0MTI4NTl9.LsiPKbCKdbzFocsJkFD1EkNNrMpmstopGGuBfNCs2_8"
}
```
error: **400_BAD_REQUEST**
```
{
    "error": "Username is not available"
}
```
GET PUT DELETE '/surveys/api/users/<int:pk>/

response: **200_OK**
```
{
    "message": "User deleted successfully"
}
```
error: **404_NOT_FOUND**
```
{
    "error": "User not found"
}
```
PUT response:  **200_OK**
```
{
    "id": 7,
    "username": "justuser",
    "email": null,
    "admin": false,
    "answered_surveys": [],
    "created_surveys": []
}
```
error: **400_BAD_REQUEST**
```
{
    "error": "Username is not available"
}
```
GET  /surveys/api/users/all/ Получение всех пользователей
GET /surveysapi/users/survey/<int:pk>/  Получение администраторов опроса по ID 
error: **404_NOT_FOUND**
```
{
    "message": "No administrators found for this survey."
}
```

---
### Survey
_Error: **400_BAD_REQUEST**_ _error with time_
```
{
    "error_end_date": [
        "The end date must be later than the start date."
    ]
    "error_start_date": [
        "The start date cannot be in the past."
    ]
}
```

POST /surveys/api/surveys/ - Create a survey

Request Body:
```
{
    "title": "О",
    "description": "?",
    "start_date": "2025-12-25",
    "end_date": "2026-01-31",
    "activity": true,
    "admins": [7] 
}
```
Response: **201_CREATED**
```
{
    "id": 26,
    "title": "О",
    "description": "Как т?",
    "start_date": "2025-12-25",
    "end_date": "2026-01-31",
    "admins": [
        7
    ],
    "number_of_respondents": 0
}
```
GET DELETE PUT /surveys/api/surveys/<int:pk>/
Request Body:
```
{
    "title": "Опрос о качествах продукта",
    "description": "Как вы оцениваете наш продукт?",
    "start_date": "2025-01-03",
    "end_date": "2025-01-31",
    "admins": [2, 5],
}
```
Response: **200_OK**
```
{
    "id": 6,
    "title": "-",
    "description": "Как вы оцениваете наш продукт?",
    "start_date": "2025-01-06",
    "end_date": "2025-01-31",
    "admins": [
        2,
        5
    ],
    "number_of_respondents": 2
}
```
```
{
    "message": "Survey deleted successfully"
}
```
Error: **404_NOT_FOUND**
```
{
    "error": "Survey not found"
}
```
GET /surveys/api/surveys/all/ возвращение всех опросов

GET /surveys/api/surveys/user/5/ возвращение всех опросов созданных определенным пользователем

GET /surveys/api/surveys/all/?search=test поиск по title description username 

error: **404_NOT_FOUND**
```
{
    "message": "No surveys found for this user."
    "message": "No surveys match the search criteria."
}
```
---
### Questions
POST /surveys/api/questions/ - Create a question

Request Body:
```
{
    "survey": 1,
    "text": "What is your favorite color?"
}
```
Response: **201_CREATED**
```
{
    "id": 1,
    "survey": 1,
    "text": "What is your favorite color?"
}
```
Error: **400_BAD_REQUEST**
```
{
    "error": "Survey not found"
}
```
GET PUT DELETE /surveys/api/questions/<int:pk>/ 

Request Body:
```
{
    "survey": 1,
    "text": "What is your favorite color?"
}
```
Response: **200_OK**
```
{
    "id": 1,
    "survey": 1,
    "text": "What is your favorite color?"
}
```
```
{
    "message": "Question deleted successfully"
}
```
Error: **404_NOT_FOUND**
```
{
    "error": "Question not found"
}
```
**400_BAD_REQUEST**
```
{
    "error": "Survey not found"
}
```

GET /surveys/api/questions/survey/<int:pk>/ Все вопросы опроса

Response: **200_OK**
```
[
    {
        "id": 2,
        "survey": 6,
        "text": "What?"
    },
    {
        "id": 10,
        "survey": 6,
        "text": "?"
    }
]
```
Error: **404_NOT_FOUND**
```
{
    "error": "Survey not found."
}
```

---

### Options
POST /surveys/api/options/ - Create an option

Request Body:
```
{
    "question": 1,
    "text": "Blue"
}
```
Response: **201_CREATED**
```
{
    "id": 12,
    "question": 2,
    "text": "yes",
    "selected_count": 0
}
```
Error: **400_BAD_REQUEST**
```
{
    "error": "Question not found"
}
```
GET PUT DELETE /surveys/api/options/<int:pk>/ 

Request Body:
```
{
    "question": 20,
    "text": "grey"
}
```
Response: **200_OK**
```
{
    "id": 10,
    "question": 2,
    "text": "grey",
    "selected_count": 2"
}
```
```
{
    "message": "Option deleted successfully"
}
```
Error: **404_NOT_FOUND**
```
{
    "error": "Option not found"
}
```
Error: **400_BAD_REQUEST**
```
{
    "error": "Invalid data provided"
}
```
GET /surveys/api/options/question/11/ все варианты ответов вопроса

Error: **404_NOT_FOUND**
```
{
    "error": "Question not found"
}
```
---
### Answer

POST /surveys/api/answer/?user=2&survey=6  сохранить все ответы данного пользователя на опрос

Request Body:
```
[
    {"question": 1, "options": [3]},
    {"question": 2, "options": [10, 2]}
   
]
```
Response: **200_OK**
```
{
    "message": "Answers successfully created."
}
```
Errors: **400_BAD_REQUEST**
```
{
    "error": "User and Survey are required in query parameters"
}
```
```
{
    "error": "Answers are missing for some questions."
}
```
**404_NOT_FOUND**
```
{
    "error": "Not found user or survey"
}
```
DELETE /surveys/api/answer/?user=2&survey=6 все ответы данного пользователя на данный опрос

Response: **200_OK**
```
{
    "message": "Deleted {count} answers."
}
```