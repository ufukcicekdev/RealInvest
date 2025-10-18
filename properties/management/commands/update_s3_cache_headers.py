"""
Management command to update Cache-Control headers for existing files in S3/DigitalOcean Spaces
This will improve performance by setting proper cache times for static assets.
"""

from django.core.management.base import BaseCommand
from django.conf import settings
import boto3
import os


class Command(BaseCommand):
    help = 'Update Cache-Control headers for existing files in S3/DigitalOcean Spaces'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be updated without actually updating',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        # Check if we're in production mode
        if settings.DEBUG:
            self.stdout.write(self.style.WARNING(
                'This command should only be run in production mode (DEBUG=False)'
            ))
            return

        # Get S3 credentials from environment
        access_key = os.getenv('AWS_ACCESS_KEY_ID')
        secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
        bucket_name = os.getenv('AWS_STORAGE_BUCKET_NAME')
        region_name = os.getenv('AWS_S3_REGION_NAME')
        endpoint_url = os.getenv('AWS_S3_ENDPOINT_URL')

        if not all([access_key, secret_key, bucket_name, region_name, endpoint_url]):
            self.stdout.write(self.style.ERROR(
                'Missing required S3 environment variables. Please check your .env file.'
            ))
            return

        # Initialize S3 client
        s3_client = boto3.client(
            's3',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region_name,
            endpoint_url=endpoint_url
        )

        # Define file extensions that should have long cache times (1 year)
        long_cache_extensions = (
            '.webp', '.jpg', '.jpeg', '.png', '.gif', '.svg', '.ico',
            '.woff', '.woff2', '.ttf', '.eot', '.otf',
            '.css', '.js'
        )

        # Content-Type mapping
        content_type_map = {
            '.webp': 'image/webp',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif',
            '.svg': 'image/svg+xml',
            '.ico': 'image/x-icon',
            '.css': 'text/css',
            '.js': 'application/javascript',
            '.woff': 'font/woff',
            '.woff2': 'font/woff2',
            '.ttf': 'font/ttf',
            '.eot': 'application/vnd.ms-fontobject',
            '.otf': 'font/otf',
        }

        updated_count = 0
        skipped_count = 0

        try:
            # List all objects in the bucket
            self.stdout.write(self.style.SUCCESS(f'Scanning bucket: {bucket_name}'))
            
            paginator = s3_client.get_paginator('list_objects_v2')
            pages = paginator.paginate(Bucket=bucket_name)

            for page in pages:
                if 'Contents' not in page:
                    continue

                for obj in page['Contents']:
                    key = obj['Key']
                    file_extension = os.path.splitext(key)[1].lower()

                    # Skip if not a static asset
                    if file_extension not in long_cache_extensions:
                        skipped_count += 1
                        continue

                    # Determine cache control and content type
                    cache_control = 'public, max-age=31536000, immutable'
                    content_type = content_type_map.get(file_extension, 'application/octet-stream')

                    if dry_run:
                        self.stdout.write(
                            f'Would update: {key}\n'
                            f'  Cache-Control: {cache_control}\n'
                            f'  Content-Type: {content_type}'
                        )
                    else:
                        # Copy object to itself with new metadata
                        try:
                            s3_client.copy_object(
                                Bucket=bucket_name,
                                CopySource={'Bucket': bucket_name, 'Key': key},
                                Key=key,
                                MetadataDirective='REPLACE',
                                CacheControl=cache_control,
                                ContentType=content_type,
                                ACL='public-read'
                            )
                            self.stdout.write(self.style.SUCCESS(f'✓ Updated: {key}'))
                            updated_count += 1
                        except Exception as e:
                            self.stdout.write(self.style.ERROR(f'✗ Error updating {key}: {str(e)}'))

            # Summary
            self.stdout.write(self.style.SUCCESS(
                f'\n{"DRY RUN - " if dry_run else ""}Summary:\n'
                f'  Updated: {updated_count}\n'
                f'  Skipped: {skipped_count}\n'
                f'  Total: {updated_count + skipped_count}'
            ))

            if dry_run:
                self.stdout.write(self.style.WARNING(
                    '\nThis was a dry run. Run without --dry-run to actually update files.'
                ))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))
