<!-- markdownlint-disable MD033 -->

<h1 align="center"> PLaTon Server</h1>

<p align="center">
<img src="https://raw.githubusercontent.com/PremierLangage/platon-front/df0476c77f6bf4356700a28ae51f207c76696658/assets/images/logo/platon.svg" alt="Logo PLaTon" width="120px" />
</p>

<p align="center">
REST API of <a href="https://github.com/PremierLangage/platon">PLaTon</a> written using <a href="https://www.django-rest-framework.org">Django REST Framework</a>.
</p>

<p align="center">
    <a href="https://github.com/PremierLangage/platon-server/actions/">
        <img src="https://github.com/PremierLangage/platon-server/workflows/Tests/badge.svg" alt="Tests">
    </a>
    <a href="https://codecov.io/gh/PremierLangage/platon-server">
        <img src="https://codecov.io/gh/PremierLangage/platon-server/branch/master/graph/badge.svg" alt="codecov">
    </a>
    <a href="https://www.codefactor.io/repository/github/premierlangage/platon-server/overview/master">
        <img src="https://www.codefactor.io/repository/github/premierlangage/platon-server/badge/master" alt="CodeFactor">
    </a>
    <a href="#">
        <img src="https://img.shields.io/badge/python-3.8+-brightgreen.svg" alt="Python 3.8+"/>
    </a>
    <a href="https://github.com/PremierLangage/platon-server/blob/master/LICENSE">
        <img src="https://img.shields.io/badge/license-CeCILL--B-green" alt="License">
    </a>
</p>

## Development

### Prerequisites

Before you start contributing to this backend project, you should be familiar with the following stacks. We recommend also visiting the links listed at the bottom of this page:

- [`Python >= 3.8`](https://www.python.org/)
- [`Pip3`](https://pip.pypa.io/en/stable/installing/)
- [`Django`](https://pip.pypa.io/en/stable/installing/)
- [`Django Channels`](https://channels.readthedocs.io/en/stable/index.html)
- [`Django REST Framework`](https://www.django-rest-framework.org)
- [`PostgreSQL`](https://www.postgresql.org)
- [`Redis`](https://redis.io)
- [`Celery`](https://docs.celeryproject.org/en/stable/)
- [`Uvicorn`](https://www.uvicorn.org)
- [`Elasticsearch`](https://django-elasticsearch-dsl.readthedocs.io/en/latest/quickstart.html)
- [`PLaTon sandbox`](https://github.com/PremierLangage/sandbox)

### Getting started

Using this project requires to setup multiple services like a PostgreSQL database, a Redis cache, or Elasticsearch... So instead of installing all theses tools on your system, you should follow the instructions on the
[main repository](https://github.com/PremierLangage/platon) of PLaTon project to use a dockerized version of PLaTon during your development or deployment. A documentation is also hosted over there.

### Contributing

#### Contributing guidelines

Read through our [contributing guidelines](https://github.com/PremierLangage/platon/blob/master/CONTRIBUTING.md) to learn about our submission process, coding rules and more.

#### Want to help?

Want to report a bug, contribute some code, or improve the platform? Read up on our guidelines for
[contributing](https://github.com/PremierLangage/platon/blob/master/CONTRIBUTING.md) and then check out one of our issues labeled as [help wanted](https://github.com/PremierLangage/platon/labels/help%20wanted) or
[submit a new one](https://github.com/PremierLangage/platon/issues).

### Links

- [Django tutorial](https://docs.djangoproject.com/en/3.1/intro/tutorial01/)
- [Django Channels tutorial](https://www.tutorialdocs.com/tutorial/django-channels/introduction.html)
- [Django Elasticsearch tutorial](https://apirobot.me/posts/django-elasticsearch-searching-for-awesome-ted-talks)
- [Django REST Framework tutorial](https://www.django-rest-framework.org)
- [Django + Frontend Frameworks tutorial](https://testdriven.io/blog/django-spa-auth/#conclusion)
- [Django + Docker + Nginx tutorial](https://medium.com/bb-tutorials-and-thoughts/how-to-serve-angular-application-with-nginx-and-docker-3af45be5b854)
- [Django + Docker + Redis + Celery tutorial](https://soshace.com/dockerizing-django-with-postgres-redis-and-celery/)
- [Django Elasticsearch + Django REST Framework tutorial](https://www.merixstudio.com/blog/elasticsearch-django-rest-framework/)
