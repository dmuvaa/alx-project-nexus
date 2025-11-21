E-Commerce Backend API

A production-style backend for an e-commerce product catalog using Django, PostgreSQL, and JWT authentication.
This project is built as part of the ALX Backend Engineering (ProDev) program.

Overview

This project provides a scalable backend API featuring:

User registration and authentication with JWT

CRUD operations for products and categories

Advanced querying: filtering, sorting, and pagination

PostgreSQL database optimization with indexing

Interactive API documentation using Swagger/OpenAPI

Features
Feature	Description
Authentication	Register and login using JWT tokens
Product Catalog	Full CRUD for products with category relations
Filtering	Filter by category, price range, and stock availability
Sorting	Sort results by price and creation date
Pagination	Page-based responses for large product datasets
Optimization	Indexing and query tuning for performance
API Docs	Swagger UI from an auto-generated OpenAPI schema
Technologies
Category	Tools
Backend	Django, Django REST Framework
Database	PostgreSQL
Authentication	djangorestframework-simplejwt
Documentation	drf-spectacular (Swagger/OpenAPI)
Deployment	Compatible with Render, Railway, Fly.io, etc.
