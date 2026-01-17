# Isaac ROS CLI

A command-line interface for managing Isaac ROS development environments.

## Installation

```bash
git clone https://github.com/jega-tagi/isaac-ros-cli.git

# If you don't have build dependencies, install them first:
sudo apt-get install -y debhelper dh-python python3-all python3-setuptools

# Build the package
make build

# Install the newly built package
sudo dpkg -i ../isaac-ros-cli_*.deb
```

## Quick Start

```bash
# 1. Initialize environment (first time only)
sudo isaac-ros init docker

# 2. Activate environment
isaac-ros activate

# 3. Inside container: Install your packages

# 4. Commit changes from inside container (in another terminal)
# Open a new terminal on your host and run:
# The custom image feature allows you to save your installed packages and modifications, while maintaining the ability to # revert to the baseline image.
isaac-ros commit my_isaac_ros:custom --set-default

# 5. Exit container
exit

# 7. Next activation uses your custom image with all packages preserved
isaac-ros activate
```

## Commands

### `isaac-ros init <mode>`
Initialize the Isaac ROS environment. Currently supports `docker` mode.

```bash
sudo isaac-ros init docker
```

### `isaac-ros activate`
Start the Isaac ROS development container. Uses custom image if configured, otherwise uses baseline.

```bash
isaac-ros activate
```

Options:
- `--build` - Build the image remotely if missing
- `--build-local` - Build the image locally if missing
- `--push` - Push the image to registry when complete
- `--use-cached-build-image` - Use cached build image
- `--no-cache` - Do not use docker layer cache
- `--verbose` - Enable verbose output

### `isaac-ros commit [IMAGE_NAME]`
Commit the current container to a custom Docker image to preserve your installations.

```bash
# Commit to custom image
isaac-ros commit my_isaac_ros:custom

# Commit and set as default
isaac-ros commit my_isaac_ros:custom --set-default
```

Options:
- `--set-default` - Automatically configure this image as the default

### Switch Back to Baseline

**Option 1: Edit config file**
```bash
nano ~/.config/isaac-ros-cli/config.yaml
# Set: custom_image: ""
```

**Option 2: Delete user config**
```bash
rm ~/.config/isaac-ros-cli/config.yaml
```

Then run:
```bash
isaac-ros activate  # Uses baseline image
```

### Multiple Custom Images

Create different images for different purposes:

```bash
# Development environment
isaac-ros commit my_isaac_ros:dev --set-default

# Production environment
isaac-ros commit my_isaac_ros:prod

# Testing environment
isaac-ros commit my_isaac_ros:test
```

Switch between them by editing `~/.config/isaac-ros-cli/config.yaml`:

```yaml
docker:
  image:
    custom_image: "my_isaac_ros:dev"  # or :prod, :test, or "" for baseline
```

## Configuration

Configuration files are loaded in order of precedence:

1. **Workspace**: `$ISAAC_ROS_WS/.isaac-ros-cli/config.yaml`
2. **User**: `~/.config/isaac-ros-cli/config.yaml` (created by `isaac-ros commit --set-default`)
3. **System**: `/etc/isaac-ros-cli/config.yaml` (created by `isaac-ros init`)
4. **Default**: `/usr/share/isaac-ros-cli/config.yaml`

### Custom Image Setting

To manually configure a custom image, edit `~/.config/isaac-ros-cli/config.yaml`:

```yaml
docker:
  image:
    custom_image: "my_isaac_ros:custom"  # Your custom image name
```

Set to `""` (empty string) to use the baseline image.

## Development

### Rebuilding Debian Package

To build a new local copy:
```bash
make build
```

### Installing Local Build

```bash
sudo dpkg -i isaac-ros-cli_*.deb
```

## Troubleshooting

**Error: Custom image not found**
- Commit the container first: `isaac-ros commit <name>`
- Or remove `custom_image` from config to use baseline

**Changes not persisting**
- Make sure you committed: `isaac-ros commit <name> --set-default`
- Verify config: `cat ~/.config/isaac-ros-cli/config.yaml`

**Want fresh baseline**
- Clear `custom_image` from config or delete `~/.config/isaac-ros-cli/config.yaml`
