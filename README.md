# Spirit (alesdotio fork)

Custom changes from nitely/Spirit:

* Added ability to restrict access, topic creation or comment creation per Category
* User groups
* Unlimited comment length
* User email is now required on registration
* Saner password policy
* User titles
* Added option to upload a file avatar or use a different source (social login)
* Search in comments content
* Configurable ratelimit
* HTML Emails
* Simple but functional Django admin
* Improved compatibility with python-social (social login)


# Spirit

[![Build Status](https://img.shields.io/travis/nitely/Spirit.svg?style=flat-square)](https://travis-ci.org/nitely/Spirit)
[![Coverage Status](https://img.shields.io/coveralls/nitely/Spirit.svg?style=flat-square)](https://coveralls.io/r/nitely/Spirit)
[![pypi](https://img.shields.io/pypi/v/django-spirit.svg?style=flat-square)](https://pypi.python.org/pypi/django-spirit)
[![licence](https://img.shields.io/pypi/l/django-spirit.svg?style=flat-square)](https://raw.githubusercontent.com/nitely/Spirit/master/LICENSE)

Spirit is a Python based forum built using the Django framework.

To see it in action, please visit [The Spirit Project](http://spirit-project.com/).

## Compatibility

* Python 2.7, 3.3, 3.4 (recommended) and 3.5
* Django 1.8 LTS
* PostgreSQL (recommended), MySQL, Oracle Database and SQLite

## Installing (Advanced)

Check out the [example project](https://github.com/nitely/Spirit/tree/master/example).

## Upgrading

Detailed upgrade instructions are listed in [Upgrading Spirit](https://github.com/nitely/Spirit/wiki/Upgrading)

## Testing

The `runtests.py` script enable you to run the test suite of spirit.

- Type `./runtests.py` to run the test suite using the settings from the `spirit` folder.
- Type `./runtests.py example` to run the test suite using the settings from the `example` folder.

## License

MIT
