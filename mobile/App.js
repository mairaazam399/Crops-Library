import React, { useState } from 'react';
import { Button, Image, Platform, StyleSheet, Text, View } from 'react-native';
import * as ImagePicker from 'expo-image-picker';

// Change this to your backend while developing. For Android emulator use 10.0.2.2 if running backend on host machine.
const BACKEND_URL = 'http://10.0.2.2:8000';

export default function App() {
  const [image, setImage] = useState(null);
  const [result, setResult] = useState(null);
  const [uploading, setUploading] = useState(false);

  const pickImage = async () => {
    // Ask for permission
    const permissionResult = await ImagePicker.requestMediaLibraryPermissionsAsync();
    if (!permissionResult.granted) {
      alert('Permission to access gallery is required!');
      return;
    }

    let pickerResult = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      quality: 0.7,
      base64: false,
    });

    if (!pickerResult.cancelled) {
      setImage(pickerResult.uri);
      setResult(null);
    }
  };

  const uploadImage = async () => {
    if (!image) return;
    setUploading(true);
    try {
      const uriParts = image.split('.');
      const fileType = uriParts[uriParts.length - 1];

      const formData = new FormData();
      formData.append('file', {
        uri: image,
        name: `photo.${fileType}`,
        type: `image/${fileType}`,
      });

      const res = await fetch(`${BACKEND_URL}/identify`, {
        method: 'POST',
        body: formData,
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      const data = await res.json();
      setResult(data);
    } catch (err) {
      alert('Upload failed: ' + String(err));
    } finally {
      setUploading(false);
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Crops Library — Mobile Demo</Text>
      <Button title="Pick an image from gallery" onPress={pickImage} />
      {image && (
        <>
          <Image source={{ uri: image }} style={styles.image} />
          <Button title={uploading ? 'Uploading...' : 'Upload & Identify'} onPress={uploadImage} disabled={uploading} />
        </>
      )}

      {result && (
        <View style={styles.results}>
          <Text style={styles.subtitle}>Results:</Text>
          {result.success ? (
            result.predictions.map((p, i) => (
              <Text key={i}>{`${p.name} — ${(p.confidence * 100).toFixed(1)}%`}</Text>
            ))
          ) : (
            <Text>Error: {result.error}</Text>
          )}
        </View>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'flex-start',
    paddingTop: 60,
    paddingHorizontal: 20,
  },
  title: { fontSize: 18, marginBottom: 12 },
  image: { width: 300, height: 300, marginTop: 12, marginBottom: 12 },
  results: { marginTop: 16 },
  subtitle: { fontWeight: 'bold', marginBottom: 6 },
});
