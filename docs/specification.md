# Specifications

Here you will find all the endpoints to handle resources.

## **API**

- [Circle API](#circle-api)
- [Resource API](#resource-api)
- [File API](#file-api)

## **Circle API**

The circle API allows you to manage circles.

 ### **Endpoints**

`POST` *{baseUrl}/api/circles/*

 Create new circle.

 ---


`GET` *{baseUrl}/api/circles/*

 Get all circles.

 ---


`GET` *{baseUrl}/api/circles/\<int:pk/*

 *Get one circle*

 ---

`PATCH` *{baseUrl}/api/circles/\<int:pk/*

 *Update circle*

 ---

 `POST` *{baseUrl}/api/circles/\<int:pk/register/*

Register a current user in circle.

 ---

  `POST` *{baseUrl}/api/circles/\<int:pk/quit/*

 User left a circle.

 ---

  `POST` *{baseUrl}/api/circles/\<int:pk/publish/*

 Publish a circle.

---

`GET` *{baseUrl}/api/circles/\<int:pk/parent/*

 *Get all circle's parent*

 ---
 ---





 ### **`POST`** ***{baseUrl}/api/circles/***
*create new circle*

 ### **Resource URL :**
 ```
 {baseUrl}/api/circles/
 ```

 ### **HTTP headers :**
 TODO

### **Path parameters :**
 This endpoint does not require Path parameters.

 ### **Query parameters :**
 This endpoint does not require Query parameters.

 ### **Request body :**

 Key|Desciption|Example value
 --|--|--
 name|name of the circle
 description|description of the cirle
 parent_id|id of parent circle


 ### **Response :**
 [`201`] Circle created.

 [`400`] Bad request.

 [`404`] Not found.

*Example*

 ```json
 {
    "id" : 123,
    "id_parent" : 0,
    "desciption" : "My first circle",
    "is_publish" : false,
    "created_date" : "2020-09-07",
    "users" : [
       {
           "id" : 12,
           "name" : "...",
       }
   ],
 }
 ```

*Structure (object)*

 Key|Desciption
 --|--
 id|The unique identifier of the circle
 description|Description of the cirle with id `id`
 parent_id|Id of parent circle
 is_publish|True if circle with id `id` is publish, False otherwise
 created_date|Created date in ISO format (YYYY-MM-DD pattern)
 users|List of users registered in the circle with id `id`


---


 ### **`GET`** ***{baseUrl}/api/circles/***
*Get all circles*

 ### **Resource URL :**
 ```
 {baseUrl}/api/circles/
 ```

 ### **HTTP headers :**
 TODO

### **Path parameters :**
 This endpoint does not require Path parameters.

 ### **Query parameters :**
 This endpoint does not require Query parameters.

 ### **Request body :**

 Key|Desciption|Example value
 --|--|--
 name|name of the circle
 description|description of the cirle
 parent_id|id of parent circle


 ### **Response :**
 [`201`] Circle created.

 [`400`] Bad request.

 [`404`] Not found.

*Example*

 ```json
 {
   "circles" : [
        {
           "id" : 123,
           "id_parent" : 0,
           "desciption" : "My first circle",
           "is_publish" : false,
           "created_date" : "2020-09-07",
           "users" : [
               {
                   "id" : 12,
                   "name" : "...",
               }
           ],
       }
   ]
 }
 ```

*Structure (object)*

 Key|Desciption
 --|--
 circles| List of all circles
 id|The unique identifier of the circle
 description|Description of the cirle with id `id`
 parent_id|Id of parent circle
 is_publish|True if circle with id `id` is publish, False otherwise
 created_date|Created date in ISO format (YYYY-MM-DD pattern)
 users|List of users registered in the circle with id `id`


---

 ### **`GET`** ***{baseUrl}/api/circles/\<int:pk/***
*Get a circle*

 ### **Resource URL :**
 ```
 {baseUrl}/api/circles/<int:pk/
 ```

 ### **HTTP headers :**
 TODO

### **Path parameters :**
 This endpoint does not require Path parameters.

 ### **Query parameters :**
 This endpoint does not require Query parameters.

 ### **Request body :**

 Key|Desciption|Example value
 --|--|--
 name|name of the circle
 description|description of the cirle
 parent_id|id of parent circle


 ### **Response :**
 [`201`] Circle created.

 [`400`] Bad request.

 [`404`] Not found.

*Example*

 ```json
 {
    "id" : 123,
    "id_parent" : 0,
    "desciption" : "My first circle",
    "is_publish" : false,
    "created_date" : "2020-09-07",
    "users" : [
       {
           "id" : 12,
           "name" : "...",
       }
   ],
 }
 ```

*Structure (object)*

 Key|Desciption
 --|--
 id|The unique identifier of the circle
 description|Description of the cirle with id `id`
 parent_id|Id of parent circle
 is_publish|True if circle with id `id` is publish, False otherwise
 created_date|Created date in ISO format (YYYY-MM-DD pattern)
 users|List of users registered in the circle with id `id`

---

 ### **`GET`** ***{baseUrl}/api/circles/\<int:pk/***
*Get a circle*

 ### **Resource URL :**

### **Path parameters :**
 This endpoint does not require Path parameters.

 ### **Query parameters :**
 This endpoint does not require Query parameters.

 ### **Request body :**

 Key|Desciption|Example value
 --|--|--
 name|name of the circle
 description|description of the cirle
 parent_id|id of parent circle


 ### **Response :**
 [`201`] Circle created.

 [`400`] Bad request.

 [`404`] Not found.

*Example*

 ```json
 {
    "id" : 123,
    "id_parent" : 0,
    "desciption" : "My first circle",
    "is_publish" : false,
    "created_date" : "2020-09-07",
    "users" : [
       {
           "id" : 12,
           "name" : "...",
       }
   ],
 }
 ```

*Structure (object)*

 Key|Desciption
 --|--
 id|The unique identifier of the circle
 description|Description of the cirle with id `id`
 parent_id|Id of parent circle
 is_publish|True if circle with id `id` is publish, False otherwise
 created_date|Created date in ISO format (YYYY-MM-DD pattern)
 users|List of users registered in the circle with id `id`

---

 ### **`PATCH`** ***{baseUrl}/api/circles/\<int:pk/***
*Update a circle*

 ### **Resource URL :**
 ```
 {baseUrl}/api/circles/<int:pk/
 ```

 ### **HTTP headers :**
 TODO

### **Path parameters :**

 Key|Desciption|Example value
 --|--|--
 pk|id of the circle

 ### **Query parameters :**
 This endpoint does not require Query parameters.

 ### **Request body :**

 You can update theses fields

 Key|Desciption|Example value
 --|--|--
 id|id of the circle


 ### **Response :**
 [`200`] Query request successfully processed. Return updated circle.

 [`400`] Bad request.

 [`404`] Not found.


*Example*

 ```json
 {
    "id" : 123,
    "id_parent" : 0,
    "desciption" : "My first circle",
    "is_publish" : false,
    "created_date" : "2020-09-07",
    "users" : [
       {
           "id" : 12,
           "name" : "...",
       }
   ],
 }
 ```

*Structure (object)*

 Key|Desciption
 --|--
 id|The unique identifier of the circle
 description|Description of the cirle with id `id`
 parent_id|Id of parent circle
 is_publish|True if circle with id `id` is publish, False otherwise
 created_date|Created date in ISO format (YYYY-MM-DD pattern)
 users|List of users registered in the circle with id `id`


---


 ### **`POST`** ***{baseUrl}/api/circles/\<int:pk/quit/***
*User left a circle*

 ### **Resource URL :**
 ```
 {baseUrl}/api/circles/<int:pk/quit/
 ```

 ### **HTTP headers :**
 TODO

### **Path parameters :**
 Key|Desciption|Example value
 --|--|--
 pk|id of the circle

 ### **Query parameters :**
 This endpoint does not require Query parameters.

 ### **Request body :**

 Key|Desciption|Example value
 --|--|--
 id_user|id of user who left of the circle


 ### **Response :**
 [`200`] Query request successfully processed. Return circle is user lefted the circle.

 [`400`] Bad request.

 [`404`] Not found.


*Example*

 ```json
 {
    "id" : 123,
    "id_parent" : 0,
    "desciption" : "My first circle",
    "is_publish" : false,
    "created_date" : "2020-09-07",
    "users" : [
       {
           "id" : 12,
           "name" : "...",
       }
   ],
 }
 ```

*Structure (object)*

 Key|Desciption
 --|--
 id|The unique identifier of the circle
 description|Description of the cirle with id `id`
 parent_id|Id of parent circle
 is_publish|True if circle with id `id` is publish, False otherwise
 created_date|Created date in ISO format (YYYY-MM-DD pattern)
 users|List of users registered in the circle with id `id`


---

### **`POST`** ***{baseUrl}/api/circles/\<int:pk/publish/***
*Publish a circle*

 ### **Resource URL :**
 ```
 {baseUrl}/api/circles/<int:pk/publish/
 ```

 ### **HTTP headers :**
 TODO

### **Path parameters :**
 Key|Desciption|Example value
 --|--|--
 pk|id of the circle

 ### **Query parameters :**
 This endpoint does not require Query parameters.

 ### **Request body :**

 Key|Desciption|Example value
 --|--|--
 id_user|id of user who left of the circle


 ### **Response :**
 [`200`] Query request successfully processed. Return circle if he is published.

 [`400`] Bad request.

 [`404`] Not found.


 *Example*

 ```json
 {
    "id" : 123,
    "id_parent" : 0,
    "desciption" : "My first circle",
    "is_publish" : false,
    "created_date" : "2020-09-07",
    "users" : [
       {
           "id" : 12,
           "name" : "...",
       }
   ],
 }
 ```

*Structure (object)*

 Key|Desciption
 --|--
 id|The unique identifier of the circle
 description|Description of the cirle with id `id`
 parent_id|Id of parent circle
 is_publish|True if circle with id `id` is publish, False otherwise
 created_date|Created date in ISO format (YYYY-MM-DD pattern)
 users|List of users registered in the circle with id `id`

---

### **`GET`** ***{baseUrl}/api/circles/\<int:pk/parent/***
*Publish a circle*

 ### **Resource URL :**
 ```
 {baseUrl}/api/circles/<int:pk/publish/
 ```

 ### **HTTP headers :**
 TODO

### **Path parameters :**
 Key|Desciption|Example value
 --|--|--
 pk|id of the circle

 ### **Query parameters :**
 This endpoint does not require Query parameters.

 ### **Request body :**

 This endpoint does not require request body.

 ### **Response :**
 [`200`] Query request successfully processed

 [`400`] Bad request.

 [`404`] Not found.


 *Example*

 ```json
 {
   "parents" : [0, 2, ...]
 }
 ```

*Structure (object)*

 Key|Desciption
 --|--
 parents|List of id of Circle parent


---
---


## **Resource API**

The resource API allows you to manage resources

 ### **Endpoints**

 `POST` *{baseUrl}/api/circles/\<int:pk/resources/*

 Create resource un circle `pk`.

 ---

 `GET` *{baseUrl}/api/circles/\<int:pk/resources/*

 Get all resources in circle `pk`.

 ---

 `GET` *{baseUrl}/api/circles/\<int:pk/resources/\<int:pkr/*

  Get current resource `pkr` in circle `pk`.

 ---

  `PATCH` *{baseUrl}/api/circles/\<int:pk/resources/\<int:pkr/*

  Update current resource `pkr` in circle `pk`.

 ---

  `POST` *{baseUrl}/api/circles/\<int:pk/resources/\<int:pkr/versions/*

  Create new version of resource `pkr` in circle `pk`.

 ---

   `GET` *{baseUrl}/api/circles/\<int:pk/resources/\<int:pkr/versions/*

  Get all versions of resource `pkr` in circle `pk`.

 ---

   `GET` *{baseUrl}/api/circles/\<int:pk/resources/\<int:pkr/versions/\<int:pkv/*

  Get resource `pkr` and version `pkv` in circle `pk`.

 ---

   `PATCH` *{baseUrl}/api/circles/\<int:pk/resources/\<int:pkr/versions/\<int:pkv/*

  Update version `pkv` of resource `pkr` in circle `pk`.

 ---

### **`POST`** ***{baseUrl}/api/circles/\<int:pk/resources/***
*Create a resource*

 ### **Resource URL :**
 ```
 {baseUrl}/api/circles/<int:pk/resources/
 ```

 ### **HTTP headers :**
 TODO

### **Path parameters :**
 Key|Desciption|Example value
 --|--|--
 pk|id of the circle|1

 ### **Query parameters :**
 This endpoint does not require Query parameters.

 ### **Request body :**

 Key|Desciption|Example value
 --|--|--
 name|name of resource|my_resource
 directory|name of directory (can be empty)|my_directory


 ### **Response :**
 [`201`] Resource successfully created.

 [`400`] Bad request.

 [`404`] Not found.


 *Example*

 ```json
 {
    "id" : 13,
    "name" : "my_resource",
    "directory" : "my_directory",
    "creator" : 
       {
           "id" : 18,
           "name" : "...",
       },
   "created_date" : "2021-02-08",
 }
 ```

*Structure (object)*

 Key|Desciption
 --|--
 id|The unique identifier of the resource
 name|Name of the resource
 directory|Directory of the resource in circle
 creator|User who create the resource
 created_date|Created date in ISO format (YYYY-MM-DD pattern)


---


### **`GET`** ***{baseUrl}/api/circles/\<int:pk/resources/***
*Get all resources in the circle with id `pk`*

 ### **Resource URL :**
 ```
 {baseUrl}/api/circles/<int:pk/resources/
 ```

 ### **HTTP headers :**
 TODO

### **Path parameters :**
 Key|Desciption|Example value
 --|--|--
 pk|id of the circle|1

 ### **Query parameters :**
 This endpoint does not require query parameters.

 ### **Request body :**

 This endpoint does not require request body.


 ### **Response :**
 [`200`] Query request successfully processed. 

 [`400`] Bad request.

 [`404`] Not found.


 *Example*

 ```json
 {
   "resources": [
        {
           "id" : 13,
           "name" : "my_resource",
           "directory" : "my_directory",
           "creator" : 
               {
               "id" : 8,
               "name" : "...",
               },
           "created_date" : "2021-02-08",
       }
   ]    
 }
 ```

*Structure (object)*

 Key|Desciption
 --|--
 resources|List of all resource in a circle
 id|The unique identifier of the resource
 name|Name of the resource
 directory|Directory of the resource in circle
 creator|User who create the resource
 created_date|Created date in ISO format (YYYY-MM-DD pattern)

---


### **`GET`** ***{baseUrl}/api/circles/\<int:pk/resources/\<int:pkr***
*Get resource with id `pkr` in the circle with id `pk`*

 ### **Resource URL :**
 ```
 {baseUrl}/api/circles/<int:pk/resources/<int:pkr
 ```

 ### **HTTP headers :**
 TODO

### **Path parameters :**
 Key|Desciption|Example value
 --|--|--
 pk|id of the circle|1

 ### **Query parameters :**
 This endpoint does not require query parameters.

 ### **Request body :**

 This endpoint does not require request body.


 ### **Response :**
 [`200`] Query request successfully processed. 

 [`400`] Bad request.

 [`404`] Not found.


 *Example*

 ```json
 {
    "id" : 13,
    "name" : "my_resource",
    "directory" : "my_directory",
    "creator" : 
       {
           "id" : 18,
           "name" : "...",
       },
   "created_date" : "2021-02-08",
 }
 ```

 *Structure (object)*

 Key|Desciption
 --|--
 resources|List of all resource in a circle
 id|The unique identifier of the resource
 name|Name of the resource
 directory|Directory of the resource in circle
 creator|User who create the resource
 created_date|Created date in ISO format (YYYY-MM-DD pattern)

---

### **`PATCH`** ***{baseUrl}/api/circles/\<int:pk/resources/\<int:pkr/***
*Update resource with id `pkr` in the circle with id `pk`*

 ### **Resource URL :**
 ```
 {baseUrl}/api/circles/<int:pk/resources/<int:pkr
```

 ### **HTTP headers :**
 TODO

### **Path parameters :**
 Key|Desciption|Example value
 --|--|--
 pk|id of the circle|1
 pkr|id of the resource|1

 ### **Query parameters :**

 This endpoint does not require query parameters.

 ### **Request body :**

 You can update theses fields

 Key|Desciption|Example value
 --|--|--
 name|name of resource|my_resource
 directory|name of directory (can be empty)|my_directory

 ### **Response :**

 [`200`] Query request successfully processed. 

 [`400`] Bad request.

 [`404`] Not found.


 *Example*

 ```json
 {
    "id" : 13,
    "name" : "my_resource",
    "directory" : "my_directory",
    "creator" : 
       {
           "id" : 18,
           "name" : "...",
       },
   "created_date" : "2021-02-08",
 }
 ```

 *Structure (object)*

 Key|Desciption
 --|--
 id|The unique identifier of the resource
 name|Name of the resource
 directory|Directory of the resource in circle
 creator|User who create the resource
 created_date|Created date in ISO format (YYYY-MM-DD pattern)

---

### **`POST`** ***{baseUrl}/api/circles/\<int:pk/resources/\<int:pkr/versions/***
*Create a version of resource `pkr` in the circle with id `pk`*

 ### **Resource URL :**
 ```text
 {baseUrl}/api/circles/<int:pk/resources/<int:pkr/versions/
 ```

 ### **HTTP headers :**
 TODO

### **Path parameters :**
 Key|Desciption|Example value
 --|--|--
 pk|id of the circle|1
 pkr|id of the resource|1

 ### **Query parameters :**

 This endpoint does not require query parameters.

 ### **Request body :**

 Key|Desciption|Example value
 --|--|--
 tags|List of tags | TODO
 description| Version's description of resource

 ### **Response :**

 [`201`] New version of resource is created. 

 [`400`] Bad request.

 [`404`] Not found.


 *Example*

 ```json
 {
    "id" : 13,
    "name" : "my_resource",
    "directory" : "my_directory",
    "creator" : 
       {
           "id" : 18,
           "name" : "...",
       },
   "created_date" : "2021-02-08",
   "description" : "Use this version for ...",
   "tags" : ["tag1", "Python", ...],
   "version" : 0,
 }
 ```

 *Structure (object)*

 Key|Desciption
 --|--
 id|The unique identifier of the resource
 name|Name of the resource
 directory|Directory of the resource in circle
 creator|User who create the resource
 created_date|Created date in ISO format (YYYY-MM-DD pattern)
 description|Description of this version of resource
 tags|List of tags
 version| version of this resource


---

### **`GET`** ***{baseUrl}/api/circles/\<int:pk/resources/\<int:pkr/versions/***
*Get all versions of resource `pkr` in the circle with id `pk`*

 ### **Resource URL :**
 ```text
 {baseUrl}/api/circles/<int:pk/resources/<int:pkr/versions/
 ```

 ### **HTTP headers :**
 TODO

### **Path parameters :**
 Key|Desciption|Example value
 --|--|--
 pk|id of the circle|1
 pkr|id of the resource|1

 ### **Query parameters :**

 This endpoint does not require query parameters.

 ### **Request body :**

 Key|Desciption|Example value
 --|--|--
 tags|List of tags | TODO
 description| Version's description of resource

 ### **Response :**

 [`200`] Query request successfully processed. 

 [`400`] Bad request.

 [`404`] Not found.


 *Example*

 ```json
 {
    "versions" : [
       {   
           "id" : 13,
           "name" : "my_resource",
           "directory" : "my_directory",
           "creator" : 
               {
                   "id" : 18,
                   "name" : "...",
               },
           "created_date" : "2021-02-08",
           "description" : "Use this version for ...",
           "tags" : ["tag1", "Python", ...],
           "version" : 0,
       }
    ]
 }
 ```

 *Structure (object)*

 Key|Desciption
 --|--
 versions|List of version for a given resource 
 id|The unique identifier of the resource's version
 name|Name of the resource
 directory|Directory of the resource in circle
 creator|User who create the resource
 created_date|Created date in ISO format (YYYY-MM-DD pattern)
 description|Description of this version of resource
 tags|List of tags
 version| version of this resource

---

### **`GET`** ***{baseUrl}/api/circles/\<int:pk/resources/\<int:pkr/versions/\<int:pkv/***
*Get a version `pkv` of resource `pkr` in the circle with id `pk`*

 ### **Resource URL :**
 ```text
 {baseUrl}/api/circles/<int:pk/resources/<int:pkr/versions/<int:pkv/
 ```

 ### **HTTP headers :**
 TODO

### **Path parameters :**
 Key|Desciption|Example value
 --|--|--
 pk|id of the circle|1
 pkr|id of the resource|1
 pkv|id of the version|0


 ### **Query parameters :**

 This endpoint does not require query parameters.

 ### **Request body :**

 This endpoint does not require request body.

 ### **Response :**

 [`200`] Query request successfully processed. 

 [`400`] Bad request.

 [`404`] Not found.


 *Example*

 ```json
 {
    "id" : 13,
    "name" : "my_resource",
    "directory" : "my_directory",
    "creator" : 
       {
           "id" : 18,
           "name" : "...",
       },
   "created_date" : "2021-02-08",
   "description" : "Use this version for ...",
   "tags" : ["tag1", "Python", ...],
   "version" : 0,
 }
 ```

 *Structure (object)*

 Key|Desciption
 --|--
 id|The unique identifier of the version of resource
 name|Name of the resource
 directory|Directory of the resource in circle
 creator|User who create the resource
 created_date|Created date in ISO format (YYYY-MM-DD pattern)
 description|Description of this version of resource
 tags|List of tags
 version| version of this resource

---

### **`PATCH`** ***{baseUrl}/api/circles/\<int:pk/resources/\<int:pkr/versions/\<int:pkv/***
*Update a version `pkv` of resource `pkr` in the circle with id `pk`*

 ### **Resource URL :**
 ```text
 {baseUrl}/api/circles/<int:pk/resources/<int:pkr/versions/<int:pkv/
 ```

 ### **HTTP headers :**
 TODO

### **Path parameters :**
 Key|Desciption|Example value
 --|--|--
 pk|id of the circle|2
 pkr|id of the resource|1
 pkv|id of the version|0

 ### **Query parameters :**

 This endpoint does not require query parameters.

 ### **Request body :**

 You can update theses fields

 Key|Desciption|Example value
 --|--|--
 status|Status of resource | TESTED
 tags|List of tags | TODO
 description| Version's description of resource

 ### **Response :**

 [`200`] Query request successfully processed. 

 [`400`] Bad request.

 [`404`] Not found.


 *Example*

 ```json
 {
    "id" : 13,
    "name" : "my_resource",
    "directory" : "my_directory",
    "creator" : 
       {
           "id" : 18,
           "name" : "...",
       },
   "created_date" : "2021-02-08",
   "description" : "Use this version for ...",
   "tags" : ["tag1", "Python", ...],
   "version" : 0,
 }
 ```

 *Structure (object)*

 Key|Desciption
 --|--
 id|The unique identifier of the version of resource
 name|Name of the resource
 directory|Directory of the resource in circle
 creator|User who create the resource
 created_date|Created date in ISO format (YYYY-MM-DD pattern)
 description|Description of this version of resource
 tags|List of tags
 version| version of this resource

---
---

## **File API**

The file API allows you to manage File of resources


`POST` *{baseUrl}/api/circles/\<int:pk/resources/\<int:pkr/versions/\<int:pkv/files/*

Create new file in resource `pkr` and version `pkv` in circle `pk`.

---

`GET` *{baseUrl}/api/circles/\<int:pk/resources/\<int:pkr/versions/\<int:pkv/files/*

  Get all files of version `pkv` of resource `pkr` in circle `pk`.

---

`GET` *{baseUrl}/api/circles/\<int:pk/resources/\<int:pkr/versions/\<int:pkv/files/\<int:pkf/*

Get file `pkf` in resource `pkr` and version `pkv` in circle `pk`.

 ---

`PUT` *{baseUrl}/api/circles/\<int:pk/resources/\<int:pkr/versions/\<int:pkv/files/\<int:pkf/*

  Update `pkf` files of version `pkv` of resource `pkr` in circle `pk`.

---


### **`POST`** ***{baseUrl}/api/circles/\<int:pk/resources/\<int:pkr/versions/\<int:pkv/files/***
*Create a new file in version `pkv` of resource `pkr` in the circle with id `pk`*

 ### **Resource URL :**
 ```text
 {baseUrl}/api/circles/\<int:pk/resources/\<int:pkr/versions/\<int:pkv/files/
 ```

 ### **HTTP headers :**
 TODO

### **Path parameters :**
 Key|Desciption|Example value
 --|--|--
 pk|id of the circle|3
 pkr|id of the resource|0
 pkv|id of the resource's version|1

 ### **Query parameters :**

 This endpoint does not require query parameters.

 ### **Request body :**

 Key|Desciption|Example value
 --|--|--
 name|Name of file | "my_file.pl"
 path| Path of file from the circle's root| "science/"
 content|File's content|"Lorem ipsum dolor sit amet, consectetur adipiscing elit."

 ### **Response :**

 [`201`] New version of resource is created. 

 [`400`] Bad request.

 [`404`] Not found.


 *Example*

 ```json
 {
    "id" : 4,
    "name" : "my_resource",
    "path" : "/science",
    "content" : "Lorem ipsum dolor sit amet, consectetur adipiscing elit."
 }
 ```

 *Structure (object)*

 Key|Desciption
 --|--
 id|The unique identifier of file
 name|Name of the file
 path|Path of the file from circle's root
 content| Content's file


---



### **`GET`** ***{baseUrl}/api/circles/\<int:pk/resources/\<int:pkr/versions/\<int:pkv/files/***
*Get all files in version `pkv` of resource `pkr` in the circle with id `pk`*

 ### **Resource URL :**
 ```text
 {baseUrl}/api/circles/\<int:pk/resources/\<int:pkr/versions/\<int:pkv/files/
 ```

 ### **HTTP headers :**
 TODO

### **Path parameters :**
 Key|Desciption|Example value
 --|--|--
 pk|id of the circle|3
 pkr|id of the resource|0
 pkv|id of the resource's version|1

 ### **Query parameters :**

 This endpoint does not require query parameters.

 ### **Request body :**

 This endpoint does not require request body.

 ### **Response :**

 [`201`] New version of resource is created. 

 [`400`] Bad request.

 [`404`] Not found.


 *Example*

 ```json
 {
   "files" : [
        {
            "id" : 4,
           "name" : "my_resource",
           "path" : "/science",
       }
   ]
 }
 ```

 *Structure (object)*

 Key|Desciption
 --|--
 files|List of files from a given resource and given version
 id|The unique identifier of file
 name|Name of the file
 path|Path of the file from circle's root


---

### **`GET`** ***{baseUrl}/api/circles/\<int:pk/resources/\<int:pkr/versions/\<int:pkv/files/\<int:pkf/***
*Get all files in version `pkv` of resource `pkr` in the circle with id `pk`*

 ### **Resource URL :**
 ```text
 {baseUrl}/api/circles/\<int:pk/resources/\<int:pkr/versions/\<int:pkv/files/<int:pkf/
 ```

 ### **HTTP headers :**
 TODO

### **Path parameters :**
 Key|Desciption|Example value
 --|--|--
 pk|id of the circle|3
 pkr|id of the resource|0
 pkv|id of the resource's version|1
 pkf|id of the file|2

 ### **Query parameters :**

 This endpoint does not require query parameters.

 ### **Request body :**

 This endpoint does not require request body.

 ### **Response :**

 [`201`] New version of resource is created. 

 [`400`] Bad request.

 [`404`] Not found.


 *Example*

 ```json
 {
    "id" : 4,
    "name" : "my_resource",
    "path" : "/science",
    "content" : "Lorem ipsum dolor sit amet, consectetur adipiscing elit."
 }
 ```

 *Structure (object)*

 Key|Desciption
 --|--
 id|The unique identifier of file
 name|Name of the file
 path|Path of the file from circle's root
 content| Content's file

---


### **`PATCH`** ***{baseUrl}/api/circles/\<int:pk/resources/\<int:pkr/versions/\<int:pkv/files/\<int:pkf/***
*Get all files in version `pkv` of resource `pkr` in the circle with id `pk`*

 ### **Resource URL :**
 ```text
 {baseUrl}/api/circles/\<int:pk/resources/\<int:pkr/versions/\<int:pkv/files/<int:pkf/
 ```

 ### **HTTP headers :**
 TODO

### **Path parameters :**
 Key|Desciption|Example value
 --|--|--
 pk|id of the circle|3
 pkr|id of the resource|0
 pkv|id of the resource's version|1
 pkf|id of the file|2

 ### **Query parameters :**

 This endpoint does not require query parameters.

 ### **Request body :**

 You can update theses fields

 Key|Desciption|Example value
 --|--|--
 name|Name of file | "my_file.pl"
 path| Path of file from the circle's root| "science/"
 content|File's content|"Lorem ipsum dolor sit amet, consectetur adipiscing elit."

 ### **Response :**

 [`201`] New version of resource is created. 

 [`400`] Bad request.

 [`404`] Not found.


 *Example*

 ```json
 {
    "id" : 4,
    "name" : "my_resource",
    "path" : "/science",
    "content" : "Lorem ipsum dolor sit amet, consectetur adipiscing elit."
 }
 ```

 *Structure (object)*

 Key|Desciption
 --|--
 id|The unique identifier of file
 name|Name of the file
 path|Path of the file from circle's root
 content| Content's file

---
