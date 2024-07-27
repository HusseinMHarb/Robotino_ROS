# cmvision - Fast color blob detector

## cmvision port for ROS Noetic. Tested on Ubuntu 20.04

![demo.gif](static/demo.gif)

### Dependancies

* WxWidgets

    ```sh
    apt install --no-install-recommends -y \
    libgtk-3-dev  \
    wx3.0-headers \
    libwxgtk3.0-gtk3-dev
    ```
### Usage

1. Use `colorgui` node to select the color ranges for your blobs (Sample launch file in `launch/colorgui.launch`)

    * Click on the colors you want as the images play on the window. The **AB** range will get updated with the each click. 
      Use this range in the colors file (Sample file in `config/colors.txt`)

2. Use `cmvision` node for blob detection (Sample launch file in `launch/cmvision.launch`)

    * Pass the colors file with param `cmvision/color_file`

    * Set param `cmvision/debug_on` to `true` to display the detections

### TODO

1. Remove WxWidgets dependancy and use OpenCV highgui for `colorgui`

2. Publish debug image to a rostopic with a new param to enable it

3. Remove the need for the spaces being exactly correctly for specifying colors in `colors.txt` 

## Credits

- [Original work](http://library.isr.ist.utl.pt/docs/roswiki/cmvision.html) by Nate Koenig

- [ROS Hydro port](https://github.com/utexas-bwi/cmvision) by Piyush Khandelwal

- [ROS Melodic port](https://github.com/kbogert/cmvision) by Kenneth Bogert
