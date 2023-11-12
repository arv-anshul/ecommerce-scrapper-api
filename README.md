# E-Commerce Scrapper API

<p align=center>
  <a href="https://www.linkedin.com/posts/arv-anshul_fastapi-api-ecommerce-activity-7128575593570340864-WE2m?utm_source=share&utm_medium=member_desktop">
    <img src="https://img.shields.io/badge/LinkedIn-0A66C2?logo=linkedin&logoColor=fff&style=for-the-badge" alt="LinkedIn Post">
  </a>
  <a href="https://github.com/arv-anshul">
    <img src="https://img.shields.io/badge/GitHub-181717?logo=github&logoColor=fff&style=for-the-badge" alt="GitHub Badge">
  </a>
</p>

Welcome to the E-commerce API project! 🌐 This API is designed to scrape valuable data from E-commerce websites, with a focus on [Flipkart](https://flipkart.com) (for now).

#### 🧐 What I Learned While Creating This API?

- 🕵️ **FastAPI Framework:** Explored the ins and outs of the powerful `FastAPI` framework, leveraging its asynchronous capabilities for efficient and speedy data retrieval.
- 🤓 **HTTP Request Methods and Status Codes:** Delved deeper into HTTP request methods at an intermediate level, mastering the use of various HTTP status codes for a more nuanced and controlled API interaction.
- 💡 **Error Handling and Exception Tricks:** Implemented clever techniques to handle errors and exceptions, ensuring a robust and graceful API experience for users.
- 🗺️ **Pydantic Library and Modular Programming:** Explored the versatility of the `pydantic` library for data validation and modular programming. Embraced object-oriented programming (OOPs) concepts for a more structured and maintainable codebase.
- 🧪 **Writing Tests:** Implemented thorough [tests](ecommerce/tests/test_api/) for the FastAPI application, ensuring the reliability and correctness of every API endpoint.

### 🤝 What You Can Achieve With My APIs?

- **Data Analysis:** Conduct in-depth data analysis on the information fetched from E-commerce websites. Gain insights into price variations, product specification differences, and overall market trends.
- **Machine Learning Integration:** Leverage the scraped data to build machine learning models. Explore possibilities such as sentiment analysis, product price prediction (for items like Mobiles, Laptops, etc.), and other innovative applications.
- **Custom Use Cases:** The versatility of this API allows you to tailor its application to your specific needs. Whether you're interested in market research, trend analysis, or creating unique machine learning applications, the possibilities are vast.
- **Data-Driven Decision Making:** Empower your decision-making process with accurate and up-to-date data from E-commerce websites. Use the insights gained to make informed choices in various domains.

### 🧑‍💻 Tech Stacks

|           Stack | Tech                                                                                                        |
| --------------: | :---------------------------------------------------------------------------------------------------------- |
|    Web scraping | ![Python](https://img.shields.io/badge/Beautiful%20Soup-3776AB?logo=python&logoColor=fff&style=flat-square) |
|         Backend | ![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=fff&style=flat-square)        |
| Data Validation | ![Pydantic](https://img.shields.io/badge/Pydantic-E92063?logo=pydantic&logoColor=fff&style=flat-square)     |
|        Websites | ![Flipkart](https://img.shields.io/badge/Flipkart-2874F0?logo=flipkart&logoColor=fff&style=flat-square)     |
|     Curl Parser | ![Python](https://img.shields.io/badge/Curler-%40me-3776AB?logo=python&logoColor=fff&style=flat-square)     |

### 🧩 Usage

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

### 📌 API Endpoints

#### 🖼️ Screenshot of OpenAPI Docs

![OpenAPI Docs](assets/flipkart-api-routes.png "Flipkart API Routes")
