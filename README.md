# Sectors

## Deploying

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/lm-tools/sectors)

### Environment variables

* DEFAULT_FROM_EMAIL
* DJANGO_SECRET_KEY
* GOOGLE_ANALYTICS_ID

## Running

Depends on Python >= 3.4, Sass 3.2.19

Install python dependancies for your environment (local, production, etc):

> pip install -r requirements/[env].txt

Install asset pipeline dependancies:

> bundle install

To run the dev server

> ./manage.py runserver

Or use `foreman` to run as heroku would:

> foreman start

## Faster asset compilation in development

[SASS](http://sass-lang.com/), while awesome, is (comparatively) slow. Compilation of scss assets takes ~1.5s.

To speed asset compilation up locally, replace sass with [sassc](https://github.com/sass/sassc) as follows:

1. install sassc (`brew install sassc`)
2. add the following to `prototype/settings/local.py`:

```python
STATIC_PRECOMPILER_COMPILERS = (
    'static_precompiler.compilers.SCSS', {'executable': 'sassc'}),
)
```
