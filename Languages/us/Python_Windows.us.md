
# Python Installation Guide for Windows

This guide will walk you through installing Python on a Windows system. Follow the steps below to properly set up the Python environment.

### Step 1: Download the Python Installer

1. Go to the official Python download page:  
   [https://www.python.org/downloads/](https://www.python.org/downloads/)

2. Click on the download button for the latest version of Python for Windows (it will generally be the most stable version). The page will automatically recognize your operating system and offer the correct installer.

### Step 2: Start the Installation

1. Run the downloaded `.exe` file.
2. **Important**: On the first screen of the installer, check the option **"Add Python to PATH"**. This ensures you can use Python from the terminal in any directory.
3. Click on **"Install Now"** to begin the installation.

### Step 3: Verify the Installation

Once the installation is complete, it's time to verify that Python was installed correctly:

1. Open the **Command Prompt** (press `Win + R`, type `cmd`, and press Enter).
2. Type the following command to check the Python version:
   ```sh
   python --version
   ```
   or, depending on the configuration:
   ```sh
   python3 --version
   ```

   If the installation was successful, you will see the installed Python version, such as:
   ```
   Python 3.x.x
   ```

### Step 4: Install `pip` (Python Package Manager)

`pip` is usually installed automatically with Python. To check if `pip` is installed, run the following command in Command Prompt:

```sh
pip --version
```

If `pip` is not installed, you can download and install it manually by following the instructions at [https://pip.pypa.io/en/stable/installation/](https://pip.pypa.io/en/stable/installation/).

### Step 5: Install Python Packages

With `pip` installed, you can start installing packages and libraries. For example, to install the `requests` library, use the following command:

```sh
pip install requests
```

### Step 6: Set Up a Virtual Environment (Optional but Recommended)

To manage project dependencies in isolation, it is recommended to use virtual environments. To create a virtual environment, follow these steps:

1. In the terminal, navigate to the directory where you want to create the virtual environment.
2. Run the command:
   ```sh
   python -m venv name_of_environment
   ```
   This will create a folder called `name_of_environment` with isolated Python.

3. To activate the virtual environment, use the command:
   ```sh
   name_of_environment\Scripts\activate
   ```

4. Now, any package installed with `pip` will be restricted to this virtual environment.

5. To deactivate the virtual environment, type:
   ```sh
   deactivate
   ```

---

With this, Python will be installed and ready to use on your Windows system. If you encounter any issues, refer to the [official documentation](https://docs.python.org/3/) for more information.
