# HomeMind AI Database Inspection

The HomeMind AI database is a PostgreSQL database with `pgvector` support, running inside a Docker container.

## Connection Details

- **Host**: `localhost` (from your Mac) or `db` (from inside the backend container)
- **Port**: `5432`
- **Database**: `homemind`
- **Username**: `user`
- **Password**: `password`

## How to Connect

### 1. Using PhpStorm / JetBrains IDEs

1. Open the **Database** tool window (usually on the right side).
2. Click the `+` icon -> **Data Source** -> **PostgreSQL**.
3. Enter the following:
   - **Host**: `localhost`
   - **Port**: `5432`
   - **User**: `user`
   - **Password**: `password`
   - **Database**: `homemind`
4. Click **Test Connection**. You may need to download drivers if prompted.

### 2. Using Terminal (psql)

If you have `psql` installed locally:
```bash
psql -h localhost -U user -d homemind
```

Alternatively, you can run `psql` directly inside the running Docker container:
```bash
docker exec -it homemind_db psql -U user -d homemind
```

## Verifying Table Schema

Once connected, you can verify the tables exist:

```sql
\dt
```

Expected tables for Phase 1 MVP (including House Abstraction):
- `users`: User accounts and credentials.
- `houses`: User homes/properties.
- `rooms`: Rooms within houses.
- `furniture`: Furniture within rooms.
- `containers`: Storage containers within furniture.
- `locations`: Unique coordinate for items (Room/Furniture/Container combo).
- `objects`: Stored physical items.
- `memory_history`: Movement and storage history logs.
- `chat_sessions` & `messages`: Natural language interaction logs.
- `object_embeddings`: Vector data for semantic search.
- `alembic_version`: Tracks database migrations.

## Running Migrations

If the database is out of sync, ensure the backend container is running and execute:
```bash
docker exec -it homemind_backend alembic upgrade head
```
