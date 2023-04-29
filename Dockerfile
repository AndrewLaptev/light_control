FROM python:3.10-alpine AS build-image

RUN pip install pdm~=2.5.3
COPY ./pdm.lock pyproject.toml /service/
WORKDIR /service
RUN mkdir __pypackages__ && pdm sync --prod --no-self


FROM python:3.10-alpine AS runtime-image

ENV PYTHONPATH=/service/pkgs
COPY --from=build-image /service/__pypackages__/3.10/lib /service/pkgs
COPY . /service
WORKDIR /service

ENTRYPOINT ["python", "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
