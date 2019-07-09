set -e

image_name="pubmed_parser"
image_version=0.1
image_name=$image_name:$image_version

docker build \
    -t $image_name .

docker tag $image_name $HW_IMAGE_PREFIX/$image_name
docker push $HW_IMAGE_PREFIX/$image_name
