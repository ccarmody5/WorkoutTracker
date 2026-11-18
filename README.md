# WorkoutTracker

Run the web app and PostgreSQL locally with Docker Desktop and WSL 2.

## Prerequisites

Start Docker Desktop and select the WSL 2 engine in **Settings → General**. From PowerShell, run `wsl --list --verbose` to check which distributions are installed. To run Compose from a Linux terminal, install a user distribution such as Ubuntu with `wsl --install -d Ubuntu` if needed. Open it once to finish setup, then enable it in Docker Desktop under **Settings → Resources → WSL Integration**. Docker Desktop can also run Compose from PowerShell using the same WSL 2 engine. [Docker Desktop WSL 2 setup](https://docs.docker.com/desktop/features/wsl/)

## Start the app from WSL

In your WSL terminal, open this checkout. For the existing Windows checkout, use the mounted Windows path.

```bash
cd /mnt/c/Users/Chris-Laptop/Repos/WorkoutTracker
# Run once per checkout. Keep the same .env for this database volume.
if [ ! -f .env ]; then
  password=$(openssl rand -hex 24) &&
    sed "s/^POSTGRES_PASSWORD=.*/POSTGRES_PASSWORD=$password/" .env.example > .env
fi
docker compose up --build -d --wait
```

Open [http://localhost:5000](http://localhost:5000) and select **Workout User**. A fresh database gets this starter profile and a **Weight Training** activity. Startup applies Alembic migrations automatically. The database uses a named Docker volume, so it survives container rebuilds and `docker compose down`.

If port 5000 is in use, change `WORKOUT_PORT` in `.env`, rerun the startup command, and open the new port. The app binds to localhost and shares the selected profile and workout state across browser sessions, so use it as a single-user local app.

## Manage the containers

```bash
docker compose ps
docker compose logs -f web db
docker compose down
```

To run the terminal interface against the same database, run `docker compose exec web python terminal_program.py` while the stack is up.
