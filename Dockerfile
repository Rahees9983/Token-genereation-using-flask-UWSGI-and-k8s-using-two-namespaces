# Use an official Python runtime as a parent image
FROM python:3.6

# Set the working directory to /app
WORKDIR /raheesapp

# Copy the current directory contents into the container at /app
COPY . /raheesapp

# Install any needed packages specified in requirements.txt
RUN pip3 install -r req.txt

# Make port 5000 available to the world outside this container
EXPOSE 9095 5000

# Run app.py when the container launches
# CMD ["python3", "curd_project.py"]
# CMD ["python3", "falsk_with_mongo.py"]
CMD [ "uwsgi", "jwt.ini" ]