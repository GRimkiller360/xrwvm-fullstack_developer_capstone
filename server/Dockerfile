FROM python:3.12.0-slim-bookworm
ENV PYTHONBUFFERED 1
ENV PYTHONWRITEBYTECODE 1
ENV APP=/app
ENV PORT=8000
# Change the workdir.
WORKDIR $APP
# Install the requirements
COPY requirements.txt $APP
RUN pip3 install -r requirements.txt
# Copy the rest of the files
COPY . $APP
EXPOSE $PORT
RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["/bin/bash","/app/entrypoint.sh"]
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:$PORT --workers 3 djangoproj.wsgi"]