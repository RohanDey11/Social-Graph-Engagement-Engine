# Social Graph & Engagement Engine

## Project Overview

This project is a full-stack social media platform designed to model complex user relationships and automate user retention strategies. The application replicates core social networking functionalities, including a directional user graph (follow/unfollow logic), content feeds, and dynamic user profiling.

A key differentiator of this system is its automated "Churn Prevention" engine. By leveraging asynchronous task queues (Redis and Celery), the application monitors user activity latency and triggers automated engagement loops (email reminders) for users inactive for more than 24 hours.

## Video Demonstration

A comprehensive walkthrough of the application's features, including the user graph logic and automated email triggers, can be viewed here:

https://drive.google.com/file/d/1FV6DqoJzXoUt_Aq0-f1cMjIWApY2sSiN/view?usp=sharing

## Technical Architecture

### Tech Stack

- **Backend:** Python, Flask (REST API)
- **Frontend:** Vue.js, Bootstrap
- **Database:** SQLite (Development) / PostgreSQL (Production ready), SQLAlchemy ORM
- **Asynchronous Processing:** Celery
- **Message Broker:** Redis
- **Caching:** Redis

### System Workflow

1. **User Interaction:** Users interact with the Vue.js frontend to post content or follow other users.
2. **Data Persistence:** Relational data (users, posts, connections) is stored via SQLite/SQLAlchemy.
3. **Async Tasks:**
   - A Celery worker runs a daily background job.
   - The job queries the database to calculate "Activity Recency" (time since last post).
   - If `Time > 24 Hours`, the system queues a notification task in Redis.
4. **Notification:** The worker processes the queue and sends re-engagement emails to at-risk users.

## Key Features

### 1. Social Graph Modeling

- Implemented directional relationships (Follow/Unfollow) using many-to-many database relationships.
- Dynamic feed generation showing posts only from followed users.
- Real-time calculation of network metrics (Follower count, Following count).

### 2. Automated Retention System

- Engineered a background monitoring system to detect user churn.
- Uses Celery beat schedules to trigger daily scans of user activity logs.
- Reduces main-thread latency by offloading email dispatching to background workers.

### 3. User Engagement Analysis

- Tracks "Recency" metrics to identify dormant accounts.
- Visualizes network density through user profile statistics.

## Installation & Setup

### Prerequisites

- Python 3.8+
- Node.js & npm
- Redis Server (Must be running locally)

### Backend Setup

1. Clone the repository.
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
