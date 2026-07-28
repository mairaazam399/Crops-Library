import React, { useState, useEffect } from 'react';
import { ActivityIndicator, Alert, Button, Image, Platform, ScrollView, StyleSheet, Text, TouchableOpacity, View } from 'react-native';
import * as ImagePicker from 'expo-image-picker';

// Change this to your backend while developing. For Android emulator use 10.0.2.2 if running backend on host machine.
const BACKEND_URL = 'http://10.0.2.2:8000';

export default function App() {
  const [image, setImage] = useState(null);
  const [result, setResult] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [crops, setCrops] = useState([]);
  const [loadingCrops, setLoadingCrops] = useState(false);
  const [selectedCrop, setSelectedCrop] = useState(null);

  useEffect(() => {
    fetchCrops();
  }, []);

  const fetchCrops = async () => {
    setLoadingCrops(true);
    try {
      const res = await fetch(`${BACKEND_URL}/crops`);
      if (!res.ok) throw new Error(`Status ${res.status}`);
      const data = await res.json();
      setCrops(data);
    } catch (err) {
      console.warn('Failed to fetch crops:', err);
      Alert.alert('Error', 'Could not load crops. Is the backend running and reachable?');
    } finally {
      setLoadingCrops(false);
    }
  };

  const pickImage = async () => {
    // Ask for permission
    const permissionResult = await ImagePicker.requestMediaLibraryPermissionsAsync();
    if (!permissionResult.granted) {
      Alert.alert('Permission required', 'Permission to access gallery is required!');
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

  const takePhoto = async () => {
    // Ask for camera permission
    const permissionResult = await ImagePicker.requestCameraPermissionsAsync();
    if (!permissionResult.granted) {
      Alert.alert('Permission required', 'Permission to access camera is required!');
      return;
    }

    let cameraResult = await ImagePicker.launchCameraAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      quality: 0.7,
      base64: false,
    });

    if (!cameraResult.cancelled) {
      setImage(cameraResult.uri);
      setResult(null);
    }
  };

  const uploadImage = async () => {
    if (!image) return;
    setUploading(true);
    try {
      // Try to infer file extension, default to jpg
      const extMatch = image.match(/\.([0-9a-zA-Z]+)(?:\?|$)/);
      const fileType = extMatch ? extMatch[1] : 'jpg';

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
          // Let fetch set the correct multipart boundary; omit Content-Type to allow that
        },
      });

      if (!res.ok) {
        const text = await res.text();
        throw new Error(`Upload failed: ${res.status} - ${text}`);
      }

      const data = await res.json();
      setResult(data);
    } catch (err) {
      console.warn(err);
      Alert.alert('Upload failed', String(err));
    } finally {
      setUploading(false);
    }
  };

  const renderCropList = () => {
    if (loadingCrops) return <ActivityIndicator />;
    return (
      <ScrollView style={styles.cropList}>
        {crops.map((c) => (
          <TouchableOpacity key={c.id} style={styles.cropItem} onPress={() => setSelectedCrop(c)}>
            <Text style={styles.cropTitle}>{c.common_name}</Text>
            <Text style={styles.cropSubtitle}>{c.scientific_name}</Text>
          </TouchableOpacity>
        ))}
      </ScrollView>
    );
  };

  if (selectedCrop) {
    return (
      <View style={styles.container}>
        <Text style={styles.title}>{selectedCrop.common_name}</Text>
        <Text style={styles.scientific}>{selectedCrop.scientific_name}</Text>
        <Text style={styles.family}>{selectedCrop.family}</Text>
        <Text style={styles.description}>{selectedCrop.description}</Text>
        <Button title="Back to list" onPress={() => setSelectedCrop(null)} />
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Crops Library — Mobile Demo</Text>

      <View style={styles.buttonRow}>
        <Button title="Pick from gallery" onPress={pickImage} />
        <View style={{ width: 12 }} />
        <Button title="Take photo" onPress={takePhoto} />
      </View>

      {image && (
        <>
          <Image source={{ uri: image }} style={styles.image} />
          <Button title={uploading ? 'Uploading...' : 'Upload & Identify'} onPress={uploadImage} disabled={uploading} />
        </>
      )}

      {result && (
        <View style={styles.results}>
          <Text style={styles.subtitle}>Identification Results:</Text>
          {result.success ? (
            result.predictions.map((p, i) => (
              <Text key={i}>{`${p.name} — ${(p.confidence * 100).toFixed(1)}%`}</Text>
            ))
          ) : (
            <Text>Error: {result.error}</Text>
          )}
        </View>
      )}

      <Text style={[styles.subtitle, { marginTop: 20 }]}>Crops Library</Text>
      {renderCropList()}
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
  buttonRow: { flexDirection: 'row', marginBottom: 12 },
  image: { width: 300, height: 300, marginTop: 12, marginBottom: 12 },
  results: { marginTop: 16 },
  subtitle: { fontWeight: 'bold', marginBottom: 6 },
  cropList: { marginTop: 8, width: '100%' },
  cropItem: { paddingVertical: 12, borderBottomWidth: 1, borderBottomColor: '#eee' },
  cropTitle: { fontSize: 16 },
  cropSubtitle: { color: '#666' },
  scientific: { fontStyle: 'italic', color: '#333', marginBottom: 6 },
  family: { color: '#444', marginBottom: 8 },
  description: { marginBottom: 12 },
});
