# start by pulling the python image
FROM python:3.8-alpine

# copy the requirements file into the image
COPY ./requirements.txt /fingerboards/requirements.txt

# switch working directory
WORKDIR /fingerboards

# install the dependencies and packages in the requirements file
RUN pip install -r requirements.txt

# copy every content from the local file to the image
COPY . .

CMD [ "python", "-m" , "flask", "run"]
