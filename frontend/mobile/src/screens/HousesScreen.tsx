import React, { useState, useEffect } from 'react';
import { View, Text, FlatList, StyleSheet, TouchableOpacity, ActivityIndicator, Alert } from 'react-native';
import { Home, ChevronRight, LogOut, Building2 } from 'lucide-react-native';
import apiClient from '../api/client';
import { useAuthStore } from '../store/authStore';

interface House {
  id: number;
  name: string;
  description?: string;
}

export default function HousesScreen({ navigation }: any) {
  const [houses, setHouses] = useState<House[]>([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const logout = useAuthStore(state => state.logout);

  const fetchHouses = async () => {
    try {
      setLoading(true);
      const response = await apiClient.get('/houses/');
      setHouses(response.data);
    } catch (error) {
      console.error('Error fetching houses:', error);
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
    fetchHouses();
  }, []);

  const onRefresh = () => {
    setRefreshing(true);
    fetchHouses();
  };

  const renderHouse = ({ item }: { item: House }) => (
    <TouchableOpacity 
      style={styles.houseCard}
      onPress={() => navigation.navigate('Rooms', { houseId: item.id, houseName: item.name })}
    >
      <View style={styles.houseIcon}>
        <Building2 size={24} color="#007AFF" />
      </View>
      <View style={styles.houseInfo}>
        <Text style={styles.houseName}>{item.name}</Text>
        {item.description && <Text style={styles.houseDesc}>{item.description}</Text>}
      </View>
      <ChevronRight size={20} color="#ccc" />
    </TouchableOpacity>
  );

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.headerTitle}>My Houses</Text>
        <TouchableOpacity onPress={handleLogout} style={styles.logoutButton}>
          <LogOut size={20} color="#FF3B30" />
        </TouchableOpacity>
      </View>

      {loading && !refreshing ? (
        <ActivityIndicator style={styles.loader} size="large" color="#007AFF" />
      ) : (
        <FlatList
          data={houses}
          keyExtractor={(item) => item.id.toString()}
          renderItem={renderHouse}
          contentContainerStyle={styles.list}
          refreshing={refreshing}
          onRefresh={onRefresh}
          ListEmptyComponent={
            <View style={styles.emptyContainer}>
              <Text style={styles.emptyText}>No houses created yet.</Text>
              <Text style={styles.emptySubtext}>You can add a house to organize your rooms and belongings.</Text>
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
  houseCard: { 
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
  houseIcon: { 
    width: 48, 
    height: 48, 
    borderRadius: 24, 
    backgroundColor: '#F0F7FF', 
    justifyContent: 'center', 
    alignItems: 'center',
    marginRight: 15
  },
  houseInfo: { flex: 1 },
  houseName: { fontSize: 18, fontWeight: '600', color: '#333' },
  houseDesc: { fontSize: 14, color: '#666', marginTop: 2 },
  loader: { marginTop: 50 },
  emptyContainer: { alignItems: 'center', marginTop: 100, paddingHorizontal: 40 },
  emptyText: { fontSize: 18, fontWeight: '600', color: '#333', marginBottom: 10 },
  emptySubtext: { textAlign: 'center', color: '#999', lineHeight: 20 }
});
