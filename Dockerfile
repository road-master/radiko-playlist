# Slim image can't install numpy
FROM python:3.13.3-slim-bookworm AS production
# setuptools 65.3.0 can't lock package defined its dependencies by pyproject.toml
RUN pip install --upgrade --no-cache-dir setuptools>=65.4.0 uv===0.6.14
# && uv pip install --no-managed-python --system --no-dev \
# && uv cache clean \
# && rm -r "$(uv python dir)" \
# && rm -r "$(uv tool dir)" \
# && rm ~/.local/bin/uv ~/.local/bin/uvx
WORKDIR /workspace
COPY . /workspace

FROM production AS development
RUN pip install --no-cache-dir uv===0.6.14 \
 && uv sync
ENTRYPOINT [ "uv", "run" ]
CMD ["pytest"]
