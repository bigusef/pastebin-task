# start from an official image
FROM python:3.7

# arbitrary location choice
RUN mkdir -p /opt/services/pastebin
WORKDIR /opt/services/pastebin

# install our dependencies
# we use --system flag because we don't need an extra virtualenv
COPY Pipfile Pipfile.lock /opt/services/pastebin/
RUN pip install pipenv && pipenv install --system

# expose the port 8000
EXPOSE 8000

# define the default command to run when starting the container
CMD ["gunicorn", "--chdir", "src", "--bind", ":8000", "pastebin.wsgi:application"]