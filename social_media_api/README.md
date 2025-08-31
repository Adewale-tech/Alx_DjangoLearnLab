# Social Media API

## Deployment to Production
- **Hosting**: Deployed on Heroku at `https://social-media-api-prod.herokuapp.com`
- **Configuration**:
  - `settings.py`: `DEBUG=False`, `ALLOWED_HOSTS=['*']`, security settings enabled.
  - Database: Heroku Postgres via `dj-database-url`.
  - Static Files: Managed with WhiteNoise.
- **Deployment Steps**:
  1. Install Heroku CLI and log in.
  2. Create app: `heroku create social-media-api-prod`.
  3. Add Postgres: `heroku addons:create heroku-postgresql:hobby-dev`.
  4. Set `SECRET_KEY`: `heroku config:set SECRET_KEY=...`.
  5. Deploy: `git push heroku main`.
  6. Migrate: `heroku run python manage.py migrate`.
- **Maintenance**:
  - Monitor logs: `heroku logs --tail`.
  - Update dependencies periodically.
- **Testing**:
  - Verified endpoints (e.g., `/api/posts/`, `/api/notifications/`) with Postman.