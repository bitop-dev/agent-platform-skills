---
name: s3_storage
version: 1.0.0
description: "S3-compatible object storage — put, get, and list objects. Use for persisting reports, data exports, and artifacts."
author: platform-team
tags: [storage, s3, aws, artifacts]
emoji: "📦"
always: false
runtime: wasm
requires: {}
---
# S3 Storage
Read and write files to S3-compatible storage (AWS S3, R2, MinIO). Runs as a sandboxed WASM module.

## Required Credentials
- `AWS_ACCESS_KEY_ID` — AWS access key
- `AWS_SECRET_ACCESS_KEY` — AWS secret key
- `S3_BUCKET` — Bucket name
- `S3_REGION` — AWS region (default: us-east-1)
