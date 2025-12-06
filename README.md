# ♠️ Blackjack: Massive Multiplayer Online Game

> A high-concurrency, real-time multiplayer Blackjack platform powered by **FastAPI**, **WebSockets**, and **Docker**.
> Designed to simulate "Twitch Plays" style cooperative gameplay.

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg?style=flat&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-High%20Performance-green.svg?style=flat&logo=fastapi)
![Docker](https://img.shields.io/badge/Docker-Containerized-blue.svg?style=flat&logo=docker)
![AWS](https://img.shields.io/badge/AWS-EC2%20Deployed-orange.svg?style=flat&logo=amazon-aws)
![WebSocket](https://img.shields.io/badge/Protocol-WebSocket-lightgrey.svg?style=flat)

## 📖 Introduction (專案簡介)

This project demonstrates a **Server-Push Architecture** capable of handling real-time state synchronization across multiple clients. 
Instead of traditional turn-based logic, it implements a **"World Co-op"** mode where all connected players share a single global game state, voting (via first-come-first-serve actions) to Hit or Stand against the Dealer.

**Live Demo:** [Wait for AWS Deployment] (Coming Soon)

## 🏗 System Architecture (系統架構)

The system is containerized using Docker and deployed on AWS EC2, utilizing Nginx as a reverse proxy to handle WebSocket upgrades.

```mermaid
graph TD
    User["Clients / Players"] -->|HTTPS / WSS| CF["Cloudflare CDN"]
    CF -->|Port 80| Nginx["Nginx Reverse Proxy"]
    
    subgraph "AWS EC2 Instance"
        Nginx -->|Proxy Pass| Docker["Docker Container"]
        
        subgraph "Blackjack Service"
            Docker -->|Run| Uvicorn["Uvicorn ASGI Server"]
            Uvicorn -->|Mount| FastAPI["FastAPI App"]
            
            FastAPI -->|Manage| CM["Connection Manager"]
            FastAPI -->|Logic| GameEngine["Game Logic (Singleton)"]
            
            CM <-->|Broadcast State| User
        end
    end