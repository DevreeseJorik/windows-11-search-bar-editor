# Windows 11 Search Bar Icon Editor

This repository enables swift editing of the Windows 11 search bar icon to any SVG file through registry manipulation. The SVGs are stored in the registry at:
`Computer\HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\SearchSettings\Dynamic\ {-} \icons` with key names `0` and `1` of type `REG_BINARY` containing the SVG data in binary format.

![Windows 11 Search Bar Icon](embeds/win11-searchbar-poc.png)

Editing the SVGs does not automatically update them. To accomplish this, the code temporarily changes the search bar state to one not displaying the image, then edits the images, and finally restores the search bar state to display the edited icons. This process reinitializes the SVGs, allowing custom-injected ones to be displayed.

This state is stored at:
`Computer\HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Search`
with key name `SearchboxTaskbarMode` of type `REG_DWORD`. While this state can be manually adjusted in Windows settings under the personalization tab, the script automates this process for convenience.

To use the repository, simply place your preferred SVG under [/svg/my-svg.svg](/svg/my-svg.svg) and run the Python script. No additional requirements need to be installed beyond a clean Python installation.

