#!/bin/sh
echo Seed som data
curl \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"name": "Apples",  "price": 2.0}' \
  http://localhost:4000/api/v1.0/fruits

curl \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"name": "Peaches", "price": 5.5}' \
  http://localhost:4000/api/v1.0/fruits

echo