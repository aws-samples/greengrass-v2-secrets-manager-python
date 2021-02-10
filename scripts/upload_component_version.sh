# MIT No Attribution
#
# Copyright 2021 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

if [ $# -ne 5 ]; then
  echo 1>&2 "Usage: $0 AWS-PROFILE-NAME COMPONENT_NAME COMPONENT_VERSION BUCKET_NAME AWS_REGION"
  exit 3
fi

AWS_PROFILE=$1
COMPONENT_NAME=$2
COMPONENT_VERSION=$3
S3_BUCKET_NAME=$4
AWS_REGION=$5

cd components/artifacts/$COMPONENT_NAME/$COMPONENT_VERSION

for FILE in *; do aws s3api put-object --profile $AWS_PROFILE --bucket $S3_BUCKET_NAME --key artifacts/$COMPONENT_NAME/$COMPONENT_VERSION/$FILE --body $FILE; done

cd ../../..

aws greengrassv2 create-component-version --profile $AWS_PROFILE --inline-recipe fileb://recipes/$COMPONENT_NAME-$COMPONENT_VERSION.yaml --region $AWS_REGION