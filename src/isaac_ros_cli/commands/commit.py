# Copyright (c) 2025, NVIDIA CORPORATION. All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto. Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

import click
import subprocess
import sys

from isaac_ros_cli.config_loader import load_config, update_config, ConfigScope


@click.command()
@click.argument('image_name', required=False)
@click.option('--set-default', is_flag=True, help='Set the committed image as default in config.')
def commit(image_name: str, set_default: bool):
    """Commit the current container to a custom image.
    
    This allows you to save your installed packages and modifications.
    
    Examples:
        isaac-ros commit my_isaac_ros:custom
        isaac-ros commit my_isaac_ros:custom --set-default
    """
    cfg = load_config()
    container_name = cfg['docker']['run']['container_name']
    
    # Check if container exists
    result = subprocess.run(
        ["docker", "ps", "-a", "--filter", f"name={container_name}", "--format", "{{.Names}}"],
        capture_output=True,
        text=True
    )
    
    if not result.stdout.strip():
        click.echo(f"Error: Container '{container_name}' not found.", err=True)
        click.echo("Please run 'isaac-ros activate' first to create a container.", err=True)
        sys.exit(1)
    
    # If no image name provided, use default
    if not image_name:
        image_name = f"{container_name}_custom:latest"
        click.echo(f"No image name provided, using: {image_name}")
    
    # Commit the container
    click.echo(f"Committing container '{container_name}' to image '{image_name}'...")
    commit_result = subprocess.run(
        ["docker", "commit", container_name, image_name],
        capture_output=True,
        text=True
    )
    
    if commit_result.returncode != 0:
        click.echo(f"Error: Failed to commit container: {commit_result.stderr}", err=True)
        sys.exit(1)
    
    click.echo(f"✓ Successfully committed to image: {image_name}")
    
    # Set as default if requested
    if set_default:
        click.echo(f"Setting '{image_name}' as default custom image in config...")
        overlay = {
            'docker': {
                'image': {
                    'custom_image': image_name
                }
            }
        }
        config_path = update_config(overlay, ConfigScope.USER)
        click.echo(f"✓ Updated config at: {config_path}")
        click.echo(f"Next 'isaac-ros activate' will use this custom image.")
    else:
        click.echo(f"\nTo use this image, either:")
        click.echo(f"  1. Run: isaac-ros commit {image_name} --set-default")
        click.echo(f"  2. Manually edit ~/.config/isaac-ros-cli/config.yaml")
        click.echo(f"     Set: docker.image.custom_image: \"{image_name}\"")
