docker run -d \
  -p 9000:9000 -p 9001:9001 \
  --name minio-server \
  --restart always \
  -v /home/ubuntu/minio/files:/data \
  quay.io/minio/minio server /data --console-address ":9001"