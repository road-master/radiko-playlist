# Slim image can't install numpy
FROM futureys/claude-code-python-development:20260609002000
COPY pyproject.toml /workspace/
RUN uv sync
COPY . /workspace/
ENTRYPOINT [ "uv", "run" ]
CMD ["pytest"]
