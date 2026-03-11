# Local Fitbit ZIP to CSV app

## What this is
This is a local-only Streamlit app that runs on the user's own computer.

- The Python code runs locally.
- The browser is only the interface.
- Input ZIP files stay on the user's machine.
- Output CSV files stay on the user's machine.
- The app is configured to bind to `localhost` only.
- Streamlit usage telemetry is disabled in `.streamlit/config.toml`.

## Files
- `converter.py` - your parsing logic
- `app.py` - local browser UI
- `requirements.txt` - Python dependencies
- `setup_windows.bat` / `setup_mac.command` - one-time setup
- `run_windows.bat` / `run_mac.command` - launch the app
- `build_wheelhouse_windows.bat` / `build_wheelhouse_mac.command` - build an offline dependency bundle for the same OS

## Recommended rollout
Create **two separate bundles**:
- one built on Windows, shared to Windows colleagues
- one built on macOS, shared to Mac colleagues

Do not try to make one single folder for both operating systems.

## Fastest pilot
Use this if colleagues are allowed a one-time package install from the internet or from your organization's internal Python mirror.

### Windows
1. Install Python 3.11 or 3.12.
2. Unzip the folder.
3. Double-click `setup_windows.bat` once.
4. Double-click `run_windows.bat` whenever you want to use the app.
5. The app opens in a browser at `http://localhost:8501`.

### macOS
1. Install Python 3.11 or 3.12.
2. Unzip the folder.
3. Double-click `setup_mac.command` once.
4. Double-click `run_mac.command` whenever you want to use the app.
5. The app opens in a browser at `http://localhost:8501`.

## Offline / no-web install after you distribute it
Use this if colleagues should be able to install dependencies without the app reaching out to the public internet.

### Build the offline bundle on your own machine first
On **Windows**, run:
- `build_wheelhouse_windows.bat`

On **macOS**, run:
- `build_wheelhouse_mac.command`

This creates a local `wheelhouse/` folder with the required Python packages for that operating system.

Then zip the whole app folder, including `wheelhouse/`, and share **that OS-specific zip** with colleagues.

### What your colleagues do
They just run:
- `setup_windows.bat` on Windows, or
- `setup_mac.command` on macOS

The setup scripts automatically prefer the local `wheelhouse/` and install with:
- `--no-index`
- `--find-links wheelhouse`

That means pip installs from the local package folder instead of going to PyPI.

## Important practical limits
1. **Runtime can be fully local/offline.**
   Once setup is complete, the app can run without internet access.

2. **Installation still needs Python.**
   The colleague's machine needs Python 3.11 or 3.12 installed first.

3. **For strict enterprise rollout**, use IT.
   If your organization does not want people to install Python themselves, the cleanest next step is to ask IT to:
   - provide the approved Python runtime, or
   - wrap this folder in an internal signed installer

4. **Build Mac and Windows separately.**
   The `wheelhouse/` contents are OS-specific.

## Suggested internal distribution message
"Unzip the folder, run setup once, then use the run file. The app runs only on your own computer and opens in your browser at localhost. No public server is used."
