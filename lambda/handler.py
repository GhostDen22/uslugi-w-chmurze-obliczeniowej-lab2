
import os
import boto3
from html import escape
from botocore.config import Config

BUCKET_NAME = "lab2-szablon-koszykow"
TEMPLATE_KEY = "template.html"


def handler(event, context):
    params = event.get("queryStringParameters") or {}
    imie = params.get("imie", "")

    if not imie or not imie.strip():
        return {
            "statusCode": 400,
            "headers": {
                "Content-Type": "text/plain; charset=utf-8"
            },
            "body": "Brak parametru imie. Uzyj ?imie=Ola"
        }

    s3 = boto3.client(
        "s3",
        endpoint_url=os.environ.get("AWS_ENDPOINT_URL"),
        config=Config(s3={"addressing_style": "path"})
    )

    response = s3.get_object(
        Bucket=BUCKET_NAME,
        Key=TEMPLATE_KEY
    )

    template = response["Body"].read().decode("utf-8")

    bezpieczne_imie = escape(imie, quote=True)

    html = template.replace("{{IMIE}}", bezpieczne_imie)

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "text/html; charset=utf-8"
        },
        "body": html
    }
