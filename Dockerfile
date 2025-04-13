# Slim image can't install numpy
FROM python:3.11.1-slim-bullseye AS production
# setuptools 65.3.0 can't lock package defined its dependencies by pyproject.toml
RUN pip install --upgrade setuptools>=65.4.0
WORKDIR /workspace
COPY . /workspace
RUN pip --no-cache-dir install pipenv==2022.8.30 \
 && pipenv install --skip-lock \
 && pip uninstall -y pipenv virtualenv-clone virtualenv

FROM production AS development
# see: https://pythonspeed.com/articles/activate-virtualenv-dockerfile/
ENV PIPENV_VENV_IN_PROJECT=1
# see:
# - Fail to pipenv update due to MetadataGenerationFailed · Issue #5377 · pypa/pipenv
#   https://github.com/pypa/pipenv/issues/5377
RUN pip --no-cache-dir install pipenv==2022.8.30 \
 && pipenv install --skip-lock --dev
ENTRYPOINT [ "pipenv", "run" ]
CMD ["pytest"]
