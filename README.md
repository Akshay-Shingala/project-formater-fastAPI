# Project Formater FastAPI

## Overview

**Project Formater FastAPI** is a Python-based application built with FastAPI. Its main purpose is to provide a simple and efficient way to format, organize, or process projects using a web API. The project leverages the speed and modern features of FastAPI, making it suitable for building scalable and high-performance APIs.

## Features

- Built with FastAPI for rapid API development
- GraphQL API powered by Strawberry for flexible and efficient data querying
- Supports pre-commit hooks for code quality
- Easy to extend and customize for various formatting or processing use-cases
- Designed for scalability and performance
- Simple structure for quick setup and use

## Why GraphQL?

We use **GraphQL** (with [Strawberry](https://strawberry.rocks/)) for APIs because it allows clients to request exactly the data they need and nothing more. This is especially useful for complex data models (like authors and books) and for reducing over-fetching/under-fetching of data compared to REST.

**Benefits:**
- Flexible queries: Fetch nested and related data in a single request.
- Strong typing: The schema defines exactly what queries and mutations are possible.
- Self-documenting: GraphQL Playground/GraphiQL lets you explore the API interactively.

## Example: Using GraphQL

After running the server (`uvicorn main:app --reload`), open [http://127.0.0.1:8000/graphql](http://127.0.0.1:8000/graphql) in your browser for the GraphiQL interface.

### Example Query: Get All Authors and Their Books

```graphql
query {
  authors {
    id
    name
    bio
    books {
      id
      title
      description
    }
  }
}
```

### Example Mutation: Add a New Author

```graphql
mutation {
  createAuthor(author: { name: "John Doe", bio: "Writes about APIs" }) {
    id
    name
    bio
  }
}
```

## Why Use pre-commit?

This project uses **pre-commit**, a framework for managing and maintaining multi-language pre-commit hooks. 

**pre-commit** is useful because:
- It automatically runs checks and formatting tools before you make a commit, enforcing code quality.
- It prevents committing code that doesn’t follow best practices or formatting guidelines.
- It can catch common mistakes (like trailing whitespace, missing newlines, linting errors) before they get into your repository.
- It saves time on code review and keeps your codebase cleaner.

To use pre-commit, ensure you have it installed and run `pre-commit install` after cloning the repo.

## Project Contents

- Python source code (main API and related modules)
- GraphQL schema and resolvers
- Configuration files for FastAPI and dependencies
- Requirements file for managing Python dependencies
- (Other files may include tests, documentation, and utilities)

## Usage

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Akshay-Shingala/project-formater-fastAPI.git
   cd project-formater-fastAPI
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **(Optional) Install pre-commit hooks:**
   ```bash
   pip install pre-commit
   pre-commit install
   ```

### Running the Project

1. **Start the FastAPI server:**
   ```bash
   uvicorn "app demo code.main:app" --reload
   ```

2. **Access the API:**
   - Open your browser and go to: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for interactive REST API documentation.
   - Or use the [http://127.0.0.1:8000/graphql](http://127.0.0.1:8000/graphql) endpoint for GraphQL.

## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss your ideas.

## License

This project is licensed under the terms you prefer. (Add a LICENSE file for more details.)
