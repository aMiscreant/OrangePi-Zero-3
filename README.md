# OrangePi-Zero-3
 Orange Pi Zero 3, including peripherals like TFT screens, sensors, and other essential hardware. It provides a collection of useful scripts and step-by-step guides to help streamline the setup and ensure seamless operation of your Orange Pi Zero 3 with various accessories.

---

- 7735S [Monkey patch for Raspberry GPIO to configure 7735S]

        Configure IC:ST7735s [Manually enabled spi, overlay should work to enable spi]
        used Raspberry pi's python gpio lib; with a monkey patch for orangepi zero3
        to utilize the RGB_TFT (IC: ST7735S). Plays videos, images, gifs, emulates termial.
        "Surpisingly the video isnt terribly bad."

- BlueDucky [OrangePi Zero3 version]
            
      Configure virtual venv to inherit system packages.
      python -m site && edit the virtual config to use system packages.
      All other steps can remain the same, you will need pybluez stable from debian
      repo for this to work.

- GPIO [GPIO Scripts]

        Interactive / GPIO scripts to view.
        overlay tuple / pin / interface keyword.

- IR_Controller [ir_controller, contains scripts for configuration for IR on sunxi top hats.]

        Can be easily configured to add commands recieved from IR Controllers.
        Verify screen dimensions, easy to add commands to.

- Kernel [Kernel build scripts for mainline]

        ToDo [needs firmware / patches] - will stick work but you will be missing key firmware.

- TFT [Screensavers for TFT]

        Variety on screensavers for TFT, Double visual overlays.