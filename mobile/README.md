This directory contains a minimal Expo-managed React Native app that lets you pick an image from the gallery or take a photo, upload it to the backend, and display stubbed identification results. It also fetches the built-in crops list from the backend and shows crop details.

Run (you need node + npm/yarn + expo-cli):

1. cd mobile
2. npm install
3. npx expo start

Set BACKEND_URL in App.js to point at your running backend (e.g., http://10.0.2.2:8000 for Android emulator, or your machine IP) before using the app.

Notes:
- Camera support uses Expo's ImagePicker.launchCameraAsync() which works in the Expo client and simulators; on physical devices the permissions prompt will appear.
- The app fetches /crops on startup. Make sure your backend is running and reachable from the device/emulator.
- If you see permission errors, ensure the simulator/emulator or physical device grants camera/gallery permissions.
