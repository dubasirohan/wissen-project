name: Deploy Image Processing Lambda

on:
  push:
    paths:
      - 'image-processing-lambda/**'

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout
      uses: actions/checkout@v3

    - name: Zip Lambda code
      run: |
        cd image-processing-lambda
        zip -r function.zip .

    - name: Deploy to AWS Lambda
      run: |
        aws lambda update-function-code \
          --function-name image-processing-lambda \
          --zip-file fileb://image-processing-lambda/function.zip