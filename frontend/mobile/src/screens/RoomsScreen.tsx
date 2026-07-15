import React, { useState, useEffect } from 'react';
import { View, Text, FlatList, StyleSheet, TouchableOpacity, ActivityIndicator, Alert } from 'react-native';
import { Home, ChevronRight, LogOut } from 'lucide-react-native';
import apiClient from '../api/client';
import { useAuthStore } from '../store/authStore';

interface Room {
  id: number;
  name: string;
  description?: string;
}

export default function RoomsScreen({ route }: any) {
  const houseId = route?.params?.houseId;
  const houseName = route?.params?.houseName;
  const [rooms, setRooms] = useState<Room[]>([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const logout = useAuthStore(state => state.logout);

  const fetchRooms = async () => {
    try {
      setLoading(true);
      const url = houseId ? `/rooms/?house_id=${houseId}` : '/rooms/';
      const response = await apiClient.get(url);
      setRooms(response.data);
    } catch (error) {
      console.error('Error fetching rooms:', error);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  const handleLogout = () => {
    Alert.alert('Logout', 'Are you sure you want to logout?', [
      { text: 'Cancel', style: 'cancel' },
      { text: 'Logout', style: 'destructive', onPress: () => logout() }
    ]);
  };

  useEffect(() => {
    fetchRooms();
  }, []);

  const onRefresh = () => {
    setRefreshing(true);
    fetchRooms();
  };

  const renderRoom = ({ item }: { item: Room }) => (
    <TouchableOpacity style={styles.roomCard}>
      <View style={styles.roomIcon}>
        <Home size={24} color="#007AFF" />
      </View>
      <View style={styles.roomInfo}>
        <Text style={styles.roomName}>{item.name}</Text>
        {item.description && <Text style={styles.roomDesc}>{item.description}</Text>}
      </View>
      <ChevronRight size={20} color="#ccc" />
    </TouchableOpacity>
  );

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.headerTitle}>{houseName ? houseName : 'My Rooms'}</Text>
        <TouchableOpacity onPress={handleLogout} style={styles.logoutButton}>
          <LogOut size={20} color="#FF3B30" />
        </TouchableOpacity>
      </View>

      {loading && !refreshing ? (
        <ActivityIndicator style={styles.loader} size="large" color="#007AFF" />
      ) : (
        <FlatList
          data={rooms}
          keyExtractor={(item) => item.id.toString()}
          renderItem={renderRoom}
          contentContainerStyle={styles.list}
          refreshing={refreshing}
          onRefresh={onRefresh}
          ListEmptyComponent={
            <View style={styles.emptyContainer}>
              <Text style={styles.emptyText}>No rooms created yet.</Text>
              <Text style={styles.emptySubtext}>Rooms are automatically created when you tell HomeMind about an object's location.</Text>
            </View>
          }
        />
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#f8f9fa' },
  header: { 
    flexDirection: 'row', 
    justifyContent: 'space-between', 
    alignItems: 'center', 
    paddingHorizontal: 20, 
    paddingTop: 60, 
    paddingBottom: 10,
    backgroundColor: '#fff',
    borderBottomWidth: 1,
    borderBottomColor: '#eee'
  },
  headerTitle: { fontSize: 24, fontWeight: '700', color: '#333' },
  logoutButton: { padding: 8 },
  list: { padding: 15 },
  roomCard: { 
    flexDirection: 'row', 
    alignItems: 'center', 
    backgroundColor: '#fff', 
    padding: 15, 
    borderRadius: 12, 
    marginBottom: 10,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.05,
    shadowRadius: 3,
    elevation: 1
  },
  roomIcon: { 
    width: 48, 
    height: 48, 
    borderRadius: 24, 
    backgroundColor: '#F0F7FF', 
    justifyContent: 'center', 
    alignItems: 'center',
    marginRight: 15
  },
  roomInfo: { flex: 1 },
  roomName: { fontSize: 18, fontWeight: '600', color: '#333' },
  roomDesc: { fontSize: 14, color: '#666', marginTop: 2 },
  loader: { marginTop: 50 },
  emptyContainer: { alignItems: 'center', marginTop: 100, paddingHorizontal: 40 },
  emptyText: { fontSize: 18, fontWeight: '600', color: '#333', marginBottom: 10 },
  emptySubtext: { textAlign: 'center', color: '#999', lineHeight: 20 }
});
