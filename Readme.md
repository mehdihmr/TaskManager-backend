```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

```bash
# Drop the database (or tables)
flask db downgrade base  # optional: revert all migrations
# Or drop tables manually using your DB client

# Delete migration folder (optional, if you want to restart)
rm -rf migrations

# Re-initialize migrations
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```