# Snake Game for Android

A simple snake game with the following features:
- Touch controls (swipe to change direction)
- Regular red apples (1 point)
- Bonus green apples (2 points + wall-passing ability)
- Score tracking
- Game over screen with retry option

## Building the APK

1. Install Python 3.9 (recommended version for best compatibility)
2. Install buildozer:
   ```
   pip install buildozer
   ```
3. Initialize buildozer:
   ```
   buildozer init
   ```
4. Build the APK:
   ```
   buildozer android debug deploy
   ```

The APK will be created in the `bin` directory.
