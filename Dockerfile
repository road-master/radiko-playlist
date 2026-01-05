# Slim image can't install numpy
FROM futureys/claude-code-python-development:20251104123000
COPY pyproject.toml /workspace/
RUN uv sync --python 3.13
COPY . /workspace/
RUN uv sync
ENTRYPOINT [ "uv", "run" ]
CMD ["pytest"]
