import winreg

class FileDataReader:
    def read_data(self, file_path):
        try:
            with open(file_path, 'rb') as file:  # Read file in binary mode
                return file.read()  # Return binary data
        except FileNotFoundError:
            return None

class RegistryEditor:
    def __init__(self, key):
        self.key = key

    def read_value(self, subkey, value_name):
        try:
            with winreg.OpenKey(self.key, subkey) as reg_key:
                value, _ = winreg.QueryValueEx(reg_key, value_name)
                return value
        except FileNotFoundError:
            return None

    def read_subkey_at_index(self, subkey, index):
        try:
            with winreg.OpenKey(self.key, subkey) as key:
                subkey_name = winreg.EnumKey(key, index)
                return subkey_name
        except OSError as e:
            if e.errno == 2:  # The registry key does not exist
                return None

    def read_subkeys(self, subkey):
        subkeys = []
        try:
            with winreg.OpenKey(self.key, subkey) as key:
                index = 0
                while True:
                    subkey_name = winreg.EnumKey(key, index)
                    subkeys.append(subkey_name)
                    index += 1
        except OSError as e:
            if e.errno == 2:  # The registry key does not exist
                pass
        return subkeys
    
    def write_value(self, subkey, value_name, value, value_type=winreg.REG_SZ):
        try:
            with winreg.OpenKey(self.key, subkey, 0, winreg.KEY_WRITE) as reg_key:
                winreg.SetValueEx(reg_key, value_name, 0, value_type, value)
                print(f"Value {value_name} has been successfully updated.")
        except OSError as e:
            print(f"Error occurred while writing value: {e}")

class RegistryImageEditor(RegistryEditor):
    def __init__(self, key):
        super().__init__(key)

    def print_image_data(self, subkey, value_name):
        print(f"subkey: {subkey}")
        image_data = self.read_value(subkey, value_name)
        if image_data:
            print(f"Image data for {value_name}:")
            print(image_data)
        else:
            print(f"No data found for {value_name}")

    def edit_image_data(self, subkey, value_name, file_path):
        image_data = FileDataReader().read_data(file_path)

        if image_data:
            try:
                with winreg.OpenKey(self.key, subkey, 0, winreg.KEY_WRITE) as reg_key:
                    winreg.SetValueEx(reg_key, value_name, 0, winreg.REG_BINARY, image_data)  # Write as REG_BINARY
                    print(f"Image data for {value_name} has been successfully updated.")
            except OSError as e:
                print(f"Error occurred while editing image data: {e}")

def main():
    search_reg = r"Software\Microsoft\Windows\CurrentVersion\Search"
    search_settings_reg = r"Software\Microsoft\Windows\CurrentVersion\SearchSettings\Dynamic"
    registry_editor = RegistryImageEditor(winreg.HKEY_CURRENT_USER)
    dir_name = registry_editor.read_subkey_at_index(search_settings_reg, 1)

    if dir_name:
        print(f"Dir found: {search_settings_reg}\\{dir_name}")
        icon_dir = search_settings_reg + "\\" + dir_name + r"\icons"

        # Initialize RegistryImageEditor
        # Print data for images 0 and 1
        # registry_editor.print_image_data(icon_dir, "0")
        # registry_editor.print_image_data(icon_dir, "1")

        # Edit data for image 0

        # set search_reg's SearchboxTaskbarMode to 0
        registry_editor.write_value(search_reg, "SearchboxTaskbarMode", 0, winreg.REG_DWORD)

        # wait 3 seconds
        file_path = r"C:\Users\jorik\OneDrive\Documents\Projects\RegistryTweak\svg\my-svg.svg"
        registry_editor.edit_image_data(icon_dir, "0", file_path)
        registry_editor.edit_image_data(icon_dir, "1", file_path)

        # set search_reg's SearchboxTaskbarMode to 2
        registry_editor.write_value(search_reg, "SearchboxTaskbarMode", 2, winreg.REG_DWORD)
    else:
        print("No directory found in the registry path.")

if __name__ == "__main__":
    main()
