# Fix Windows Long Path Issue for TensorFlow Installation

## Problem
TensorFlow installation fails with:
```
ERROR: Could not install packages due to an OSError: [Errno 2] No such file or directory
HINT: This error might have occurred since this system does not have Windows Long Path support enabled.
```

## Solution: Enable Windows Long Path Support

### Method 1: Using the PowerShell Script (Recommended)

1. **Open PowerShell as Administrator:**
   - Press `Windows Key + X`
   - Select "Windows PowerShell (Admin)" or "Terminal (Admin)"
   - Click "Yes" when prompted by User Account Control

2. **Navigate to your project directory:**
   ```powershell
   cd "C:\Users\Muhammad Shakir\OneDrive\Desktop\HandWritten Digit Recognition\handWrittenDigitRecognition"
   ```

3. **Run the enable script:**
   ```powershell
   .\enable_long_paths.ps1
   ```

4. **Restart your computer** (recommended for changes to take full effect)

5. **After restart, activate your virtual environment and install TensorFlow:**
   ```powershell
   .\venv\Scripts\Activate.ps1
   pip install tensorflow-cpu
   ```

### Method 2: Manual Registry Edit

If the script doesn't work, you can enable it manually:

1. Press `Windows Key + R`
2. Type `regedit` and press Enter
3. Navigate to: `HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\FileSystem`
4. Find `LongPathsEnabled` (or create it if it doesn't exist)
5. Set its value to `1` (DWORD)
6. Restart your computer

### Method 3: Using Group Policy Editor (Windows Pro/Enterprise)

1. Press `Windows Key + R`
2. Type `gpedit.msc` and press Enter
3. Navigate to: `Computer Configuration > Administrative Templates > System > Filesystem`
4. Enable "Enable Win32 long paths"
5. Restart your computer

## Verify Long Path Support is Enabled

After restarting, verify it's enabled:
```powershell
Get-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem' -Name 'LongPathsEnabled'
```

You should see `LongPathsEnabled : 1`

## Alternative: Use Shorter Path (Temporary Workaround)

If you can't enable long paths, you could:
1. Move your project to a shorter path like `C:\Projects\HandWrittenDigitRecognition`
2. Or use a junction/symlink to shorten the path

## After Enabling Long Paths

Once enabled and restarted, try installing TensorFlow again:
```powershell
.\venv\Scripts\Activate.ps1
pip install tensorflow-cpu
```

Or if you prefer the full TensorFlow package:
```powershell
pip install tensorflow
```


