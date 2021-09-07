## For system administrator

To use API need send Token in header with key *Authorization*

To get Token need GET-request to link /auth/jwt/create/ with username and password of admin

### Create survey

POST-request to link: /v1/survey/

```
{
    "title": "Title of survey",
    "start_date": "2021-09-04",
    "end_date": "2021-09-05",
    "description": "Description of survey"
}
```

at */v1/survey/{id}* is also available

- *CRUD operations*

### To get all surveys

GET-request to link: /v1/survey/

```
[
    {
        "id": 1,
        "title": "Title of survey",
        "start_date": "2021-09-04",
        "end_date": "2021-09-05",
        "description": "Description of survey"
    },
    ...
]
```

### To get detail information of survey

GET-request to link: /v1/survey/{id}/ question of survey has 3 types:

- 0 - TEXT
- 1 - MULTI_CHOICE
- 2 - CHOICE

```
{
    "id": 1,
    "title": "Title of survey",
    "start_date": "2021-09-04",
    "end_date": "2021-09-05",
    "description": "Description of survey",
    "questions": [
        {
            "id": 1,
            "type": 0,
            "text": "question of survey",
            "choices": []
        },
        {
            "id": 2,
            "type": 1,
            "text": "question of survey 2",
            "choices": [
                {
                    "id": 1,
                    "text": "choice of question"
                },
                {
                    "id": 2,
                    "text": "choice of question 2"
                },
                {
                    "id": 3,
                    "text": "choice of question 3"
                }
            ]
        },
        ...
    ]
}
```

### Create question of created survey

POST-request to link: /v1/survey/{survey_id}/questions/

```
{
    "type": 3,
    "text": "question of survey",
    "choices": [
        {
            "text": "choice 1"
        },
        {
            "text": "choice 2"
        },
        {
            "text": "choice 3"
        }
    ]
}
```

at */v1/survey/{survey_id}/questions/{id}*

- *CRUD operations of questions*

### Choices

*get list of choices of question /v1/survey/{survey_id}/questions/<question_id>/choices/*

*at /v1/survey/{survey_id}/questions/<question_id>/choices/<choice_id>/*

- *CRUD operations of choices*

## For user

### To get active surveys

GET-request to link: /v1/user/survey/

```
[
    {
        "id": 1,
        "title": "Title of survey",
        "description": "Description of survey"
        ...
    },
    ...
]
```

### Detail information of survey for user

GET-request to link: /v1/user/survey/{id}/

```
{
{
    "id": 1,
    "title": "Title of survey",
    "start_date": "2021-09-04",
    "end_date": "2021-09-05",
    "description": "Description of survey",
    "questions": [
        {
            "id": 1,
            "type": 0,
            "text": "question of survey",
            "choices": []
        },
        {
            "id": 2,
            "type": 1,
            "text": "question of survey 2",
            "choices": [
                {
                    "id": 1,
                    "text": "choice of question"
                },
                {
                    "id": 2,
                    "text": "choice of question 2"
                },
                {
                    "id": 3,
                    "text": "choice of question 3"
                }
            ]
        },
        ...
    ]
}
```

### Save user's vote

POST-request to link: /v1/user/vote/

```
{
    "survey": <survey_id>,
    "answers": [
        {
            "question": <question_id>,
            "text": "text answer"
        },
        {
            "question": <question_id>,
            "choice_id": [<choice_id>,<choice_id>]
        },
        {
            "question": <question_id>,
            "choice_id": [<choice_id>]
        },
        ...
    ]
}
```

### Detail information of user's votes

GET-request to link: /v1/user/{user_id}/

```
[
    {
        "id": <id_vote>,
        "id_user": <id_user>,
        "survey": "title of survey",
        "created": "2021-09-04",
        "answers": [
            {
                "id": "<id_answer>",
                "question": "text question",
                "choice": [],
                "value": "answer text"
            },
            {
                "question": "MULTI_CHOICE question",
                "choice": [
                   {
                    "id": 17,
                    "text": "2 choice for multi choice question"
                  },
                  {
                    "id": 19,
                    "text": "4 choice for multi choice question"
                  }
                ],
                "value": null
            },
            {
                "id": "<id_answer>",
                "question": "CHOICE question text",
                "choice": [
                    "id": 19,
                    "text": "4 choice for multi choice question"
                ],
                "value": null
            },
            ...
        ]
    }
]
```

### To get vote by ID and user ID

GET-request to link: /v1/user/{user_id}/{id}/

```
{
    "id": <id_vote>,
    "id_user": <id_user>,
    "survey": "title of survey",
    "created": "2021-09-04",
    "answers": [
        {
            "id": "<id_answer>",
            "question": "text question",
            "choice": [],
            "value": "answer text"
        },
        {
            "question": "MULTI_CHOICE question",
            "choice": [
               {
                "id": 17,
                "text": "2 choice for multi choice question"
              },
              {
                "id": 19,
                "text": "4 choice for multi choice question"
              }
            ],
            "value": null
        },
        {
            "id": "<id_answer>",
            "question": "CHOICE question text",
            "choice": [
                "id": 19,
                "text": "4 choice for multi choice question"
            ],
            "value": null
        },
        ...
    ]
}
```

### Choice's operations

at link: /v1/survey/{survey_id}/questions/{questions_id}/choice/{id}/

- CRUD operations of Choices
