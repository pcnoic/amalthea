# Amalthea Minimal API Documentation 
## Persephone

The authentication and user management system of Amalthea is called _Persephone_ and is re-usable.

### Register in Persephone

To register in Persephone you have to make the following `POST` request:

**REQUEST**

```curl
curl --location --request POST 'http://<domain>:<port>/auth/register/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "email":"email@email.com",
    "password":"password",
    "username":"email"
}'
```

**RESPONSE**
```json
{
    "id": "2ab355fd-798c-4378-b4ed-a8be96e8fcd2",
    "email": "email@email.com",
    "is_active": true,
    "is_superuser": false,
    "is_verified": false,
    "username": "email"
}
```

Note: the `username` should be the same as the one you have in Wikipedia, so that the identity of the user can be verified in both platforms. This is because Mediawiki does not have an easy way to allow someone to "login with Wikipedia". 

### Login in Persephone

To login in Persephone you have to make the following `POST` request:


**REQUEST**

```curl
curl --location --request POST 'http://<domain>:<port>/auth/jwt/login' \
--form 'username="email@email.com"' \
--form 'password="email"'
```

**RESPONSE**

```curl
{
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiMmFiMzU1ZmQtNzk4Yy00Mzc4LWI0ZWQtYThiZTk2ZThmY2QyIiwiYXVkIjoiZmFzdGFwaS11c2VyczphdXRoIiwiZXhwIjoxNjI1MTc1OTE5fQ.O2x8mDO_MQ0S5U_jk-AExZ-McEUgcaVQpBVa65RyiUs",
    "token_type": "bearer"
}
```

You will received the following response, if the credentials you have provided are valid. You can use the `access_token` to perform requests to endpoints requiring authentication. 

You will have to use the `access_token` as a `Bearer token` and dispatch it with every request. 

### Refresh your access token

TODO

### Fetch your Wikipedia ID

Unfortunately there is no authentication backend in Mediawiki (the Wikipedia CMS) API to use as an Oauth provider for logging into Amalthea (at the time of writing). So to facilitate user authorization between Amalthea (Persephone) and Wikipedia we had to hack our way into. 

First of all:

**IT IS MANDATORY TO USE THE SAME USERNAME AND EMAIL ADDRESS ON AMALTHEA AND WIKIPEDIA** 

We do not have another way of verifying your identity currently. 

You can grab your Wikipedia ID by sending the following `POST` request.

**REQUEST**

```curl
curl --location --request POST 'http://<domain>:<port>/get-wiki-id' \
--header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiMmFiMzU1ZmQtNzk4Yy00Mzc4LWI0ZWQtYThiZTk2ZThmY2QyIiwiYXVkIjoiZmFzdGFwaS11c2VyczphdXRoIiwiZXhwIjoxNjI1MjYwOTI3fQ.HncwIiLE-5FxOzE6gYl3vJmoPfFiVCxj6NvFSji6jTw' \
--header 'Content-Type: application/json' \
--data-raw '{
    "password":"yourwikipediapassword"
}'
```

**RESPONSE**

```json
{
    "message": "Come to the dark side, we have cookies."
}
```

You will also receive a response header setting the cookie `am_wikiID`. This verifies your identity on Wikipedia.


### Verify your Wikipedia identity

The only way to verify your identity is to allow our application to use your password on Wikipedia to imitate a successful login. 

**We are working on a workaround that won't ask for your Wikipedia password.**

For cross-verifying the identity on Wikipedia and Amalthea send the following `POST` request:

**REQUEST**

```curl
curl --location --request POST 'http://<domain>:<port>/verify' \
--header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiMmFiMzU1ZmQtNzk4Yy00Mzc4LWI0ZWQtYThiZTk2ZThmY2QyIiwiYXVkIjoiZmFzdGFwaS11c2VyczphdXRoIiwiZXhwIjoxNjI1MjYwOTI3fQ.HncwIiLE-5FxOzE6gYl3vJmoPfFiVCxj6NvFSji6jTw' \
--header 'Cookie: am_wikiID="Pcnoic\07319c37effe0c7001b5008af26f770120a5030f5112b299bb65a6b917a5f4342bf"'
```

**RESPONSE** on **success**

```json
{
    "message": "successful"
}
```

**RESPONSE** on **failure**

```json
{
    "message":"failed"
}
```

**RESPONSE** on **missing cookie**

```json
{
    "message":"cookie is missing"
}
```

### Search articles with keyword

You can search for a specific article on Wikipedia by sending a `GET` request to Amalthea (Hermes) which will fetch you the related articles.

**REQUEST**

```curl
curl --location --request GET 'http://<domain>:<port>/articles/<keyword>/get' \
--header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiMmFiMzU1ZmQtNzk4Yy00Mzc4LWI0ZWQtYThiZTk2ZThmY2QyIiwiYXVkIjoiZmFzdGFwaS11c2VyczphdXRoIiwiZXhwIjoxNjI1MjYwOTI3fQ.HncwIiLE-5FxOzE6gYl3vJmoPfFiVCxj6NvFSji6jTw' 
```

For example, we used the keyword `sfelinos` (a village in Greece) and we got:

**RESPONSE**

```json
{
    "results": [
        {
            "ns": 0,
            "title": "Sfelinos",
            "pageid": 61726762,
            "size": 3460,
            "wordcount": 258,
            "snippet": "<span class=\"searchmatch\">Sfelinos</span> (Greek: Σφελινός) is a village in the region of Serres, northern Greece. According to the 2011 Greek census, the village had 304 inhabitants.",
            "timestamp": "2021-06-30T19:01:32Z"
        },
        {
            "ns": 0,
            "title": "List of settlements in the Serres regional unit",
            "pageid": 1806820,
            "size": 3833,
            "wordcount": 201,
            "snippet": "Pontismeno Promachonas Proti Provatas Psychiko Rodolivos Rodopoli Serres <span class=\"searchmatch\">Sfelinos</span> Sidirokastro Sisamia Sitochori Skopia Skotoussa Skoutari Stathmos Angistis",
            "timestamp": "2019-05-25T16:16:41Z"
        }
    ]
}
```

### Fetch n revisions of certain article

You can request to fetch `n` amount of revisions for a specific article. The amount of revisions is defined in `ConfigParams.MAX_WIKIPEDIA_REV`. You will also **only** received the revisions you've authored with your verified Wikipedia ID. 

Send a `GET` request:

```curl
curl --location --request GET 'http://<domain>:<port>/articles/revisions/61726762/get' \
--header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiMmFiMzU1ZmQtNzk4Yy00Mzc4LWI0ZWQtYThiZTk2ZThmY2QyIiwiYXVkIjoiZmFzdGFwaS11c2VyczphdXRoIiwiZXhwIjoxNjI1MjYwOTI3fQ.HncwIiLE-5FxOzE6gYl3vJmoPfFiVCxj6NvFSji6jTw'
```

For the user `Pcnoic` we received the following response:

```json
{
    "results": [
        {
            "revid": 1031279100,
            "parentid": 914649157,
            "user": "Pcnoic",
            "timestamp": "2021-06-30T19:01:32Z"
        }
    ]
}
```

Expect similar responses for every user and every article. 

### Fetch the content of a certain revision

You can fetch the content of a specific revision that you've authored by performing the following `GET` request. 


**REQUEST**

```curl
curl --location --request GET 'http://<domain>:<port>/articles/revisions/content/<revid>/get' \
--header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiMmFiMzU1ZmQtNzk4Yy00Mzc4LWI0ZWQtYThiZTk2ZThmY2QyIiwiYXVkIjoiZmFzdGFwaS11c2VyczphdXRoIiwiZXhwIjoxNjI1MjYwOTI3fQ.HncwIiLE-5FxOzE6gYl3vJmoPfFiVCxj6NvFSji6jTw'
```

**RESPONSE**

TODO
