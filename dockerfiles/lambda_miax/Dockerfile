FROM public.ecr.aws/lambda/python:3.11

# Copy function code
COPY ./src/lambda_miax/ ${LAMBDA_TASK_ROOT}

# Install the function's dependencies using file requirements.txt
# from your project folder.
#COPY requirements.txt  .
RUN  pip3 install -r ${LAMBDA_TASK_ROOT}/requirements.txt --target "${LAMBDA_TASK_ROOT}"

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "app.handler" ]