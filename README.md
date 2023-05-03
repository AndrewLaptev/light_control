# light_control

## About

Simple multi-user service for control lamps over MQTT

## Prerequisites

* Ubuntu >=16.04 (Debian)
* Docker >=20.10
* Docker-compose >= 1.29
* Python >= 3.10

## How it works

Deploy two docker containers with FastAPI (frontend+backend) and Adminer. User DBMS SQLite include FastAPI container and forward via volume in host OS. Connect link to DBMS for Adminer `/dbms/$DBMS_NAME` and password `$DBMS_ADMINER_PASSWORD`. These and others env vars in `.env` (`.env.example`) file

## How to setup

* Copy or rename file `.env.example` to `.env`, open and enter values to env variabels

### Structure of `.env` config file:
 - `DBMS_NAME` - SQLite DBMS name
 - `DBMS_PATH` - path for volumes forward in Docker containers
 - `DBMS_ADMINER_PASSWORD` - password for SQLite DBMS in Adminer
 - `JWT_SECRET_KEY` - 32 digit secret key for hashing JWT (generate example `openssl rand -hex 32`)
 - `JWT_TOKEN_EXPIRE_DAYS` - expire time access tokens in days

## Installation

```bash 
sudo docker-compose up -d
```
