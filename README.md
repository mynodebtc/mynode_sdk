# MYNODE SDK
*Software Development Kit for Application Development*

## Installation
The simplest way to install the SDK is from [PyPi](https://pypi.org/manage/project/mynodesdk/releases/) via pip.

`pip3 install mynodesdk`

## Basic Usage

### Create new Application

To create a new application, run the following command. It will prompt for several answers to properly fill out your app template. A folder based on the "App Name ID" will be created in your current folder with the template.

`mynode-sdk create`

It will ask for some things:
- Application Name
- App Name ID (aka short_name)
- Port Numbers
- Requiring Bitcoin, Lightning, Docker, and Electrum

### Update Application Files

After creating the application, you will need to update several things to make the app functional, like the icon, install script, screenshots, etc... More details are available in the [Customizing your Application](#customizing-your-application) section below.

### Build Application

The appliction can be built from within the app folder or one level above.

`mynode-sdk build <app name id>`

### Add Application to Device

Once the application has been built, it can be added to the device via the web interface. In the web interface, navigate Home -> Marketplace -> Add Application. On that page, select the application *tar.gz* file generated during the previous build state. After submitting the form, your app will be available for installation on your device!
  
## Customizing your Application

After the SDK fills out the template, there are many options available for customizing your app. Some customization steps are required. Replace *appname* with the name id of your app.

### Files to Update

- Update your app icon at *appname*.png
- Update your app info file at *appname*.json
  - *author*
  - *website*
  - *category*
  - *short_description*
  - *description*
  - *latest_version*
  - *targz_download_url*
  - *app_page_content*
- Update your service file at *appname*.service
- Update your install script at script/install_*appname*.service
- Add your own screenshots under the *screenshots* folder

Details of all the configuration options and scripts can be found in the repo for the [application template](https://github.com/mynodebtc/sdk_app_template).

## Publishing your Application

After testing your application and verifying it works well, you can publish it on the myNode platform and share it with the community!

Submit a Pull Request to the myNode project including your application folder under at `rootfs/standard/usr/share/mynode_apps/<app name id>`.

We reserve the right to reject any apps for any reason. We will review it as part of the pull request. Some rules:

- No altcoins
- Must have applicable category
  - Bitcoin
  - Lightning
  - Networking
  - Communication
  - Privacy
  - Or other similar category
- Must be a quality application

## Manual Local Installation of SDK
To manually install the SDK and to test changes, run this command.

`pip3 install --upgrade --no-deps --ignore-installed --force-reinstall .`


## Publishing New SDK Version
To publish a new SDK version:
- Bump Version in setup.py
- Commit and Push All Changes
- Run `python3.8 -m build`
- Run `twine upload -r pypi dist/mynodesdk-<version>*`
