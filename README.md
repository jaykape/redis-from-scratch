<p>
<picture>
<img src="public/logo.png">
</picture>
</p>

I built a Redis implementation in Python for fun. It works almost like the real Redis you can connect using redis-cli or a Redis client from any language, most functionality is implemented.

## How to Run

Start by `cd` to the root of this repo.

### With Docker

```bash
docker build -t kape-redis .
docker run -p 6379:6379 kape-redis
```

Now your Redis server is accessible on `localhost:6379`

Or run it directly without Docker (Python >= 3.10 required)

#### Windows

```
python -m app.main
```

#### Linux/macOS

```
python3 -m app.main
```
