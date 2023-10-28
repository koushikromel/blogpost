# Django GraphQL BLOGPOST Application

This is a Blogpost Django project that demonstrates how to build a GraphQL API for a simple CRUD (Create, Read, Update, Delete) application. It uses Django, graphene-django, and SQLite as the database.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python3 installed
- Pip (Python package manager)
- Git

## Installation

1. Clone the repository to your local machine:

    ```
    git clone https://github.com/koushikromel/blogpost.git
    ```

2. After installation navigate to the project folder and install the dependencies using the code below

    ```
    pip install -r requirements.txt
    ```

3. Apply database migrations using the command below

    ```bash
    python3 manage.py makemigrations
    python3 manage.py migrate
    ```

4. Run the development server.
    ```bash
    python3 manage.py runserver
    ```
5. Head to this endpoint to test the api
    ```bash
    http://localhost:8000/graphql/
    ```

## Query Examples
```graphql
    { # get all posts
        posts {
            id
            title
            description
            published_date
            author
        }
    }
```

```graphql
{ # get post by id and its comments
    post(id: 1) {
        id
        title
        description
        published_date
        author
        comments {
            id
            text
            author
        }
    }
}
```

```graphql
mutation { # create new post
    createPost(
        title: "Title of the post",
        description: "Description of the post",
        published_date: "2023-10-27",
        author: "Author Name"
    ) {
        post {
            id
            title
            description
            published_date
            author
        }
    }
}
```
```graphql
mutation { # update existing post by its id
    updatePost(
        id: 1,
        title: "Updated Post Title",
        description: "Updated description",
        published_date: "2023-10-30",
        author: "New Author"
    ) {
        post {
            id
            title
            description
            published_date
            author
        }
    }
}
```

```graphql
mutation { # delete comment by id
    deleteComment(
        id: 1
    ) {
        success
    }
}
```

# Contact
If you have any questions or need any further assistance, feel free to [Email Me](mailto:koushikromel@gmail.com)