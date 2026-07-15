import React, { useState } from 'react';
import { View, Text, TextInput, Button, StyleSheet, TouchableOpacity, ActivityIndicator, Alert } from 'react-native';
import apiClient from '../api/client';
import { useAuthStore } from '../store/authStore';

export default function LoginScreen({ navigation }: any) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const setToken = useAuthStore(state => state.setToken);

  const handleLogin = async () => {
    if (!email || !password) {
      Alert.alert('Error', 'Please enter email and password');
      return;
    }

    setLoading(true);
    try {
      const response = await apiClient.post('/auth/login', { email, password });
      setToken(response.data.access_token);
      // Navigation is handled automatically by AppNavigator based on isAuthenticated state
    } catch (error: any) {
      console.error('Login error:', error);
      const detail = error.response?.data?.detail || 'Could not connect to server';
      Alert.alert('Login Failed', detail);
    } finally {
      setLoading(false);
    }
  };

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>HomeMind AI</Text>
        <Text style={styles.subtitle}>Welcome back! Please login to your account.</Text>
      </View>
      
      <View style={styles.form}>
        <View style={styles.inputGroup}>
          <Text style={styles.label}>Email Address</Text>
          <TextInput 
            placeholder="e.g. user@example.com" 
            style={styles.input} 
            value={email}
            onChangeText={setEmail}
            autoCapitalize="none"
            keyboardType="email-address"
          />
        </View>
        
        <View style={styles.inputGroup}>
          <Text style={styles.label}>Password</Text>
          <TextInput 
            placeholder="Enter your password" 
            style={styles.input} 
            secureTextEntry 
            value={password}
            onChangeText={setPassword}
          />
        </View>
        
        {loading ? (
          <ActivityIndicator size="large" color="#007AFF" style={styles.loader} />
        ) : (
          <TouchableOpacity style={styles.button} onPress={handleLogin}>
            <Text style={styles.buttonText}>Login</Text>
          </TouchableOpacity>
        )}
      </View>

      <View style={styles.footer}>
        <TouchableOpacity onPress={() => navigation.navigate('Register')}>
          <Text style={styles.link}>Don't have an account? <Text style={styles.linkBold}>Register</Text></Text>
        </TouchableOpacity>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: 'center', padding: 25, backgroundColor: '#fff' },
  header: { marginBottom: 40 },
  title: { fontSize: 36, fontWeight: '800', textAlign: 'center', color: '#007AFF', letterSpacing: -1 },
  subtitle: { fontSize: 16, color: '#666', textAlign: 'center', marginTop: 10 },
  form: { width: '100%' },
  inputGroup: { marginBottom: 20 },
  label: { fontSize: 14, fontWeight: '600', color: '#333', marginBottom: 8, marginLeft: 4 },
  input: { 
    borderWidth: 1.5, 
    borderColor: '#eee', 
    padding: 16, 
    borderRadius: 12, 
    backgroundColor: '#fcfcfc',
    fontSize: 16,
    color: '#333'
  },
  button: { 
    backgroundColor: '#007AFF', 
    padding: 18, 
    borderRadius: 12, 
    alignItems: 'center',
    marginTop: 10,
    shadowColor: '#007AFF',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.2,
    shadowRadius: 8,
    elevation: 3
  },
  buttonText: { color: '#fff', fontWeight: '700', fontSize: 18 },
  loader: { marginTop: 20 },
  footer: { marginTop: 30 },
  link: { textAlign: 'center', color: '#666', fontSize: 15 },
  linkBold: { color: '#007AFF', fontWeight: '700' }
});
