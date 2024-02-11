import winreg
import os

class FileDataReader:
    def read_data(self, file_path):
        try:
            with open(file_path, 'rb') as file:  # Read file in binary mode
                return file.read(), os.path.splitext(file_path)[1] # Return file data and extension
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

class SearchbarImageEditor(RegistryEditor):
    def __init__(self, key):
        super().__init__(key)
        self.search_reg = r"Software\Microsoft\Windows\CurrentVersion\Search"
        self.search_settings_reg = r"Software\Microsoft\Windows\CurrentVersion\SearchSettings\Dynamic"
        self.search_settings_current_reg = self.get_search_settings_dir()
        self.icon_dir = self.get_icon_dir()

    def get_search_settings_dir(self):
        dir_name = self.read_subkey_at_index(self.search_settings_reg, 1)
        if dir_name:
            return self.search_settings_reg + "\\" + dir_name
        raise KeyError("No directory found in the registry path.")
        
    def get_icon_dir(self):
        return self.search_settings_current_reg + r"\icons"

    def set_search_mode(self, mode):
        self.write_value(self.search_reg, "SearchboxTaskbarMode", mode, winreg.REG_DWORD)

    def set_icon_size(self, size):
        self.write_value(self.search_settings_current_reg, "iconSize", size, winreg.REG_DWORD)
    
    def set_content_type(self, content_type):
        if content_type in ["svg", "png", "jpg", "jpeg", "gif", "bmp", "ico"]:
            self.write_value(self.search_settings_current_reg, "contentType", content_type, winreg.REG_EXPAND_SZ)
            return
        raise ValueError("Invalid content type.")
    
    def set_img_data(self, value_name, image_data):
        try:
            with winreg.OpenKey(self.key, self.icon_dir, 0, winreg.KEY_WRITE) as reg_key:
                winreg.SetValueEx(reg_key, value_name, 0, winreg.REG_BINARY, image_data)
                print(f"Image data for {value_name} has been successfully updated.")
        except OSError as e:
            print(f"Error occurred while setting image data: {e}")
    
    def print_image_data(self, value_name):
        image_data = self.read_value(self.icon_dir, value_name)
        if image_data:
            print(f"Image data for {value_name}:")
            print(image_data)
            return
        raise KeyError(f"No image data found for {value_name}.")

    def edit_image_data(self, file_path):
        image_data, ext = FileDataReader().read_data(file_path)

        if image_data:
            try:
                self.set_icon_size(1)
                self.set_content_type(ext[1:])
                
                self.set_search_mode(0) # Set search mode to 0, so icon is not displayed
                self.set_img_data('0', image_data)
                self.set_img_data('1', image_data)
                self.set_search_mode(2) # Set search mode to 2, so icon is initialized and displayed

            except OSError as e:
                print(f"Error occurred while editing image data: {e}")

def main():
    registry_editor = SearchbarImageEditor(winreg.HKEY_CURRENT_USER)
    registry_editor.edit_image_data(os.path.join(os.path.dirname(__file__), "img", "my-png.png"))

if __name__ == "__main__":
    main()
