# Use an official Python image as a parent image
FROM python:3.11-slim

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir streamlit

# Copy the UI application
WORKDIR /app
COPY . /app

# Make port 8501 available to the world outside this container
EXPOSE 8501

RUN mkdir -p ~/.streamlit
RUN echo "\
[server]\n\
fileWatcherType = \"none\"\n\
" > ~/.streamlit/config.toml

# Run ui.py when the container launches
CMD ["streamlit", "run", "ui.py", "--server.port=8501", "--server.address=0.0.0.0"]