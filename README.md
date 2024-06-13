## openplotter-opencpn-installer

OpenPlotter app to manage OpenCPN and plugins installation.

### Installing

#### For production

Install [openplotter-settings](https://github.com/openplotter/openplotter-settings) for **production** and just install this app from *OpenPlotter Apps* tab.

#### For development

Install [openplotter-settings](https://github.com/openplotter/openplotter-settings) for **development**.

Install openplotter-opencpn-installer dependencies:

`sudo apt install openplotter-settings flatpak libusb-0.1-4`

Clone the repository:

`git clone https://github.com/openplotter/openplotter-opencpn-installer.git`

Make your changes and create the package:

```
cd openplotter-opencpn-installer
dpkg-buildpackage -b
```

Install the package:

```
cd ..
sudo dpkg -i openplotter-opencpn-installer_x.x.x-xxx_all.deb
```

Run post-installation script:

`sudo opencpnPostInstall`

Run:

`openplotter-opencpn-installer`

Make your changes and repeat package and installation steps to test. Pull request your changes to github and we will check and add them to the next version of the [Debian package]((https://cloudsmith.io/~openplotter/repos/openplotter/packages/).

### Documentation

https://openplotter.readthedocs.io

### Support

http://forum.openmarine.net/forumdisplay.php?fid=1