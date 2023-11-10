# E-Commerce API

[![LinkedIn Post](https://img.shields.io/badge/LinkedIn-0A66C2?logo=linkedin&logoColor=fff&style=flat-square)](https://www.linkedin.com/posts/arv-anshul_fastapi-api-ecommerce-activity-7128575593570340864-WE2m?utm_source=share&utm_medium=member_desktop)
[![GitHub Badge](https://img.shields.io/badge/GitHub-181717?logo=github&logoColor=fff&style=flat-square)](https://github.com/arv-anshul)

This is an API project which scrapes data from e-commerce websites (for now only [flipkart.com](https://flipkart.com)).

#### What I Learn While Creating This API?

1. Gets a deep dive into `FastAPI` framework.
2. Learned http request methods further at intermediate level and used more http status codes.
3. Used some awesome tricks to handle Errors and Exceptions.
4. Explored `pydantic` library, modular programming, OOPs concepts and many more things.

### Tech Stacks

|           Stack | Tech                                                                                                        |
| --------------: | :---------------------------------------------------------------------------------------------------------- |
|    Web scraping | ![Python](https://img.shields.io/badge/Beautiful%20Soup-3776AB?logo=python&logoColor=fff&style=flat-square) |
|         Backend | ![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=fff&style=flat-square)        |
| Data Validation | ![Pydantic](https://img.shields.io/badge/Pydantic-E92063?logo=pydantic&logoColor=fff&style=flat-square)     |
|        Websites | ![Flipkart](https://img.shields.io/badge/Flipkart-2874F0?logo=flipkart&logoColor=fff&style=flat-square)     |
|     Curl Parser | ![Python](https://img.shields.io/badge/Curler-%40me-3776AB?logo=python&logoColor=fff&style=flat-square)     |

### Usage

1. Clone this repo.
2. Install the projects requirements with following command:

```sh
pip install -r requirements.txt
```

3. Run the fastapi app.

```sh
uvicorn --reload ecommerce.api.app:app
```

4. Now FastAPI instance is running on your system. So, you can access it on your localhost with the following url:

```url
http://localhost:8000/
```

For better representation of the APIs head to:

```url
http://localhost:8000/docs
```

### API Endpoints

#### Screenshot of OpenAPI Docs

![OpenAPI Docs](assets/flipkart-api-routes.png "Flipkart API Routes")
